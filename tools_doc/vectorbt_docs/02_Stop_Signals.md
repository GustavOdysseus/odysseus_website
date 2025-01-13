# Gerenciamento de Sinais no VectorBT Pro

## Visão Geral
O módulo de gerenciamento de sinais no VectorBT Pro fornece ferramentas para processar e otimizar a execução de sinais de trading. Este documento detalha a implementação do sistema de gerenciamento de sinais.

## Estrutura do Sistema

### 1. Gerenciador de Sinais
```python
import vectorbt as vbt
import pandas as pd
import numpy as np
from typing import Dict, List, Union

class SignalManager:
    """
    Gerenciador de sinais de trading.
    """
    
    def __init__(
        self,
        data: pd.DataFrame,
        strategy_params: Dict,
        risk_params: Dict = None
    ):
        """
        Inicializa o gerenciador.
        
        Args:
            data: DataFrame com dados OHLCV
            strategy_params: Parâmetros da estratégia
            risk_params: Parâmetros de risco (opcional)
        """
        self.data = data
        self.strategy_params = strategy_params
        self.risk_params = risk_params or {}
        self.signals = {}
        
    def process_signals(self) -> Dict[str, pd.Series]:
        """
        Processa sinais da estratégia.
        
        Returns:
            Dict[str, pd.Series]: Sinais processados
        """
        # Processa sinais de entrada
        entries = self._process_entries()
        
        # Processa sinais de saída
        exits = self._process_exits()
        
        # Aplica filtros
        entries, exits = self._apply_filters(entries, exits)
        
        # Aplica regras de risco
        entries, exits = self._apply_risk_rules(entries, exits)
        
        return {
            'entries': entries,
            'exits': exits
        }
        
    def _process_entries(self) -> pd.Series:
        """
        Processa sinais de entrada.
        
        Returns:
            pd.Series: Sinais de entrada
        """
        entry_signals = []
        
        for condition in self.strategy_params['entry_conditions']:
            signal = self._generate_signal(condition)
            entry_signals.append(signal)
            
        # Combina sinais conforme lógica definida
        if self.strategy_params.get('entry_logic', 'AND') == 'AND':
            return pd.Series(
                np.all(entry_signals, axis=0),
                index=self.data.index
            )
        else:
            return pd.Series(
                np.any(entry_signals, axis=0),
                index=self.data.index
            )
            
    def _process_exits(self) -> pd.Series:
        """
        Processa sinais de saída.
        
        Returns:
            pd.Series: Sinais de saída
        """
        exit_signals = []
        
        for condition in self.strategy_params['exit_conditions']:
            signal = self._generate_signal(condition)
            exit_signals.append(signal)
            
        return pd.Series(
            np.any(exit_signals, axis=0),
            index=self.data.index
        )
        
    def _generate_signal(self, condition: Dict) -> pd.Series:
        """
        Gera sinal baseado em condição.
        
        Args:
            condition: Dicionário com parâmetros da condição
            
        Returns:
            pd.Series: Sinal gerado
        """
        indicator = condition['indicator']
        params = condition['params']
        operation = condition['operation']
        
        # Calcula indicador
        if indicator == 'RSI':
            values = vbt.RSI.run(
                self.data['close'],
                **params
            ).rsi
        elif indicator == 'MA':
            values = vbt.MA.run(
                self.data['close'],
                **params
            ).ma
        # Adicione mais indicadores conforme necessário
        
        # Aplica operação
        if operation == 'greater_than':
            return values > condition['threshold']
        elif operation == 'less_than':
            return values < condition['threshold']
        elif operation == 'cross_above':
            return values > values.shift(1)
        elif operation == 'cross_below':
            return values < values.shift(1)
            
        raise ValueError(f"Operação não suportada: {operation}")
        
    def _apply_filters(
        self,
        entries: pd.Series,
        exits: pd.Series
    ) -> tuple:
        """
        Aplica filtros aos sinais.
        
        Args:
            entries: Sinais de entrada
            exits: Sinais de saída
            
        Returns:
            tuple: (entradas filtradas, saídas filtradas)
        """
        filters = self.strategy_params.get('filters', {})
        
        # Filtro de volatilidade
        if 'volatility' in filters:
            vol = self.data['close'].pct_change().rolling(
                window=filters['volatility']['window']
            ).std()
            
            vol_filter = vol < filters['volatility']['threshold']
            entries = entries & vol_filter
            
        # Filtro de volume
        if 'volume' in filters:
            vol_ma = self.data['volume'].rolling(
                window=filters['volume']['window']
            ).mean()
            
            vol_filter = self.data['volume'] > vol_ma
            entries = entries & vol_filter
            
        return entries, exits
        
    def _apply_risk_rules(
        self,
        entries: pd.Series,
        exits: pd.Series
    ) -> tuple:
        """
        Aplica regras de risco.
        
        Args:
            entries: Sinais de entrada
            exits: Sinais de saída
            
        Returns:
            tuple: (entradas com risco, saídas com risco)
        """
        if not self.risk_params:
            return entries, exits
            
        # Stop Loss
        if 'stop_loss' in self.risk_params:
            sl = vbt.STOP.run(
                close=self.data['close'],
                entries=entries,
                sl_stop=self.risk_params['stop_loss']
            ).exits
            exits = exits | sl
            
        # Take Profit
        if 'take_profit' in self.risk_params:
            tp = vbt.STOP.run(
                close=self.data['close'],
                entries=entries,
                tp_stop=self.risk_params['take_profit']
            ).exits
            exits = exits | tp
            
        # Trailing Stop
        if 'trailing_stop' in self.risk_params:
            ts = vbt.STOP.run(
                close=self.data['close'],
                entries=entries,
                trail_stop=self.risk_params['trailing_stop']
            ).exits
            exits = exits | ts
            
        return entries, exits
```

