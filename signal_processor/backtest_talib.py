import vectorbtpro as vbt
import numpy as np
import pandas as pd
import json
from typing import Tuple, Dict, Any, Optional
from signal_tools_talib import VectorBTIndicator
from tools.fetch_binance_data import FetchBinanceDataTool



def run_signal_test(symbol:str="BTCUSDT", timeframe:str="1h", start:str="6 months ago", strategy_config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
        Executa um teste de sinais usando dados da Binance e a ferramenta `VectorBTIndicator`.

        Args:
             symbol (str): Símbolo do trading pair na Binance (ex: "BTCUSDT")
            timeframe (str): Timeframe para download dos dados, exemplo "1h", "4h" ou "1d".
            start (str):  Período que vai fazer o download de dados usando datetime com a frase (ex: "6 months ago" . O valor  "now UTC" vai fazer o download atual.
           strategy_config (Dict): Dict for parameters and settings . See in Tool class of VectorBTIndicator

         Returns:
              dict: A dictionary with the raw output data (Signals, Indicators, Stop_price, and stop_type) from VectorBTIndicator Tool, formated by Json
        """
    print(f"\nIniciando teste de sinais para {symbol}")
    print(f"Timeframe: {timeframe}")
    print(f"Período: {start} até agora")

    print("\nBaixando dados...")
    binance_data = vbt.BinanceData.pull(
        symbol,
        start=start,
        end="now UTC",
        timeframe=timeframe
    )
    
    data = binance_data.select_symbols(symbol)
    print(f"Dados baixados: {len(data.data[symbol])} candles")
    
     # Extrair OHLCV
    close = data.data[symbol]['Close']
    high = data.data[symbol]['High']
    low = data.data[symbol]['Low']

    if strategy_config is None:
        strategy_config = {}
     # Create object with all abstractions and core of VectorBt

    indicator_tool = VectorBTIndicator()
    # Pass parameters and all types (string, int, bool, list etc. ) to be used inside of the class by pydantic and type hints.
    signal_json = indicator_tool._run(
         expression = strategy_config.get("expression"), # Get arguments from strategies (parameters from a higher level of abstractions). String types explicit, since  your Tool must be flexible for type checking  and type hints explicit for contracts with IA
        data = {'close': close , 'high': data.data[symbol]['High'] , 'low': data.data[symbol]['Low'] }   if "trailing_stop" in strategy_config.get("signal_type","") or  "stop_loss" in strategy_config.get("signal_type","")  else { 'close': close },  # If is or not  ohlc or normal, specific keys or any data type to be compatible (numpy or series)
        parameters = strategy_config.get("parameters", {}), # Parameters of strategy (can be string, list, numpy array, dict, etc, all must be well structured in code from python). This is responsability for your layer
        signal_type = strategy_config.get("signal_type", "threshold_above") , # type of signal. String. Validated also at method of the tool implementation
        threshold_value = strategy_config.get("threshold_value", None)   if "threshold" in strategy_config.get("signal_type", "") else None,  # pass optional  parameter (or a default value None), this is all on pydantic/typehint. String only is a valid key
        stop_value=strategy_config.get("stop_value", None) if  "stop" in strategy_config.get("signal_type", "") else None , # If have stops , all parameters in correct way ( all in strings or number explicit type). You must set to None by convention in parameters that are not used
         entry_price = strategy_config.get("entry_price", None) if  "stop" in strategy_config.get("signal_type", "") else None,
        trailing_offset= strategy_config.get("trailing_offset", None) if "trailing" in strategy_config.get("signal_type", "") else None ,
       wait = strategy_config.get("wait", 1) if "cross" in strategy_config.get("signal_type", "")  else 1, # For cross only

    )
     # Now get the json object. This JSON object can be used in other layer of AI or other frameworks . This is a output object type that serves as a contract.
    output = json.loads(signal_json)
    
    print("\n=== Resultados dos Sinais ===")
     # Returning objects for tests and debug.
    print("\n Signals:", output["signals"])
    print("\nIndicators:", output["indicators"])
    if "stop_price" in output:
      print("\nStop Price:", output["stop_price"])
    if  "stop_type" in output:
      print("\nStop Type:", output["stop_type"])

    return  output # return all

if __name__ == "__main__":
    # Exemplo de uso da ferramenta
    from tools.fetch_binance_data import FetchBinanceDataTool
    
    # Criar instâncias das ferramentas
    data_tool = FetchBinanceDataTool()
   
    
    # Buscar dados
    data = data_tool._run(
         ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT"],
        timeframe="1h",
       start="3 months ago",
       market_type="futures"
   )
    
    # Configurar tema escuro do VectorBT
    vbt.settings.set_theme("dark")
    
     # Exemplo 1: MACD simples com sinais de cruzamento. All parameters in string (and types explicit on code)
    strategy_config_macd = {
        "expression": """
            MACD:
            fast_ema = @talib_ema(@in_close, @p_fast_w)
           slow_ema = @talib_ema(@in_close, @p_slow_w)
            macd = fast_ema - slow_ema
           signal = @talib_ema(macd, @p_signal_w)
            macd, signal
           """,
         "parameters": {'fast_w': 12, 'slow_w': 26, 'signal_w': 9},
        "signal_type": "cross_above",
         "wait": 1
       }

    signals_macd = run_signal_test(
        symbol="BTCUSDT",
        timeframe="1h",
        start="3 months ago",
        strategy_config=strategy_config_macd
    )

    # Exemplo 2: SuperTrend com ATR do TA-Lib e sinal de trailing stop
    strategy_config_supertrend = {
         "expression": """
           SuperTrend:
            avg_price = (high + low) / 2
            up = avg_price + @p_mult * @res_talib_atr.real.values
            down = avg_price - @p_mult * @res_talib_atr.real.values
            up, down
          """,
        "parameters":{
            'mult': 3,
            'atr_timeperiod': 10,
            'atr_kwargs': {'return_raw': False}
         },
        "signal_type": "trailing_stop",
         "stop_value": 1.0,
        "entry_price" : data.close.iloc[0][0],
          "trailing_offset": None,
       }
    
    signals_supertrend = run_signal_test(
         symbol="BTCUSDT",
          timeframe="1h",
         start="3 months ago",
         strategy_config=strategy_config_supertrend
   )
    

    # Exemplo 3: RSI com sinal de Threshold.
    strategy_config_rsi = {
         "expression": """
             RSI:
           rsi = @talib_rsi(@in_close, @p_rsi_w)
             rsi
         """,
         "parameters":{'rsi_w': 14},
      "signal_type": "threshold_above",
        "threshold_value": 70,
    }
   
    signals_rsi = run_signal_test(
       symbol="BTCUSDT",
       timeframe="1h",
         start="3 months ago",
       strategy_config=strategy_config_rsi
    )