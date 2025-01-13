# Processamento de Estratégias no VectorBT Pro

## Visão Geral
O módulo de processamento de estratégias no VectorBT Pro fornece uma estrutura robusta para processar parâmetros de estratégia e gerar sinais de trading. Este documento detalha a implementação do sistema de processamento de estratégias.

## Estrutura de Parâmetros

### 1. Formato do Dicionário de Estratégia
```python
strategy_params = {
    'strategy_id': 'STRAT001',
    'timeframe': '1h',
    'signals': {
        'entry': {
            'conditions': [
                {
                    'indicator': 'RSI',
                    'window': 14,
                    'threshold': 30,
                    'operation': 'less_than'
                },
                {
                    'indicator': 'SMA',
                    'fast_window': 10,
                    'slow_window': 20,
                    'operation': 'cross_above'
                }
            ],
            'logic': 'AND'
        },
        'exit': {
            'conditions': [
                {
                    'indicator': 'RSI',
                    'window': 14,
                    'threshold': 70,
                    'operation': 'greater_than'
                }
            ]
        },
        'risk_management': {
            'stop_loss': 0.02,
            'take_profit': 0.03,
            'trailing_stop': 0.015
        }
    }
}
```

## Implementação do Processador

### 1. Classe Base do Processador
```python
import vectorbt as vbt
import pandas as pd
import numpy as np
from typing import Dict, List, Union, Callable

class StrategyProcessor:
    """
    Processador principal de estratégias.
    """
    
    def __init__(
        self,
        data: pd.DataFrame,
        strategy_params: Dict
    ):
        """
        Inicializa o processador.
        
        Args:
            data: DataFrame com dados OHLCV
            strategy_params: Dicionário com parâmetros da estratégia
        """
        self.validate_data(data)
        self.validate_params(strategy_params)
        
        self.data = data
        self.params = strategy_params
        self.indicators = {}
        self.signals = {}
        
    def process_strategy(self) -> vbt.Portfolio:
        """
        Processa a estratégia completa.
        
        Returns:
            vbt.Portfolio: Resultados do backtest
        """
        # Gera indicadores
        self._generate_indicators()
        
        # Gera sinais
        entries = self._process_entry_signals()
        exits = self._process_exit_signals()
        
        # Aplica gerenciamento de risco
        exits = self._apply_risk_management(entries, exits)
        
        # Executa backtest
        return self._run_backtest(entries, exits)
        
    def _generate_indicators(self):
        """Gera todos os indicadores necessários."""
        for signal_type in ['entry', 'exit']:
            conditions = self.params['signals'][signal_type]['conditions']
            for condition in conditions:
                indicator = condition['indicator']
                if indicator not in self.indicators:
                    self.indicators[indicator] = self._calculate_indicator(
                        indicator,
                        condition
                    )
                    
    def _calculate_indicator(
        self,
        indicator: str,
        params: Dict
    ) -> pd.Series:
        """
        Calcula um indicador específico.
        
        Args:
            indicator: Nome do indicador
            params: Parâmetros do indicador
            
        Returns:
            pd.Series: Valores do indicador
        """
        if indicator == 'RSI':
            return vbt.RSI.run(
                self.data['close'],
                window=params['window']
            ).rsi
        elif indicator == 'SMA':
            fast_ma = vbt.MA.run(
                self.data['close'],
                window=params['fast_window']
            ).ma
            slow_ma = vbt.MA.run(
                self.data['close'],
                window=params['slow_window']
            ).ma
            return {'fast': fast_ma, 'slow': slow_ma}
        # Adicione mais indicadores conforme necessário
        
    def _process_entry_signals(self) -> pd.Series:
        """
        Processa sinais de entrada.
        
        Returns:
            pd.Series: Sinais de entrada
        """
        conditions = []
        entry_params = self.params['signals']['entry']
        
        for condition in entry_params['conditions']:
            indicator = condition['indicator']
            operation = condition['operation']
            
            if indicator == 'RSI':
                signal = self.indicators[indicator] < condition['threshold']
            elif indicator == 'SMA':
                mas = self.indicators[indicator]
                signal = mas['fast'] > mas['slow']
                
            conditions.append(signal)
            
        # Combina sinais
        if entry_params['logic'] == 'AND':
            return pd.Series(
                np.all(conditions, axis=0),
                index=self.data.index
            )
        else:  # OR
            return pd.Series(
                np.any(conditions, axis=0),
                index=self.data.index
            )
            
    def _process_exit_signals(self) -> pd.Series:
        """
        Processa sinais de saída.
        
        Returns:
            pd.Series: Sinais de saída
        """
        conditions = []
        exit_params = self.params['signals']['exit']
        
        for condition in exit_params['conditions']:
            indicator = condition['indicator']
            operation = condition['operation']
            
            if indicator == 'RSI':
                signal = self.indicators[indicator] > condition['threshold']
                
            conditions.append(signal)
            
        return pd.Series(
            np.any(conditions, axis=0),
            index=self.data.index
        )
        
    def _apply_risk_management(
        self,
        entries: pd.Series,
        exits: pd.Series
    ) -> pd.Series:
        """
        Aplica regras de gerenciamento de risco.
        
        Args:
            entries: Sinais de entrada
            exits: Sinais de saída
            
        Returns:
            pd.Series: Sinais de saída atualizados
        """
        risk_params = self.params['signals']['risk_management']
        
        # Stop Loss
        sl_exits = vbt.STOP.run(
            close=self.data['close'],
            entries=entries,
            sl_stop=risk_params['stop_loss']
        ).exits
        
        # Take Profit
        tp_exits = vbt.STOP.run(
            close=self.data['close'],
            entries=entries,
            tp_stop=risk_params['take_profit']
        ).exits
        
        # Trailing Stop
        trail_exits = vbt.STOP.run(
            close=self.data['close'],
            entries=entries,
            trail_stop=risk_params['trailing_stop']
        ).exits
        
        return exits | sl_exits | tp_exits | trail_exits
        
    def _run_backtest(
        self,
        entries: pd.Series,
        exits: pd.Series
    ) -> vbt.Portfolio:
        """
        Executa backtest da estratégia.
        
        Args:
            entries: Sinais de entrada
            exits: Sinais de saída
            
        Returns:
            vbt.Portfolio: Resultados do backtest
        """
        return vbt.Portfolio.from_signals(
            close=self.data['close'],
            entries=entries,
            exits=exits,
            freq=self.params['timeframe'],
            init_cash=100000,
            fees=0.001
        )
        
    @staticmethod
    def validate_data(data: pd.DataFrame):
        """Valida dados de entrada."""
        required = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in data.columns for col in required):
            raise ValueError(f"Dados devem conter: {required}")
            
    @staticmethod
    def validate_params(params: Dict):
        """Valida parâmetros da estratégia."""
        required = ['strategy_id', 'timeframe', 'signals']
        if not all(key in params for key in required):
            raise ValueError(f"Parâmetros devem conter: {required}")
```

