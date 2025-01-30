from typing import Optional, Tuple, Union, List, Dict
from pydantic import BaseModel, Field, ConfigDict
from crewai_tools import BaseTool
import vectorbtpro as vbt
import numpy as np
import pandas as pd
from vectorbtpro.signals.enums import FactoryMode
from vectorbtpro.generic.nb import crossed_above_nb, crossed_below_nb
from vectorbtpro.signals.nb import rand_by_prob_place_nb, stop_place_nb, ohlc_stop_place_nb
from vectorbtpro.indicators.configs import flex_elem_param_config
from vectorbtpro.utils import checks
from vectorbtpro.signals.factory import SignalFactory

class ThresholdSignalSchema(BaseModel):
    """Schema para sinais de threshold."""
    threshold: float = Field(..., description="Valor do threshold")
    direction: str = Field(..., description="Direção do threshold (above/below)")

class CrossSignalSchema(BaseModel):
    """Schema para sinais de cruzamento."""
    wait: int = Field(1, description="Número de períodos para esperar entre sinais")

class StopSignalSchema(BaseModel):
    """Schema para sinais de stop."""
    stop_type: str = Field(..., description="Tipo de stop ('loss' ou 'trailing' or 'custom' ")
    stop_value: float = Field(gt=0, le=100.0, description="Stop value in percentage. It can be a float (0..100).")
    entry_price: float = Field(..., description="Entry price for stop calculation,  expected a float")
    trailing_offset: Optional[float] = Field(None, description="Trailing stop optional offset to be substract of low price or add of high price. Will default to zero if wrong argument or None.")

class BaseSignalTool(BaseTool):
    """
    Abstract base class for signal tools, using `np.ndarray` as core of data output, to
    extend the class with custom attributes.
    """
    input_type: str = Field(
        "np.ndarray", 
        description="Type of the base data",
    )

class ThresholdSignalTool(BaseSignalTool):
    name: str = "Threshold Signal Generator"
    description: str = "Gera sinais baseados em threshold"
    args_schema: type[BaseModel] = ThresholdSignalSchema
    
    def _run(
        self,
        shape: Tuple[int, ...],
        values: Union[np.ndarray, pd.Series, list, Dict[str, list]],
        threshold: float,
        direction: str = "above"
    ) -> np.ndarray:
        """
        Generates signals based on thresholds for multiple assets.
        The implementation makes all conversion between array/list or dictionaries automatically.  
        You also explicitely declare which method and attributes from class are required to process it (`SignalFactory`).
        
        Args:
            values (Union[np.ndarray, list, pandas.Series, Dict[str, List[float]]]): The core series to apply the threshold. 
                It may receive array, list, dictionary (or a DataFrames in future)
            threshold: The value of threshold that needs to compare to `values`.
            direction (str): It should be 'above' to select positions when values are above the limit or below otherwise. 
                It can be only one type at time, and returns boolean to check what met or no.

        Returns:
            `np.array`: A flattened bool `numpy.array`, corresponding to the result, when a specific row is above 
                or bellow to `threshold` depending of direction string.

        The outputs should be booleans (and np arrays are expected). Using only this and `SignalFactory` makes your 
        implementation secure and fast. The framework now is doing what Vector has designed for doing.
        """
        if isinstance(values, list):
            values = np.array(values)  # List explicit types to array (for code)
        if isinstance(values, pd.Series):  # Pandas conversion (series object)
            values = np.array(values)
        if isinstance(values, dict):  # Dictionary if pass many assets or anything
            values = np.array(list(values.values())).T
        
        values = np.asarray(values).reshape(-1, 1)
        
        # Gerar sinais baseados no threshold
        if direction == "above":
            signals = values > threshold
        else:
            signals = values < threshold
            
        return signals.reshape(-1)

class CrossSignalTool(BaseSignalTool):
    name: str = "Cross Signal Generator"
    description: str = "Gera sinais baseados em cruzamento"
    args_schema: type[BaseModel] = CrossSignalSchema
    
    def _run(
        self,
        shape: Tuple[int, ...],
        fast_values: Union[np.ndarray, pd.Series, list, Dict[str, list]],
        slow_values: Union[np.ndarray, pd.Series, list, Dict[str, list]],
        wait: int = 1
    ) -> np.ndarray:
        """
        Generates cross signals using SignalFactory and VectorBT internal logic (`crossed_above_nb`).

        Args:
            fast_values (Union[np.ndarray, pandas.Series, List[float], Dict[str, list]]): Data series for faster moving average.
                It can be any array, list, pandas.series with float values. Data types (index etc.) has more priority 
                with the fast values as benchmark. And dict keys with names. If passing more data (more than 1 column), 
                it is expected the values have compatible formats in rows with slow values
            slow_values (Union[np.ndarray, pandas.Series, List[float]], Dict[str, list]]): Data series for slower moving average, 
                following the similar pattern as fast values (`dict/np/list/series`)
            wait (int): Number of periods to wait between signals, defaults `1`.
            
        Returns:
            `np.array` with boolean values in `1-dim` numpy. It will create an output with True or false if 
            a `fast_values` Cross `above` a `slow_values`. If multiple crossing happen only a first of event 
            are taken (as default and documented by implementation by design).
        """
        if isinstance(fast_values, (list, pd.Series)):
            fast_values = np.array(fast_values)
        if isinstance(slow_values, (list, pd.Series)):
            slow_values = np.array(slow_values)
        if isinstance(fast_values, dict):
            fast_values = np.array(list(fast_values.values())).T
        if isinstance(slow_values, dict):
            slow_values = np.array(list(slow_values.values())).T
            
        checks.assert_not_none(fast_values, "Must have a fast values input")
        checks.assert_not_none(slow_values, "Must have a slow values input")
        
        fast_values = np.asarray(fast_values).reshape(-1, 1)
        slow_values = np.asarray(slow_values).reshape(-1, 1)

        # Usar crossed_above_nb diretamente
        entry_signals = crossed_above_nb(fast_values, slow_values, wait=wait)
            
        return entry_signals.reshape(-1)

