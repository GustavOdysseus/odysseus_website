from typing import Optional, List, Dict, Any, Tuple, Union
from pydantic import BaseModel, Field, ConfigDict
from crewai_tools import BaseTool
import vectorbtpro as vbt
import numpy as np
import pandas as pd
from vectorbtpro.signals.enums import StopType
from vectorbtpro.generic.nb.base import crossed_above_nb, crossed_below_nb

# Schemas para diferentes tipos de sinais
class ThresholdSignalSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    shape: Tuple[int, ...] = Field(
        description="Forma do array de sinais (rows, cols)"
    )
    values: Optional[Union[np.ndarray, pd.Series, Dict[str, np.ndarray]]] = Field(
        default=None,
        description="Array de valores para gerar sinais. Pode ser numpy array, pandas series ou dicionário"
    )
    threshold: Optional[Union[float, Dict[str, float]]] = Field(
        default=None,
        description="Valor de threshold para sinais. Pode ser float ou dicionário"
    )
    operation: Optional[str] = Field(
        default="greater",
        description="Operação de comparação: 'greater' ou 'less'"
    )
    wait: Optional[int] = Field(
        default=1,
        description="Espera entre sinais"
    )

class CrossSignalSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    shape: Tuple[int, ...] = Field(
        description="Forma do array de sinais"
    )
    fast_values: Union[np.ndarray, pd.Series, Dict[str, np.ndarray]] = Field(
        description="Array de valores da linha rápida. Pode ser numpy array, pandas series ou dicionário"
    )
    slow_values: Union[np.ndarray, pd.Series, Dict[str, np.ndarray]] = Field(
        description="Array de valores da linha lenta. Pode ser numpy array, pandas series ou dicionário"
    )
    wait: Optional[int] = Field(
        default=1,
        description="Espera entre sinais"
    )

class StopSignalSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    shape: Tuple[int, ...] = Field(
        description="Forma do array de sinais"
    )
    close: Union[np.ndarray, pd.Series, Dict[str, np.ndarray]] = Field(
        description="Array de preços de fechamento. Pode ser numpy array, pandas series ou dicionário"
    )
    high: Optional[Union[np.ndarray, pd.Series, Dict[str, np.ndarray]]] = Field(
        default=None,
        description="Array de preços máximos para trailing stop. Pode ser numpy array, pandas series ou dicionário"
    )
    entry_price: float = Field(
        default=0.0,
        description="Preço de entrada para cálculo dos stops"
    )
    stop_loss: Optional[float] = Field(
        default=None,
        description="Stop loss em porcentagem (ex: 0.02 para 2%)"
    )
    take_profit: Optional[float] = Field(
        default=None,
        description="Take profit em porcentagem (ex: 0.05 para 5%)"
    )
    trailing_stop: Optional[float] = Field(
        default=None,
        description="Trailing stop em porcentagem (ex: 0.03 para 3%)"
    )

class ThresholdSignalTool(BaseTool):
    name: str = "Threshold Signal Generator"
    description: str = "Gera sinais baseados em threshold"
    args_schema: type[BaseModel] = ThresholdSignalSchema

    def _run(
        self,
        shape: Tuple[int, ...],
        values: Optional[Union[np.ndarray, pd.Series, Dict[str, np.ndarray]]] = None,
        threshold: Optional[Union[float, Dict[str, float]]] = None,
        operation: str = "greater",
        wait: int = 1
    ) -> np.ndarray:
        """
        Gera sinais baseados em threshold usando VectorBT Pro.
        
        Args:
            shape: Forma do array de sinais
            values: Array de valores para comparar
            threshold: Valor de threshold
            operation: Tipo de comparação ('greater' ou 'less')
            wait: Espera entre sinais
            
        Returns:
            Array numpy de sinais (True/False)
        """
        # Converter entrada para formato adequado
        if isinstance(values, dict):
            values = pd.DataFrame(values)
        elif isinstance(values, (np.ndarray, pd.Series)):
            values = pd.Series(values)
            
        if isinstance(threshold, dict):
            threshold = pd.Series(threshold)
            
        # Gerar sinais
        if operation == "greater":
            signals = values > threshold
        else:
            signals = values < threshold
            
        # Aplicar wait
        if wait > 1:
            signals = signals & (
                ~signals.vbt.signals.fshift(wait).fillna(False)
            )
            
        return signals.to_numpy()

