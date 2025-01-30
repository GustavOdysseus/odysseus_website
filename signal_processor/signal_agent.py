from crewai import Agent, Task, Crew
from typing import Dict, List
import vectorbtpro as vbt
import pandas as pd
import numpy as np
from signal_tools_final import CrossSignalTool, ThresholdSignalTool, StopSignalTool

class SignalGeneratorAgent:
    def __init__(self):
        # Criar agente CrewAI
        self.agent = Agent(
            role="Trading Signal Generator",
            goal="Generate high-quality trading signals using technical analysis",
            backstory="""You are an expert trading signal generator with deep knowledge 
                        of technical analysis. Your role is to analyze market data and 
                        generate reliable trading signals using a combination of 
                        indicators while maintaining strict risk management.""",
            verbose=True
        )
        
        # Inicializar ferramentas
        self.cross_tool = CrossSignalTool()
        self.threshold_tool = ThresholdSignalTool()
        self.stop_tool = StopSignalTool()

    def analyze_market(self, data: pd.DataFrame) -> Dict:
        """
        Analisa o mercado e gera sinais de trading
        
        Args:
            data: DataFrame com dados OHLCV
        """
        # Calcular indicadores
        close = data['Close'].to_numpy()
        high = data['High'].to_numpy()
        
        # Médias móveis para CrossSignalTool
        ma_fast = vbt.MA.run(close, window=20).ma.to_numpy()
        ma_slow = vbt.MA.run(close, window=50).ma.to_numpy()
        
        # RSI para ThresholdSignalTool
        rsi = vbt.RSI.run(close, window=14).rsi.to_numpy()
        
        # Criar tarefa de análise
        task = Task(
            description=f"""Analyze the market data and generate trading signals based on:
                          1. MA Cross signals (20 and 50 periods)
                          2. RSI signals (overbought/oversold)
                          3. Stop loss and trailing stop signals
                          
                          Current market data summary:
                          Close Price: {close[-1]:.2f}
                          Fast MA: {ma_fast[-1]:.2f}
                          Slow MA: {ma_slow[-1]:.2f}
                          RSI: {rsi[-1]:.2f}""",
            expected_output="""A dictionary containing:
                             - Entry signals from MA crossover
                             - Exit signals from RSI and stops
                             - Risk management levels"""
        )
        
        # Gerar sinais de entrada (MA Cross)
        entry_signals = self.cross_tool._run(
            shape=close.shape,
            fast_ma=ma_fast,
            slow_ma=ma_slow,
            wait=1
        ).entries
        
        # Gerar sinais de saída baseados em RSI
        rsi_signals = self.threshold_tool._run(
            shape=close.shape,
            values=rsi,
            threshold=70,  # Overbought
            operation="greater",
            wait=1
        ).exits
        
        # Gerar sinais de stop
        stop_signals = self.stop_tool._run(
            shape=close.shape,
            close=close,
            high=high,
            entry_price=close[-1],  # Usar último preço como referência
            stop_loss=0.02,  # 2% stop loss
            take_profit=0.04,  # 4% take profit
            trailing_stop=0.015  # 1.5% trailing stop
        ).exits
        
        # Combinar sinais de saída (RSI ou stops)
        exit_signals = np.logical_or(rsi_signals, stop_signals)
        
        return {
            'entries': entry_signals,
            'exits': exit_signals,
            'last_close': close[-1],
            'last_rsi': rsi[-1],
            'ma_cross': {
                'fast': ma_fast[-1],
                'slow': ma_slow[-1]
            }
        }

def main():
    # Criar agente
    agent = SignalGeneratorAgent()
    
    # Baixar dados
    data = vbt.BinanceData.pull(
        "BTCUSDT",
        start="1 month ago UTC",
        end="now UTC",
        timeframe="1h"
    ).get()  # Adicionando .get() para obter o DataFrame
    
    # Gerar sinais
    signals = agent.analyze_market(data)
    
    # Criar portfolio para backtest
    portfolio = vbt.Portfolio.from_signals(
        close=data['Close'],
        entries=signals['entries'],
        exits=signals['exits'],
        init_cash=10000,
        fees=0.001,
        freq='1h'  # Adicionar frequência
    )
    
    # Mostrar resultados
    print("\nResultados do Backtest:")
    print(portfolio.stats())
    
    return portfolio, signals

if __name__ == "__main__":
    portfolio, signals = main()