## Uso do Processador

### 1. Exemplo de Implementação
```python
# Carrega dados
data = pd.read_csv('market_data.csv')

# Define parâmetros da estratégia
strategy_params = {
    'strategy_id': 'STRAT001',
    'timeframe': '1h',
    'signals': {
        'entry': {
            'conditions': [
                {
                    'indicator': 'RSI',
                    'window': 14,
                    'threshold': 30,
                    'operation': 'less_than'
                }
            ],
            'logic': 'AND'
        },
        'exit': {
            'conditions': [
                {
                    'indicator': 'RSI',
                    'window': 14,
                    'threshold': 70,
                    'operation': 'greater_than'
                }
            ]
        },
        'risk_management': {
            'stop_loss': 0.02,
            'take_profit': 0.03,
            'trailing_stop': 0.015
        }
    }
}

# Processa estratégia
processor = StrategyProcessor(data, strategy_params)
results = processor.process_strategy()

# Analisa resultados
print(f"Total Return: {results.total_return():.2%}")
print(f"Sharpe Ratio: {results.sharpe_ratio():.2f}")
print(f"Max Drawdown: {results.max_drawdown():.2%}")
```

### 2. Análise de Resultados
```python
class StrategyAnalyzer:
    """
    Analisador de resultados da estratégia.
    """
    
    def __init__(self, portfolio: vbt.Portfolio):
        self.portfolio = portfolio
        
    def get_metrics(self) -> Dict:
        """
        Calcula métricas principais.
        
        Returns:
            Dict: Métricas de performance
        """
        return {
            'total_return': self.portfolio.total_return(),
            'sharpe_ratio': self.portfolio.sharpe_ratio(),
            'sortino_ratio': self.portfolio.sortino_ratio(),
            'max_drawdown': self.portfolio.max_drawdown(),
            'win_rate': self.portfolio.win_rate(),
            'profit_factor': self.portfolio.profit_factor()
        }
        
    def analyze_trades(self) -> pd.DataFrame:
        """
        Analisa trades individuais.
        
        Returns:
            pd.DataFrame: Análise de trades
        """
        trades = self.portfolio.trades
        
        return pd.DataFrame({
            'entry_price': trades.entry_price,
            'exit_price': trades.exit_price,
            'pnl': trades.pnl,
            'return': trades.returns,
            'duration': trades.duration
        })
        
    def generate_report(self) -> str:
        """
        Gera relatório completo.
        
        Returns:
            str: Relatório formatado
        """
        metrics = self.get_metrics()
        trades = self.analyze_trades()
        
        report = [
            "=== Relatório de Performance ===\n",
            f"Total Return: {metrics['total_return']:.2%}",
            f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}",
            f"Max Drawdown: {metrics['max_drawdown']:.2%}",
            f"Win Rate: {metrics['win_rate']:.2%}",
            f"\nEstatísticas de Trades:",
            f"Número de Trades: {len(trades)}",
            f"Média de Retorno: {trades['return'].mean():.2%}",
            f"Média de Duração: {trades['duration'].mean()}"
        ]
        
        return "\n".join(report)
```

## Conclusão
O sistema de processamento de estratégias do VectorBT Pro oferece uma estrutura flexível e robusta para implementar estratégias baseadas em parâmetros fornecidos por uma equipe de estratégia. O sistema permite:

1. Processamento eficiente de parâmetros
2. Geração flexível de sinais
3. Gerenciamento de risco integrado
4. Análise completa de resultados

A estrutura modular permite fácil extensão para novos indicadores e condições conforme necessário.