class StopSignalTool(BaseSignalTool):
    name: str = "Stop Signal Generator"
    description: str = "Gera sinais baseados em stop loss/trailing or 'custom stop loss value for custom rules based on fixed or relative value'."
    args_schema: type[BaseModel] = StopSignalSchema
    
    def _run(
        self,
        shape: Tuple[int, ...],
        values: Union[np.ndarray, pd.Series, List[float], Dict[str, List[float]]],
        stop_type: str,
        stop_value: float,
        entry_price: float,
        trailing_offset: Optional[float] = None,
    ) -> np.ndarray:
        """
        Generate stop signals based on price movement, expecting floats and int type in
        most common use cases (`np.array, pd.Series, list`), and also multiple rows (`dict`) with similar shape and type.
        
        Valid options are:
        * `stop_type` to equal `loss`, `trailing` or `custom` for others cases. If the type isn't defined or have errors, 
          the logic with vector pro does not apply any behavior in `ohlc` or stop at methods and will have `NaN`. 
          (check Vector's Implementation for all parameters in `ohlc_stop_place_nb`). You need to specific them 
          (and also, all errors/exception will fall down and you must document).
          
        Args:
            values (Union[np.ndarray, pandas.Series, List[float], Dict[str, List[float]]]): Price data, where the signals 
                should be placed (`float or list of floats`). Must work similar with pandas series object.
            stop_type (str): Type of stop "loss", "trailing" or custom".
            stop_value (float): percentage of a trade price, valid from 0% until 100%. Value should be used for 
                type trailing/loss. It must be a float value. (Pydantic do validation)
            entry_price (float): Entry price for stop calculation. All calculations in types floats, should return the same way.
            trailing_offset (float|Optional, Default `None`): Optional offset for trailing stop. if the values does not fit 
                in float is treated as 0 (zero).
                
        Returns:
            `np.ndarray`: A flattened bool `numpy.array` where stops (loss/trailing) are reached, using native vectorbt pro. 
            This array use False everywhere as a no signal base. If a custom_stop is used will mark an stop based on if there 
            exist a position.
            
        Notes:
            For *loss*: Signals stop are fixed for every new operation (`entry_price`, is the initial base stop of a operation, 
            at loss will try to calculate only if passed validly). For the initial positions it's checked, in the same bar as 
            `entries`, using close price (`is_entry_open`). Use a custom stop (not specified, `stop_type`, use o `entry_price`, 
            but with fixed position (`my_signal = (c.out, -1)`, the second `lambda`).

            For *trailing*, only uses parameters from prices based in close and the given `trailing_offset`, stop and close prices 
            (`c.high` or `c.low`, and only values from ts) should respect if it's a long or short position and do calculation 
            correctly by taking advantage from all method internal with no need for custom objects at core of the `with_place_func`.
            
            !!! note
                It may also place multiples values in sequence for high variability on volatile data series if new entry come or 
                high volatility. The behavior should follows a chain for multiple exit
        """
        if isinstance(values, (list, pd.Series)):
            values = np.array(values)
        if isinstance(values, dict):
            values = np.array(list(values.values())).T
            
        checks.assert_not_none(values, "Values series cannot be None. A numeric or timeserie (numpy arrays/series like, or list/dictionaries).")
        
        values = np.asarray(values).reshape(-1, 1)
        
        # Calcular sinais de stop
        if stop_type == "loss":
            # Stop loss fixo
            stop_price = entry_price * (1 - stop_value/100)
            signals = values <= stop_price
        elif stop_type == "trailing":
            # Trailing stop
            trailing_offset = trailing_offset if trailing_offset is not None else 0
            high_watermark = np.maximum.accumulate(values)
            stop_price = high_watermark * (1 - stop_value/100 + trailing_offset/100)
            signals = values <= stop_price
        else:
            # Custom stop (retorna False para todos os pontos)
            signals = np.zeros_like(values, dtype=bool)
            
        return signals.reshape(-1)