### 2. Otimizador de Execução
```python
class ExecutionOptimizer:
    """
    Otimizador de execução de sinais.
    """
    
    def __init__(
        self,
        data: pd.DataFrame,
        signals: Dict[str, pd.Series],
        params: Dict = None
    ):
        """
        Inicializa otimizador.
        
        Args:
            data: DataFrame com dados OHLCV
            signals: Dicionário com sinais
            params: Parâmetros de otimização
        """
        self.data = data
        self.signals = signals
        self.params = params or {}
        
    def optimize_execution(self) -> Dict[str, pd.Series]:
        """
        Otimiza execução dos sinais.
        
        Returns:
            Dict[str, pd.Series]: Sinais otimizados
        """
        entries = self.signals['entries']
        exits = self.signals['exits']
        
        # Aplica regras de timing
        entries = self._apply_timing_rules(entries)
        exits = self._apply_timing_rules(exits)
        
        # Aplica regras de posição
        entries = self._apply_position_rules(entries)
        
        # Aplica regras de execução
        entries, exits = self._apply_execution_rules(entries, exits)
        
        return {
            'entries': entries,
            'exits': exits
        }
        
    def _apply_timing_rules(self, signals: pd.Series) -> pd.Series:
        """
        Aplica regras de timing.
        
        Args:
            signals: Sinais originais
            
        Returns:
            pd.Series: Sinais com timing otimizado
        """
        if 'timing' not in self.params:
            return signals
            
        timing_rules = self.params['timing']
        
        # Regra de horário
        if 'hour_range' in timing_rules:
            hour = self.data.index.hour
            valid_hours = (
                hour >= timing_rules['hour_range'][0]
            ) & (
                hour <= timing_rules['hour_range'][1]
            )
            signals = signals & valid_hours
            
        # Regra de dia da semana
        if 'valid_days' in timing_rules:
            valid_days = self.data.index.dayofweek.isin(
                timing_rules['valid_days']
            )
            signals = signals & valid_days
            
        return signals
        
    def _apply_position_rules(self, entries: pd.Series) -> pd.Series:
        """
        Aplica regras de posição.
        
        Args:
            entries: Sinais de entrada
            
        Returns:
            pd.Series: Sinais com regras de posição
        """
        if 'position' not in self.params:
            return entries
            
        position_rules = self.params['position']
        
        # Máximo de trades simultâneos
        if 'max_trades' in position_rules:
            active_trades = entries.cumsum() - self.signals['exits'].cumsum()
            valid_entries = active_trades < position_rules['max_trades']
            entries = entries & valid_entries
            
        # Máximo de exposição
        if 'max_exposure' in position_rules:
            exposure = self._calculate_exposure()
            valid_entries = exposure < position_rules['max_exposure']
            entries = entries & valid_entries
            
        return entries
        
    def _apply_execution_rules(
        self,
        entries: pd.Series,
        exits: pd.Series
    ) -> tuple:
        """
        Aplica regras de execução.
        
        Args:
            entries: Sinais de entrada
            exits: Sinais de saída
            
        Returns:
            tuple: (entradas otimizadas, saídas otimizadas)
        """
        if 'execution' not in self.params:
            return entries, exits
            
        execution_rules = self.params['execution']
        
        # Delay na execução
        if 'delay' in execution_rules:
            entries = entries.shift(execution_rules['delay'])
            exits = exits.shift(execution_rules['delay'])
            
        # Confirmação de preço
        if 'price_confirmation' in execution_rules:
            threshold = execution_rules['price_confirmation']
            price_change = self.data['close'].pct_change()
            
            valid_entries = price_change > threshold
            valid_exits = price_change < -threshold
            
            entries = entries & valid_entries
            exits = exits & valid_exits
            
        return entries, exits
        
    def _calculate_exposure(self) -> pd.Series:
        """
        Calcula exposição atual.
        
        Returns:
            pd.Series: Exposição ao longo do tempo
        """
        position = self.signals['entries'].cumsum() - self.signals['exits'].cumsum()
        position_value = position * self.data['close']
        portfolio_value = position_value.cumsum()
        
        return position_value / portfolio_value
```

