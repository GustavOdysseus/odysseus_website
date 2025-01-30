import pandas as pd
import numpy as np
import os
import sys
import json
import vectorbtpro as vbt

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from typing import Dict, Any, List, Union
from pydantic import BaseModel, Field
from vectorbtpro._typing import Array2d
from vectorbtpro.signals.enums import FactoryMode
from vectorbtpro.signals.nb import rand_by_prob_place_nb, stop_place_nb, ohlc_stop_place_nb
from vectorbtpro.indicators.configs import flex_elem_param_config
from vectorbtpro.utils import checks


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
    signal_type: str = Field(
        ...,
        description="Tipo do sinal a ser gerado ('cross_above', 'threshold_above', 'stop_loss', 'trailing_stop' or 'custom')"
    )
    threshold_value: float = Field(default=None, description="Valor de threshold para sinais de threshold.")
    stop_value: float = Field(default=None, description="Valor de stop para sinais de stop loss/trailing (as percentage value).")
    entry_price: float = Field(default=None, description="Preço de entrada para sinais de stop loss.")
    trailing_offset: float = Field(default=None, description="Trailing stop optional offset to be substract of low price or add of high price")
    wait: int = Field(default=1, description="Number of periods to wait between signals for cross")
    
    class Config:
        arbitrary_types_allowed = True

class VectorBTIndicator:
    name: str = "VectorBT Indicator Expression"
    description: str = (
        "Cria indicadores técnicos usando expressões do VectorBT. "
        "Permite definir indicadores complexos usando uma sintaxe simples com suporte a "
        "funções do NumPy, TA-Lib e VectorBT. Útil para criar indicadores como MACD, RSI, "
        "Bandas de Bollinger, SuperTrend, etc. and output boolean arrays"
    )
    args_schema: Dict[str, Any] = VectorBTIndicatorInput

    def _run(
        self,
        expression: str,
        data: Dict[str, Any],
        parameters: Dict[str, Any] = {},
        signal_type: str = "custom",
        threshold_value: float = None,
        stop_value: float = None,
        entry_price: float = None,
        trailing_offset: float = None,
        wait: int = 1
    ) -> str:
        """
        Executa a expressão do indicador usando o VectorBT e retorna os sinais em JSON.
        
        Args:
            expression: Expressão do indicador
            data: Dicionário com as séries temporais
            parameters: Parâmetros do indicador
            signal_type: Tipo do sinal ('cross_above', 'threshold_above', 'stop_loss', 'trailing_stop' or 'custom')
            threshold_value: Valor de threshold para sinais de threshold
            stop_value: Valor de stop para sinais de stop loss/trailing (as percentage value)
            entry_price: Preço de entrada para sinais de stop loss
            trailing_offset: Trailing stop optional offset
            wait: Number of periods to wait between signals for cross
            
        Returns:
            JSON string com os sinais formatados para o VectorBT Pro
        """
        try:
            # Preparar os parâmetros
            if signal_type == "cross_above":
                # Ajustar expressão para retornar linhas para cruzamento
                if not expression.strip().endswith("macd, signal"):
                    expression = expression.strip() + "\nline1, line2"
                    
            elif signal_type == "threshold_above":
                # Ajustar expressão para retornar linha única
                if not expression.strip().endswith("line"):
                    expression = expression.strip() + "\nline"
                    
            # Criar o indicador a partir da expressão
            indicator = vbt.IF.from_expr(
                expression,
                input_names=list(data.keys()),
                param_names=list(parameters.keys()),
                keep_pd=True
            )
            
            # Executar o indicador com os dados fornecidos
            # Remover prefixos dos inputs e parâmetros
            inputs = {k.replace('in_', ''): v for k, v in data.items()}
            params = {k.replace('p_', ''): v for k, v in parameters.items()}
            result = indicator.run(**inputs, **params)
            
            # Processar os sinais com base no tipo
            if signal_type == "cross_above":
                # Pegar os dois últimos outputs do indicador para comparação
                line1, line2 = result.macd, result.signal
                # Gerar sinais de cruzamento
                long_entry = vbt.crossed_above(line1, line2, wait=wait).values
                long_exit = vbt.crossed_below(line1, line2, wait=wait).values
                short_entry = vbt.crossed_below(line1, line2, wait=wait).values
                short_exit = vbt.crossed_above(line1, line2, wait=wait).values
                
            elif signal_type == "threshold_above":
                if threshold_value is None:
                    raise ValueError("threshold_value é necessário para sinais threshold_above")
                # Pegar o primeiro output do indicador
                line = result.rsi
                # Gerar sinais de threshold
                long_entry = (line > threshold_value).values
                long_exit = (line <= threshold_value).values
                short_entry = (line < threshold_value).values
                short_exit = (line >= threshold_value).values
                
            elif signal_type == "stop_loss":
                if stop_value is None or entry_price is None:
                    raise ValueError("stop_value e entry_price são necessários para sinais stop_loss")
                # Calcular preço de stop
                stop_price = entry_price * (1 - stop_value)
                # Gerar sinais de stop loss
                close = data.get('close', data.get('in_close'))
                long_exit = (close <= stop_price).values
                short_exit = (close >= stop_price).values
                long_entry = np.zeros_like(long_exit)
                short_entry = np.zeros_like(short_exit)
                
            elif signal_type == "trailing_stop":
                if stop_value is None:
                    raise ValueError("stop_value é necessário para sinais trailing_stop")
                # Calcular trailing stop
                close = data.get('close', data.get('in_close'))
                high = data.get('high', close)
                low = data.get('low', close)
                if trailing_offset is not None:
                    high = high + trailing_offset
                    low = low - trailing_offset
                # Gerar sinais de trailing stop usando o módulo signals
                long_exit = vbt.nb.trailing_sl(
                    close=close.values,
                    entries=np.ones_like(close.values),  # Considerar posição sempre aberta
                    stop=stop_value,
                    is_open=True
                )
                short_exit = vbt.nb.trailing_sl(
                    close=close.values,
                    entries=np.ones_like(close.values),
                    stop=stop_value,
                    is_open=True,
                    short=True
                )
                long_entry = np.zeros_like(long_exit)
                short_entry = np.zeros_like(short_exit)
                
            else:  # custom
                # Usar os outputs do indicador diretamente como sinais
                long_entry = result.long_entry
                long_exit = result.long_exit
                short_entry = result.short_entry
                short_exit = result.short_exit
                
                # Extrair valores numpy se necessário
                long_entry = long_entry.values if hasattr(long_entry, 'values') else long_entry
                long_exit = long_exit.values if hasattr(long_exit, 'values') else long_exit
                short_entry = short_entry.values if hasattr(short_entry, 'values') else short_entry
                short_exit = short_exit.values if hasattr(short_exit, 'values') else short_exit
            
            # Converter os sinais para o formato do VectorBT Pro
            signals_dict = {
                'entries': {
                    'long': long_entry.astype(bool).tolist(),
                    'short': short_entry.astype(bool).tolist()
                },
                'exits': {
                    'long': long_exit.astype(bool).tolist(),
                    'short': short_exit.astype(bool).tolist()
                }
            }
            
            # Converter para JSON
            return json.dumps(signals_dict)
            
        except Exception as e:
            import traceback
            return json.dumps({
                "error": f"Erro ao criar/executar o indicador: {str(e)}\n{traceback.format_exc()}"
            })

