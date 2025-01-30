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
    """Schema para sinais de threshold."""
    threshold: float = Field(..., description="Valor do threshold")
    direction: str = Field(..., description="Direção do threshold (above/below)")

class CrossSignalSchema(BaseModel):
    """Schema para sinais de cruzamento."""
    wait: int = Field(1, description="Número de períodos para esperar entre sinais")

class StopSignalSchema(BaseModel):
    """Schema para sinais de stop."""
    stop_type: str = Field(..., description="Tipo de stop (loss/trailing)")
    stop_value: float = Field(..., description="Valor do stop em porcentagem")
    entry_price: float = Field(..., description="Preço de entrada para o stop")
    trailing_offset: Optional[float] = Field(None, description="Offset para trailing stop")

class ThresholdSignalTool(BaseTool):
    name: str = "Threshold Signal Generator"
    description: str = "Gera sinais baseados em threshold"
    args_schema: type[BaseModel] = ThresholdSignalSchema
    
    def _run(
        self,
        shape: Tuple[int, ...],
        values: Union[np.ndarray, pd.Series, Dict[str, np.ndarray]],
        threshold: float,
        direction: str = "above"
    ) -> np.ndarray:
        """
        Gera sinais de threshold usando VectorBT Pro.
        
        Args:
            shape: Forma do array de sinais
            values: Valores para comparar com o threshold
            threshold: Valor do threshold
            direction: Direção do threshold (above/below)
            
        Returns:
            Array numpy de sinais (True/False)
        """
        # Converter entrada para numpy array
        if isinstance(values, dict):
            values = np.array(list(values.values())).T
        elif isinstance(values, (pd.Series, pd.DataFrame)):
            values = values.to_numpy()
            
        # Garantir que é array 2D
        if len(values.shape) == 1:
            values = values.reshape(-1, 1)
            
        # Gerar sinais de threshold
        if direction == "above":
            signals = values > threshold
        else:
            signals = values < threshold
            
        return signals.flatten() if signals.shape[1] == 1 else signals

class CrossSignalTool(BaseTool):
    name: str = "Cross Signal Generator"
    description: str = "Gera sinais baseados em cruzamento"
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
        signals = vbt.crossed_above_nb(
            fast_values,
            slow_values,
            wait=wait
        )
            
        return signals.flatten() if signals.shape[1] == 1 else signals

class StopSignalTool(BaseTool):
    name: str = "Stop Signal Generator"
    description: str = "Gera sinais baseados em stop loss/trailing"
    args_schema: type[BaseModel] = StopSignalSchema
    
    def _run(
        self,
        shape: Tuple[int, ...],
        values: Union[np.ndarray, pd.Series, Dict[str, np.ndarray]],
        stop_type: str,
        stop_value: float,
        entry_price: float,
        trailing_offset: Optional[float] = None
    ) -> np.ndarray:
        """
        Gera sinais de stop usando VectorBT Pro.
        
        Args:
            shape: Forma do array de sinais
            values: Valores para comparar com o stop
            stop_type: Tipo de stop (loss/trailing)
            stop_value: Valor do stop em porcentagem
            entry_price: Preço de entrada para o stop
            trailing_offset: Offset para trailing stop
            
        Returns:
            Array numpy de sinais (True/False)
        """
        # Converter entrada para numpy array
        if isinstance(values, dict):
            values = np.array(list(values.values())).T
        elif isinstance(values, (pd.Series, pd.DataFrame)):
            values = values.to_numpy()
            
        # Garantir que é array 2D
        if len(values.shape) == 1:
            values = values.reshape(-1, 1)
            
        # Calcular preço do stop
        if stop_type == "loss":
            stop_price = entry_price * (1 - stop_value/100)
            signals = values < stop_price
        else:  # trailing
            if trailing_offset is None:
                trailing_offset = stop_value
            
            # Calcular máximos acumulados
            running_max = np.maximum.accumulate(values, axis=0)
            stop_prices = running_max * (1 - trailing_offset/100)
            signals = values < stop_prices
            
        return signals.flatten() if signals.shape[1] == 1 else signals


if __name__ == "__main__":
    # Teste simples
    # Criar dados de exemplo
    close = np.array([100, 101, 99, 98, 102, 103, 101, 100])
    ma_fast = np.array([99, 100, 100, 99, 100, 102, 102, 101])
    ma_slow = np.array([98, 99, 100, 100, 99, 100, 102, 102])
    
    # Testar CrossSignalTool
    cross_tool = CrossSignalTool()
    cross_signals = cross_tool._run(
        shape=close.shape,
        fast_values=ma_fast,
        slow_values=ma_slow,
        wait=1
    )
    print("\nCross Signals:", cross_signals)
    
    # Testar ThresholdSignalTool
    threshold_tool = ThresholdSignalTool()
    threshold_signals = threshold_tool._run(
        shape=close.shape,
        values=close,
        threshold=101,
        direction="above"
    )
    print("\nThreshold Signals:", threshold_signals)
    
    # Testar StopSignalTool
    stop_tool = StopSignalTool()
    stop_signals = stop_tool._run(
        shape=close.shape,
        values=close,
        stop_type="loss",
        stop_value=2,
        entry_price=100
    )
    print("\nStop Signals:", stop_signals)
