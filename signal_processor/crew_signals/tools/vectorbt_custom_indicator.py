import sys
from pathlib import Path

# Adiciona o diretório raiz ao Python path
root_dir = str(Path(__file__).parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from typing import Type, Dict, Any
import vectorbtpro as vbt
import pandas as pd
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class VectorBTIndicatorInput(BaseModel):
    """Schema de entrada para a ferramenta VectorBTIndicator."""
    
    expression: str = Field(
        ..., 
        description=(
            "Expressão do indicador no formato VectorBT. Suporta:\n"
            "- Anotações (@in_, @p_, @out_, @talib_, @res_)\n"
            "- Funções do NumPy, TA-Lib e VectorBT\n"
            "- Configurações via @settings\n"
            "- Mapeamento de funções personalizadas\n\n"
            "Exemplos:\n"
            "1. MACD:\n"
            "   ```python\n"
            "   MACD:\n"
            "   fast_ema = @talib_ema(@in_close, @p_fast_w)\n"
            "   slow_ema = @talib_ema(@in_close, @p_slow_w)\n"
            "   macd = fast_ema - slow_ema\n"
            "   signal = @talib_ema(macd, @p_signal_w)\n"
            "   macd, signal\n"
            "   ```\n"
            "2. SuperTrend:\n"
            "   ```python\n"
            "   SuperTrend:\n"
            "   avg_price = (high + low) / 2\n"
            "   up = avg_price + @p_mult * @res_talib_atr\n"
            "   down = avg_price - @p_mult * @res_talib_atr\n"
            "   up, down\n"
            "   ```"
        )
    )
    data: Dict[str, Any] = Field(
        ...,
        description=(
            "Dicionário com as séries temporais de entrada. As chaves podem ser:\n"
            "- 'close': Preços de fechamento\n"
            "- 'open': Preços de abertura\n"
            "- 'high': Preços máximos\n"
            "- 'low': Preços mínimos\n"
            "- 'volume': Volume\n"
            "Exemplo: {'close': close_series, 'high': high_series}"
        )
    )
    parameters: Dict[str, Any] = Field(
        default={},
        description=(
            "Dicionário com os parâmetros do indicador.\n"
            "Exemplo: {'fast_w': 12, 'slow_w': 26, 'signal_w': 9}"
        )
    )
    
    class Config:
        arbitrary_types_allowed = True


class VectorBTIndicator(BaseTool):
    name: str = "VectorBT Indicator Expression"
    description: str = (
        "Cria indicadores técnicos usando expressões do VectorBT. "
        "Permite definir indicadores complexos usando uma sintaxe simples com suporte a "
        "funções do NumPy, TA-Lib e VectorBT. Útil para criar indicadores como MACD, RSI, "
        "Bandas de Bollinger, SuperTrend, etc."
    )
    args_schema: Type[BaseModel] = VectorBTIndicatorInput

    def _run(
        self,
        expression: str,
        data: Dict[str, Any],
        parameters: Dict[str, Any] = {}
    ) -> Any:
        """
        Executa a expressão do indicador usando o VectorBT.
        
        Args:
            expression: Expressão do indicador
            data: Dicionário com as séries temporais
            parameters: Parâmetros do indicador
            
        Returns:
            Resultado do indicador (objeto Pandas)
        """
        try:
            # Criar o indicador a partir da expressão
            indicator = vbt.IF.from_expr(
                expression,
                keep_pd=True,
                **parameters
            )
            
            # Executar o indicador com os dados fornecidos
            result = indicator.run(**data)
            
            return result
            
        except Exception as e:
            return f"Erro ao criar/executar o indicador: {str(e)}"


if __name__ == "__main__":
    # Exemplo de uso da ferramenta
    from tools.fetch_binance_data import FetchBinanceDataTool
    
    # Criar instâncias das ferramentas
    data_tool = FetchBinanceDataTool()
    indicator_tool = VectorBTIndicator()
    
    # Buscar dados
    data = data_tool._run(
        ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT"],
        timeframe="1h",
        start="3 months ago",
        market_type="futures"
    )
    
    # Configurar tema escuro do VectorBT
    vbt.settings.set_theme("dark")
    
    # Exemplo 1: MACD simples
    expr1 = """
    MACD:
    fast_ema = @talib_ema(@in_close, @p_fast_w)
    slow_ema = @talib_ema(@in_close, @p_slow_w)
    macd = fast_ema - slow_ema
    signal = @talib_ema(macd, @p_signal_w)
    macd, signal
    """
    
    macd_ind = indicator_tool._run(
        expression=expr1,
        data={'close': data.close},
        parameters={'fast_w': 12, 'slow_w': 26, 'signal_w': 9}
    )

    print('\nMACD para todos os símbolos:')
    print(macd_ind.macd)
    print('\nSignal para todos os símbolos:')
    print(macd_ind.signal)

    # Exemplo 2: SuperTrend com ATR do TA-Lib
    expr2 = """
    SuperTrend:
    avg_price = (high + low) / 2
    up = avg_price + @p_mult * @res_talib_atr.real.values
    down = avg_price - @p_mult * @res_talib_atr.real.values
    up, down
    """
    
    supertrend_ind = indicator_tool._run(
        expression=expr2,
        data={
            'high': data.high,
            'low': data.low,
            'close': data.close
        },
        parameters={
            'mult': 3,
            'atr_timeperiod': 10,
            'atr_kwargs': {'return_raw': False}
        }
    )

    print('\nSuperTrend Upper Band para todos os símbolos:')
    print(supertrend_ind.up)  
    print('\nSuperTrend Lower Band para todos os símbolos:')
    print(supertrend_ind.down)  
