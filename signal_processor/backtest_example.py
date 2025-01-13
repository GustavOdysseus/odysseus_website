import vectorbtpro as vbt
import numpy as np
import pandas as pd
from signal_tools_final import CrossSignalTool, ThresholdSignalTool, StopSignalTool
from binance.client import Client
from datetime import datetime, timedelta
import pytz

def get_historical_data(symbol="BTCUSDT", timeframe="1h", start="6 months ago"):
    """
    Baixa dados históricos da Binance.
    """
    # Criar cliente Binance (sem autenticação para dados públicos)
    client = Client()
    
    # Converter timeframe para formato da Binance
    timeframe_map = {
        "1m": Client.KLINE_INTERVAL_1MINUTE,
        "5m": Client.KLINE_INTERVAL_5MINUTE,
        "15m": Client.KLINE_INTERVAL_15MINUTE,
        "30m": Client.KLINE_INTERVAL_30MINUTE,
        "1h": Client.KLINE_INTERVAL_1HOUR,
        "4h": Client.KLINE_INTERVAL_4HOUR,
        "1d": Client.KLINE_INTERVAL_1DAY,
    }
    binance_timeframe = timeframe_map.get(timeframe, Client.KLINE_INTERVAL_1HOUR)
    
    # Calcular data inicial
    if isinstance(start, str) and "ago" in start:
        months = int(start.split()[0])
        start_date = datetime.now() - timedelta(days=30*months)
    else:
        start_date = pd.to_datetime(start)
    
    # Baixar dados
    klines = client.get_historical_klines(
        symbol,
        binance_timeframe,
        start_date.strftime("%d %b %Y %H:%M:%S"),
        limit=1000
    )
    
    # Converter para DataFrame
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_volume', 'trades', 'taker_buy_base',
        'taker_buy_quote', 'ignored'
    ])
    
    # Limpar e formatar dados
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
    # Converter colunas para float
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = df[col].astype(float)
    
    return df

def run_backtest(symbol="BTCUSDT", timeframe="1h", start="6 months ago"):
    """
    Executa um backtest completo usando dados da Binance e nossas ferramentas de sinais.
    
    Args:
        symbol (str): Par de trading na Binance
        timeframe (str): Timeframe para os dados
        start (str): Data inicial para os dados
    """
    # 1. Baixar dados da Binance
    data = get_historical_data(symbol, timeframe, start)
    
    # Extrair OHLCV
    close = data['close']
    high = data['high']
    
    # 2. Calcular indicadores
    # Médias móveis para cruzamento
    fast_ma = vbt.MA.run(close, window=20).ma
    slow_ma = vbt.MA.run(close, window=50).ma
    
    # RSI para threshold
    rsi = vbt.RSI.run(close, window=14).rsi
    
    # 3. Gerar sinais
    # Sinais de cruzamento (entrada)
    cross_tool = CrossSignalTool()
    entry_signals = cross_tool._run(
        shape=close.shape,
        fast_values=fast_ma.to_numpy(),
        slow_values=slow_ma.to_numpy(),
        wait=1
    )
    
    # Sinais de threshold RSI (saída)
    threshold_tool = ThresholdSignalTool()
    exit_signals = threshold_tool._run(
        shape=close.shape,
        values=rsi.to_numpy(),
        threshold=70,  # Sobrecomprado
        operation="greater",
        wait=1
    )
    
    # Adicionar stop loss
    stop_tool = StopSignalTool()
    stop_signals = stop_tool._run(
        shape=close.shape,
        close=close.to_numpy(),
        high=high.to_numpy(),
        entry_price=close.iloc[0],  # Exemplo simples
        stop_loss=0.02,  # 2% stop loss
        take_profit=0.05,  # 5% take profit
        trailing_stop=0.03  # 3% trailing stop
    )
    
    # Combinar sinais de saída
    exit_signals = np.logical_or(exit_signals, stop_signals)
    
    # 4. Criar portfolio
    portfolio = vbt.Portfolio.from_signals(
        close=close,
        entries=entry_signals,
        exits=exit_signals,
        init_cash=10000,  # Dinheiro inicial
        fees=0.001,  # 0.1% de taxa
        freq=timeframe
    )
    
    # 5. Analisar resultados
    print("\n=== Resultados do Backtest ===")
    metrics = portfolio.stats()
    
    print(f"Total Return: {metrics['Total Return [%]']:.2f}%")
    print(f"Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}")
    print(f"Max Drawdown: {metrics['Max Drawdown [%]']:.2f}%")
    print(f"Win Rate: {metrics['Win Rate [%]']:.2f}%")
    print(f"Total Trades: {metrics['Total Trades']}")
    print(f"Best Trade: {metrics['Best Trade [%]']:.2f}%")
    print(f"Worst Trade: {metrics['Worst Trade [%]']:.2f}%")
    print(f"Profit Factor: {metrics['Profit Factor']:.2f}")
    
    print("\nMétricas detalhadas:")
    print(metrics)
    
    # 6. Plotar resultados
    portfolio.plot().show()
    
if __name__ == "__main__":
    # Executar backtest
    run_backtest(
        symbol="BTCUSDT",
        timeframe="1h",
        start="6 months ago"
    )