class CrossSignalTool(BaseTool):
    name: str = "Cross Signal Generator"
    description: str = "Gera sinais baseados em cruzamento de linhas"
    args_schema: type[BaseModel] = CrossSignalSchema

    def _run(
        self,
        shape: Tuple[int, ...],
        fast_values: Union[np.ndarray, pd.Series, Dict[str, np.ndarray]],
        slow_values: Union[np.ndarray, pd.Series, Dict[str, np.ndarray]],
        wait: int = 1
    ) -> np.ndarray:
        """
        Gera sinais de cruzamento usando VectorBT Pro.
        
        Args:
            shape: Forma do array de sinais
            fast_values: Valores da linha rápida
            slow_values: Valores da linha lenta
            wait: Espera entre sinais
            
        Returns:
            Array numpy de sinais (True/False)
        """
        # Converter entradas para numpy arrays
        if isinstance(fast_values, dict):
            fast_values = np.array(list(fast_values.values())).T
        elif isinstance(fast_values, (pd.Series, pd.DataFrame)):
            fast_values = fast_values.to_numpy()
            
        if isinstance(slow_values, dict):
            slow_values = np.array(list(slow_values.values())).T
        elif isinstance(slow_values, (pd.Series, pd.DataFrame)):
            slow_values = slow_values.to_numpy()
            
        # Garantir que são arrays 2D
        if len(fast_values.shape) == 1:
            fast_values = fast_values.reshape(-1, 1)
        if len(slow_values.shape) == 1:
            slow_values = slow_values.reshape(-1, 1)
            
        # Gerar sinais de cruzamento usando a função otimizada do VectorBT Pro
        signals = crossed_above_nb(
            fast_values,
            slow_values,
            wait=wait
        )
            
        return signals.flatten() if signals.shape[1] == 1 else signals

class StopSignalTool(BaseTool):
    name: str = "Stop Signal Generator"
    description: str = "Gera sinais de stop (stop loss, take profit, trailing stop)"
    args_schema: type[BaseModel] = StopSignalSchema

    def _run(
        self,
        shape: Tuple[int, ...],
        close: Union[np.ndarray, pd.Series, Dict[str, np.ndarray]],
        high: Optional[Union[np.ndarray, pd.Series, Dict[str, np.ndarray]]] = None,
        entry_price: float = 0.0,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        trailing_stop: Optional[float] = None
    ) -> np.ndarray:
        """
        Gera sinais de stop usando VectorBT Pro.
        
        Args:
            shape: Forma do array de sinais
            close: Preços de fechamento
            high: Preços máximos (para trailing stop)
            entry_price: Preço de entrada
            stop_loss: Stop loss em porcentagem
            take_profit: Take profit em porcentagem
            trailing_stop: Trailing stop em porcentagem
            
        Returns:
            Array numpy de sinais (True/False)
        """
        # Converter entradas para formato adequado
        if isinstance(close, dict):
            close = pd.DataFrame(close)
        elif isinstance(close, (np.ndarray, pd.Series)):
            close = pd.Series(close)
            
        if high is not None:
            if isinstance(high, dict):
                high = pd.DataFrame(high)
            elif isinstance(high, (np.ndarray, pd.Series)):
                high = pd.Series(high)
        
        # Criar sinais de stop
        signals = pd.Series(np.zeros(shape[0], dtype=bool))
        
        # Stop Loss
        if stop_loss is not None:
            sl_price = entry_price * (1 - stop_loss)
            signals = signals | (close <= sl_price)
            
        # Take Profit
        if take_profit is not None:
            tp_price = entry_price * (1 + take_profit)
            signals = signals | (close >= tp_price)
            
        # Trailing Stop
        if trailing_stop is not None and high is not None:
            trail_price = high * (1 - trailing_stop)
            signals = signals | (close <= trail_price)
            
        return signals.to_numpy()

# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo
    close = np.array([100, 101, 99, 98, 102, 103, 101, 99])
    fast_ma = np.array([100, 101, 100, 99, 101, 102, 101, 100])
    slow_ma = np.array([99, 100, 100, 100, 100, 101, 101, 101])
    
    # Exemplo de Cross Signal
    cross_tool = CrossSignalTool()
    cross_signals = cross_tool._run(
        shape=close.shape,
        fast_values=fast_ma,
        slow_values=slow_ma,
        wait=1
    )
    print("\nCross Signals:", cross_signals)
    
    # Exemplo de Threshold Signal
    threshold_tool = ThresholdSignalTool()
    threshold_signals = threshold_tool._run(
        shape=close.shape,
        values=close,
        threshold=101,
        operation="greater",
        wait=1
    )
    print("\nThreshold Signals:", threshold_signals)
    
    # Exemplo de Stop Signal
    stop_tool = StopSignalTool()
    stop_signals = stop_tool._run(
        shape=close.shape,
        close=close,
        high=close,  # Usando close como high para exemplo
        entry_price=100,
        stop_loss=0.02,
        take_profit=0.05,
        trailing_stop=0.01
    )
    print("\nStop Signals:", stop_signals)
