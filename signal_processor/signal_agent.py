from crewai import Agent, Task, Crew
from typing import Dict, List
import vectorbtpro as vbt
import pandas as pd
import numpy as np
from signal_tools_vbtpro_v2 import CrossSignalTool, ThresholdSignalTool, StopSignalTool

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
        close = data['Close']
        
        # Médias móveis para CrossSignalTool
        ma_fast = vbt.MA.run(close, window=20).ma
        ma_slow = vbt.MA.run(close, window=50).ma
        
        # RSI para ThresholdSignalTool
        rsi = vbt.RSI.run(close, window=14).rsi
        
        # Criar tarefa de análise
        task = Task(
            description=f"""Analyze the market data and generate trading signals based on:
                          1. MA Cross signals (20 and 50 periods)
                          2. RSI signals (overbought/oversold)
                          3. Stop loss and trailing stop signals
                          
                          Current market data summary:
                          Close Price: {close.iloc[-1]:.2f}
                          Fast MA: {ma_fast.iloc[-1]:.2f}
                          Slow MA: {ma_slow.iloc[-1]:.2f}
                          RSI: {rsi.iloc[-1]:.2f}""",
            expected_output="""A dictionary containing:
                             - Entry signals from MA crossover
                             - Exit signals from RSI and stops
                             - Risk management levels"""
        )
        
        # Gerar sinais
        entry_signals = self.cross_tool._run(
            shape=close.shape,
            fast_values=ma_fast,
            slow_values=ma_slow,
            wait=1
        )
        
        # Sinais de saída baseados em RSI
        rsi_exit = self.threshold_tool._run(
            shape=close.shape,
            values=rsi,
            threshold=70,
            direction="above"
        )
        
        # Stop loss e trailing stop
        stop_signals = self.stop_tool._run(
            shape=close.shape,
            values=close,
            stop_type="trailing",
            stop_value=2.0,  # 2% trailing stop
            entry_price=close.iloc[-1],
            trailing_offset=1.0  # 1% offset
        )
        
        # Combinar sinais de saída
        exit_signals = np.logical_or(rsi_exit, stop_signals)
        
        return {
            'entries': entry_signals,
            'exits': exit_signals,
            'last_close': close.iloc[-1],
            'last_rsi': rsi.iloc[-1],
            'ma_cross': {
                'fast': ma_fast.iloc[-1],
                'slow': ma_slow.iloc[-1]
            },
            'risk_levels': {
                'trailing_stop': close.iloc[-1] * 0.98,  # 2% abaixo
                'rsi_level': 70
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
        fees=0.001
    )
    
    # Mostrar resultados
    print("\nResultados do Backtest:")
    print(portfolio.stats())
    
    return portfolio, signals

if __name__ == "__main__":
    portfolio, signals = main()
