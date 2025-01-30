from typing import Tuple, Union, List, Dict, Optional
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
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    shape: Tuple[int, ...]
    values: Union[np.ndarray, List[float], Dict[str, List[float]]]
    threshold: float
    direction: str = "above"


class CrossSignalSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    shape: Tuple[int, ...]
    fast_values: Union[np.ndarray, List[float], Dict[str, List[float]]]
    slow_values: Union[np.ndarray, List[float], Dict[str, List[float]]]
    wait: int = 1


class StopSignalSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    shape: Tuple[int, ...]
    values: Union[np.ndarray, List[float], Dict[str, List[float]]]
    stop_type: str
    stop_value: float
    entry_price: float
    trailing_offset: Optional[float] = None


class ThresholdSignalTool(BaseTool):
    name: str = "Threshold Signal Generator"
    description: str = "Gera sinais baseados em threshold"
    args_schema: type[BaseModel] = ThresholdSignalSchema

    def _run(
        self,
        shape: Tuple[int, ...],
        values: Union[np.ndarray, List[float], Dict[str, List[float]]],
        threshold: float,
        direction: str = "above"
    ) -> np.ndarray:
        """
        Gera sinais de threshold utilizando SignalFactory.
        
        Args:
            values: Data Series of `np.array/List`. Values to compare to the threshold
            threshold: Limit for which, must have for trigger a `True` output
            direction: Direction for comparison ('above' or 'below')

        Returns:
            `np.array` with bool output corresponding to the comparison result
        """
        if isinstance(values, list):
            values = np.array(values)
        if isinstance(values, dict):
            values = np.array(list(values.values())).T
            
        values = np.asarray(values).reshape(-1, 1)  # Ensure 2D array
        
        MySignals = SignalFactory(
            mode=FactoryMode.Entries,
            param_names=['threshold', 'direction']
        ).with_place_func(
            entry_place_func_nb=lambda c, threshold, direction: (
                values > threshold if direction == "above" else values < threshold,
                -1
            ),
            entry_settings=dict(
                pass_kwargs=dict(
                    threshold=threshold,
                    direction=direction
                )
            )
        )

        my_sig = MySignals.run(
            values,
            input_shape=values.shape[0],
            threshold=threshold,
            direction=direction
        )

        return my_sig.entries.reshape(-1)  # Return flattened array


class CrossSignalTool(BaseTool):
    name: str = "Cross Signal Generator"
    description: str = "Gera sinais baseados em cruzamento"
    args_schema: type[BaseModel] = CrossSignalSchema
    
    def _run(
        self,
        shape: Tuple[int, ...],
        fast_values: Union[np.ndarray, List[float], Dict[str, List[float]]],
        slow_values: Union[np.ndarray, List[float], Dict[str, List[float]]],
        wait: int = 1
    ) -> np.ndarray:
        """
        Generates cross signals using vectorbt's crossed_above_nb function.
        
        Args:
            fast_values: Data series for faster moving average
            slow_values: Data series for slower moving average
            wait: Number of periods to wait between signals

        Returns:
            np.array: Boolean array with True where fast crosses above slow
        """
        if isinstance(fast_values, list):
            fast_values = np.array(fast_values)
        if isinstance(slow_values, list):
            slow_values = np.array(slow_values)
        if isinstance(fast_values, dict):
            fast_values = np.array(list(fast_values.values())).T
        if isinstance(slow_values, dict):
            slow_values = np.array(list(slow_values.values())).T
        
        # Ensure 2D arrays with shape (n, 1)
        fast_values = np.asarray(fast_values).reshape(-1, 1)
        slow_values = np.asarray(slow_values).reshape(-1, 1)
        
        # Use SignalFactory with crossed_above_nb
        MySignals = SignalFactory(
            mode=FactoryMode.Chain
        ).with_place_func(
            entry_place_func_nb=crossed_above_nb,
            entry_settings=dict(
                pass_args=['fast_ma', 'slow_ma'],
                pass_kwargs=dict(wait=wait)
            ),
            exit_place_func_nb=vbt.signals.nb.generate_ex_nb,
            exit_settings=dict(
                pass_kwargs=dict(wait=wait)
            )
        )

        my_sig = MySignals.run(
            fast_ma=fast_values,
            slow_ma=slow_values,
            input_shape=fast_values.shape,
            wait=wait
        )

        return my_sig.new_entries.reshape(-1)  # Return flattened array


class StopSignalTool(BaseTool):
    name: str = "Stop Signal Generator"
    description: str = "Gera sinais baseados em stop loss/trailing"
    args_schema: type[BaseModel] = StopSignalSchema
    
    def _run(
        self,
        shape: Tuple[int, ...],
        values: Union[np.ndarray, List[float], Dict[str, List[float]]],
        stop_type: str,
        stop_value: float,
        entry_price: float,
        trailing_offset: Optional[float] = None
    ) -> np.ndarray:
        """
        Generate stop signals based on price movement using SignalFactory.
        
        Args:
            values: Price series data
            stop_type: Type of stop - 'loss' for fixed stop loss or 'trailing' for trailing stop
            stop_value: Stop value in percentage
            entry_price: Entry price for stop calculation
            trailing_offset: Optional offset for trailing stop

        Returns:
            np.array: Boolean array with True where stop is triggered
        """
        if isinstance(values, list):
            values = np.array(values)
        if isinstance(values, dict):
            values = np.array(list(values.values())).T
            
        values = np.asarray(values).reshape(-1, 1)  # Ensure 2D array

        MySignals = SignalFactory(
            mode=FactoryMode.Chain
        ).with_place_func(
            exit_place_func_nb=ohlc_stop_place_nb if stop_type in ["trailing", "loss"]
            else lambda c: (c.out[:], -1),
            exit_settings=dict(
                pass_inputs=['entry_price', 'ts', 'follow_ts', 'close'] if stop_type in ["trailing", "loss"]
                else ['close'],
                pass_params=["stop"] if stop_type == "loss"
                else ["stop", "trailing"],
                pass_kwargs=[
                    ('trailing', True) if stop_type == "trailing" else None,
                    ('entry_price', entry_price) if stop_type == "loss" else None,
                    ('ts', values) if stop_type == "trailing" else None,
                    ('stop', stop_value) if stop_type not in ["loss", "trailing"] else np.nan
                ]
            )
        )

        my_sig = MySignals.run(
            close=values,
            input_shape=values.shape[0],
            stop=stop_value,
            trailing=True if stop_type == "trailing" else False,
            entry_price=entry_price,
            ts=values if stop_type == "trailing" else np.nan,
            follow_ts=values if stop_type == "trailing" else np.nan
        )

        return my_sig.exits.reshape(-1)  # Return flattened array
