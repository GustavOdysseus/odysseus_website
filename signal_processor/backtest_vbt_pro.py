import vectorbtpro as vbt
import numpy as np
import pandas as pd
from signal_tools_gemini import CrossSignalTool, ThresholdSignalTool, StopSignalTool
from datetime import datetime, timedelta


def run_backtest(symbol="BTCUSDT", timeframe="1h", start="6 months ago"):
    """
    Executa um backtest completo usando dados da Binance via VectorBT Pro.
    
    Args:
        symbol (str): Trading pair
        timeframe (str): Frame for download, example: "1h" "4h" , "1d"
        start (str): Period data range to analyse by now, example "6 months ago"

    Returns:
        tuple: (Portfolio object, metrics dictionary)
    """
    print(f"\nIniciando backtest para {symbol}")
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

    print("\nCalculando indicadores...")
    # Médias móveis para sinais de entrada
    fast_ma = vbt.MA.run(close, window=20).ma
    slow_ma = vbt.MA.run(close, window=50).ma
    
    # RSI para sinais de saída
    rsi = vbt.RSI.run(close, window=14).rsi

    print("\nGerando sinais...")
    # Sinais de entrada baseados em cruzamento de médias
    cross_tool = CrossSignalTool()
    entry_signals = cross_tool._run(
        shape=close.shape,
        fast_values=fast_ma.to_numpy(),
        slow_values=slow_ma.to_numpy(),
        wait=1
    )
    
    # Sinais de saída baseados em RSI sobrecomprado
    threshold_tool = ThresholdSignalTool()
    exit_signals_rsi = threshold_tool._run(
        shape=rsi.shape,
        values=rsi.to_numpy(),
        threshold=70,  # Nível de sobrecompra
        direction="above"
    )

    # Sinais de saída baseados em stop loss
    stop_tool = StopSignalTool()
    stop_signals = stop_tool._run(
        shape=close.shape,
        values=close.to_numpy(),
        stop_type="trailing",  # Usando trailing stop
        stop_value=2.0,  # 2% trailing stop
        entry_price=close.iloc[0],
        trailing_offset=None
    )
    
    # Combinar sinais de saída (RSI ou stop loss)
    exit_signals = np.logical_or(exit_signals_rsi, stop_signals)

    print("\nCriando portfolio e executando backtest...")
    portfolio = vbt.Portfolio.from_signals(
        close=close,
        entries=entry_signals,
        exits=exit_signals,
        init_cash=10000,
        fees=0.001,
        freq=timeframe,
        direction='longonly',  # Apenas posições long
        size=np.inf,  # Usar todo o capital disponível
        price=close,  # Usar preço de fechamento
        slippage=0.001,  # 0.1% de slippage
        log=True  # Registrar todas as operações
    )

    print("\n=== Resultados do Backtest ===")
    metrics = portfolio.stats()
    
    print(f"\nResumo:")
    print(f"Total Return: {metrics['Total Return [%]']:.2f}%")
    print(f"Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}")
    print(f"Max Drawdown: {metrics['Max Drawdown [%]']:.2f}%")
    print(f"Win Rate: {metrics['Win Rate [%]']:.2f}%")
    
    print(f"\nOperações:")
    print(f"Total Trades: {metrics['Total Trades']}")
    print(f"Best Trade: {metrics['Best Trade [%]']:.2f}%")
    print(f"Worst Trade: {metrics['Worst Trade [%]']:.2f}%")
    print(f"Profit Factor: {metrics['Profit Factor']:.2f}")
    
    # Plotar gráfico do portfolio
    portfolio.plot().show()
    
    return portfolio, metrics


if __name__ == "__main__":
    # Executar backtest
    portfolio, metrics = run_backtest(
        symbol="BTCUSDT",
        timeframe="1h",
        start="6 months ago"
    )