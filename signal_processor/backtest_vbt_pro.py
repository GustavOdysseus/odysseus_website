import vectorbtpro as vbt
import numpy as np
import pandas as pd
from signal_tools_final import CrossSignalTool, ThresholdSignalTool, StopSignalTool
from datetime import datetime, timedelta

def run_backtest(symbol="BTCUSDT", timeframe="1h", start="6 months ago"):
    """
    Executa um backtest completo usando dados da Binance via VectorBT Pro.
    
    Args:
        symbol (str): Par de trading na Binance
        timeframe (str): Timeframe para os dados (ex: "1h", "4h", "1d")
        start (str): Data inicial para os dados (ex: "6 months ago", "1 year ago")
    """
    print(f"\nIniciando backtest para {symbol}")
    print(f"Timeframe: {timeframe}")
    print(f"Período: {start} até agora")
    
    # 1. Baixar dados da Binance via VectorBT Pro
    print("\nBaixando dados...")
    binance_data = vbt.BinanceData.pull(
        symbol,
        start=start,
        end="now UTC",  # Até agora em UTC
        timeframe=timeframe
    )
    # Selecionar dados do símbolo
    data = binance_data.select_symbol(symbol)
    print(f"Dados baixados: {len(data)} candles")
    
    # Extrair OHLCV
    close = data['Close']
    high = data['High']
    
    # 2. Calcular indicadores
    print("\nCalculando indicadores...")
    # Médias móveis para cruzamento
    fast_ma = vbt.MA.run(close, window=20).ma
    slow_ma = vbt.MA.run(close, window=50).ma
    
    # RSI para threshold
    rsi = vbt.RSI.run(close, window=14).rsi
    
    # 3. Gerar sinais
    print("\nGerando sinais...")
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
    print("\nCriando portfolio e executando backtest...")
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
    
    print("\nMétricas detalhadas:")
    print(metrics)
    
    # 6. Plotar resultados
    print("\nGerando gráficos...")
    portfolio.plot().show()
    
    return portfolio, metrics
    
if __name__ == "__main__":
    # Executar backtest
    portfolio, metrics = run_backtest(
        symbol="BTCUSDT",
        timeframe="1h",
        start="6 months ago"
    )
