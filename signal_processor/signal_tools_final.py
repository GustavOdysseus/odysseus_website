from typing import Optional, List, Dict, Any, Tuple
from pydantic import BaseModel, Field, ConfigDict
from crewai_tools import BaseTool
import vectorbt as vbt
import numpy as np
from vectorbt.signals import nb
from vectorbt.base.accessors import BaseAccessor, BaseDFAccessor, BaseSRAccessor

# Schemas para diferentes tipos de sinais
class ThresholdSignalSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    shape: Tuple[int, ...] = Field(
        description="Forma do array de sinais (rows, cols)"
    )
    values: Optional[np.ndarray] = Field(
        default=None,
        description="Array de valores para gerar sinais"
    )
    threshold: Optional[float] = Field(
        default=None,
        description="Valor de threshold para sinais"
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
    fast_values: np.ndarray = Field(
        description="Array de valores da linha rápida"
    )
    slow_values: np.ndarray = Field(
        description="Array de valores da linha lenta"
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
    close: np.ndarray = Field(
        description="Preços de fechamento"
    )
    high: Optional[np.ndarray] = Field(
        default=None,
        description="Preços máximos (para trailing stop)"
    )
    entry_price: float = Field(
        description="Preço de entrada"
    )
    stop_loss: Optional[float] = Field(
        default=None,
        description="Stop loss em %"
    )
    take_profit: Optional[float] = Field(
        default=None,
        description="Take profit em %"
    )
    trailing_stop: Optional[float] = Field(
        default=None,
        description="Trailing stop em %"
    )

# Funções Numba otimizadas
@nb.njit
def threshold_entry_place_nb(signals, values, threshold, operation="greater", wait=1):
    """Coloca sinal baseado em threshold."""
    last_entry = -wait
    for i in range(len(signals)):
        if operation == "greater" and values[i] > threshold:
            if i - last_entry >= wait:
                signals[i] = True
                last_entry = i
        elif operation == "less" and values[i] < threshold:
            if i - last_entry >= wait:
                signals[i] = True
                last_entry = i
    return last_entry

@nb.njit
def cross_entry_place_nb(signals, fast_values, slow_values, wait=1):
    """Coloca sinal quando uma linha cruza outra."""
    last_entry = -wait
    for i in range(1, len(signals)):
        if fast_values[i] > slow_values[i] and fast_values[i-1] <= slow_values[i-1]:
            if i - last_entry >= wait:
                signals[i] = True
                last_entry = i
    return last_entry

@nb.njit
def stop_exit_place_nb(signals, close, high, entry_price, stop_loss=None, take_profit=None, trailing_stop=None):
    """Coloca sinais de stop."""
    max_price = high[0] if high is not None else close[0]
    
    for i in range(len(signals)):
        current_price = close[i]
        
        if high is not None:
            max_price = max(max_price, high[i])
        
        # Stop Loss
        if stop_loss is not None and current_price <= entry_price * (1 - stop_loss):
            signals[i] = True
            return i
            
        # Take Profit
        if take_profit is not None and current_price >= entry_price * (1 + take_profit):
            signals[i] = True
            return i
            
        # Trailing Stop
        if trailing_stop is not None and current_price <= max_price * (1 - trailing_stop):
            signals[i] = True
            return i
            
    return -1

# Ferramentas CrewAI
class ThresholdSignalTool(BaseTool):
    name: str = "Threshold Signal Generator"
    description: str = "Gera sinais baseados em threshold"
    args_schema: type[BaseModel] = ThresholdSignalSchema

    def _run(
        self,
        shape: Tuple[int, ...],
        values: Optional[np.ndarray] = None,
        threshold: Optional[float] = None,
        operation: str = "greater",
        wait: int = 1
    ) -> np.ndarray:
        if values is None:
            values = np.random.randn(*shape)
        
        # Criar array de saída
        signals = np.zeros(shape, dtype=bool)
        
        # Gerar sinais
        threshold_entry_place_nb(signals, values, threshold if threshold is not None else 0.0, operation, wait)
        
        return signals

class CrossSignalTool(BaseTool):
    name: str = "Cross Signal Generator"
    description: str = "Gera sinais baseados em cruzamento de linhas"
    args_schema: type[BaseModel] = CrossSignalSchema

    def _run(
        self,
        shape: Tuple[int, ...],
        fast_values: np.ndarray,
        slow_values: np.ndarray,
        wait: int = 1
    ) -> np.ndarray:
        # Criar array de saída
        signals = np.zeros(shape, dtype=bool)
        
        # Gerar sinais
        cross_entry_place_nb(signals, fast_values, slow_values, wait)
        
        return signals

class StopSignalTool(BaseTool):
    name: str = "Stop Signal Generator"
    description: str = "Gera sinais de stop (stop loss, take profit, trailing stop)"
    args_schema: type[BaseModel] = StopSignalSchema

    def _run(
        self,
        shape: Tuple[int, ...],
        close: np.ndarray,
        high: Optional[np.ndarray] = None,
        entry_price: float = 0.0,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        trailing_stop: Optional[float] = None
    ) -> np.ndarray:
        # Criar array de saída
        signals = np.zeros(shape, dtype=bool)
        
        # Gerar sinais
        stop_exit_place_nb(
            signals,
            close,
            high if high is not None else close,
            entry_price,
            stop_loss,
            take_profit,
            trailing_stop
        )
        
        return signals

# Exemplo de uso:
if __name__ == "__main__":
    # Exemplo de Threshold
    threshold_tool = ThresholdSignalTool()
    shape = (100,)
    values = np.random.randn(*shape)
    threshold_signals = threshold_tool._run(shape=shape, values=values, threshold=0.5)
    print(f"Sinais de threshold gerados: {np.sum(threshold_signals)} sinais")

    # Exemplo de Cruzamento
    cross_tool = CrossSignalTool()
    fast_ma = np.random.randn(100)
    slow_ma = np.random.randn(100)
    cross_signals = cross_tool._run(shape=shape, fast_values=fast_ma, slow_values=slow_ma)
    print(f"Sinais de cruzamento gerados: {np.sum(cross_signals)} sinais")

    # Exemplo de Stop
    stop_tool = StopSignalTool()
    close_prices = np.cumsum(np.random.randn(100)) + 100
    high_prices = close_prices + abs(np.random.randn(100))
    stop_signals = stop_tool._run(
        shape=shape,
        close=close_prices,
        high=high_prices,
        entry_price=100.0,
        stop_loss=0.02,
        take_profit=0.05,
        trailing_stop=0.03
    )
    print(f"Sinais de stop gerados: {np.sum(stop_signals)} sinais")