## Uso do Sistema

### 1. Exemplo de Implementação
```python
# Parâmetros da estratégia
strategy_params = {
    'entry_conditions': [
        {
            'indicator': 'RSI',
            'params': {'window': 14},
            'operation': 'less_than',
            'threshold': 30
        },
        {
            'indicator': 'MA',
            'params': {'window': 20},
            'operation': 'cross_above',
            'threshold': None
        }
    ],
    'exit_conditions': [
        {
            'indicator': 'RSI',
            'params': {'window': 14},
            'operation': 'greater_than',
            'threshold': 70
        }
    ],
    'filters': {
        'volatility': {
            'window': 20,
            'threshold': 0.02
        },
        'volume': {
            'window': 20
        }
    },
    'entry_logic': 'AND'
}

# Parâmetros de risco
risk_params = {
    'stop_loss': 0.02,
    'take_profit': 0.03,
    'trailing_stop': 0.015
}

# Parâmetros de otimização
optimization_params = {
    'timing': {
        'hour_range': (9, 16),
        'valid_days': [0, 1, 2, 3, 4]  # Segunda a Sexta
    },
    'position': {
        'max_trades': 3,
        'max_exposure': 0.8
    },
    'execution': {
        'delay': 1,
        'price_confirmation': 0.001
    }
}

# Processa sinais
manager = SignalManager(data, strategy_params, risk_params)
signals = manager.process_signals()

# Otimiza execução
optimizer = ExecutionOptimizer(data, signals, optimization_params)
optimized_signals = optimizer.optimize_execution()

# Executa backtest
portfolio = vbt.Portfolio.from_signals(
    close=data['close'],
    entries=optimized_signals['entries'],
    exits=optimized_signals['exits'],
    freq='1h',
    init_cash=100000,
    fees=0.001
)

# Analisa resultados
print(f"Total Return: {portfolio.total_return():.2%}")
print(f"Sharpe Ratio: {portfolio.sharpe_ratio():.2f}")
print(f"Max Drawdown: {portfolio.max_drawdown():.2%}")
```

## Conclusão
O sistema de gerenciamento de sinais do VectorBT Pro oferece uma estrutura completa para:

1. Processamento eficiente de sinais
2. Otimização de execução
3. Gerenciamento de risco
4. Análise de performance

A estrutura modular e flexível permite fácil extensão e customização para diferentes estratégias e necessidades.