if __name__ == "__main__":
    # Exemplo de uso da ferramenta
    import yfinance as yf
    import pandas as pd
    import numpy as np
    
    # Configurar tema escuro do VectorBT
    vbt.settings.set_theme("dark")
    
    # Buscar dados do Bitcoin
    btc = yf.download("BTC-USD", start="2023-01-01", end="2024-01-01")
    
    # Criar instância do indicador
    indicator = VectorBTIndicator()
    
    # Teste 1: MACD com sinais de cruzamento
    expr_macd = """
    fast_ema = @talib_ema(close, fast_w)
    slow_ema = @talib_ema(close, slow_w)
    macd = fast_ema - slow_ema
    signal = @talib_ema(macd, signal_w)
    macd, signal
    """
    
    macd_signals = indicator._run(
        expression=expr_macd,
        data={'close': btc['Close']},
        parameters={'fast_w': 12, 'slow_w': 26, 'signal_w': 9},
        signal_type='cross_above'
    )
    
    print('\nMACD Signals (Cross Above):')
    print(macd_signals)
    
    # Teste 2: RSI com sinais de threshold
    expr_rsi = """
rsi = @talib_rsi(close, period)
rsi
"""
    
    rsi_signals = indicator._run(
        expression=expr_rsi,
        data={'close': btc['Close']},
        parameters={'period': 14},
        signal_type='threshold_above',
        threshold_value=70
    )
    
    print('\nRSI Signals (Threshold Above 70):')
    print(rsi_signals)
    
    # Teste 3: Stop Loss fixo
    stop_signals = indicator._run(
        expression="close",  # Apenas para ter um output
        data={
            'close': btc['Close']
        },
        signal_type='stop_loss',
        stop_value=0.02,  # 2% stop loss
        entry_price=btc['Close'].iloc[0]  # Usar primeiro preço como entrada
    )
    
    print('\nStop Loss Signals (2%):')
    print(stop_signals)
    
    # Teste 4: Trailing Stop
    trailing_signals = indicator._run(
        expression="close",  # Apenas para ter um output
        data={
            'close': btc['Close']
        },
        signal_type='trailing_stop',
        stop_value=0.02,  # 2% trailing stop
        trailing_offset=0.001  # 0.1% offset
    )
    
    print('\nTrailing Stop Signals (2% with 0.1% offset):')
    print(trailing_signals)
    
    # Teste 5: Bollinger Bands com sinais customizados
    expr_bb = """
middle = @talib_sma(close, period)
std = @talib_stddev(close, period)
upper = middle + mult * std
lower = middle - mult * std

long_entry = close < lower
long_exit = close > middle
short_entry = close > upper
short_exit = close < middle

long_entry, long_exit, short_entry, short_exit
"""
    
    bb_signals = indicator._run(
        expression=expr_bb,
        data={'close': btc['Close']},
        parameters={'period': 20, 'mult': 2},
        signal_type='custom'
    )
    
    print('\nBollinger Bands Signals (Custom):')
    print(bb_signals)