# Documentação do VectorBT Pro

## Introdução

O VectorBT Pro é um framework poderoso para análise vetorizada de dados financeiros, backtesting e otimização de estratégias de trading. Ele combina a eficiência da computação vetorizada do NumPy com a flexibilidade do Pandas para fornecer uma solução completa para análise quantitativa.

## 1. Conceitos Fundamentais

### Sistema de Importação
O VectorBT Pro oferece um sistema flexível de importação com diferentes modos:

```python
# Importação completa (modo "all")
from vectorbtpro import *  # Importa todas as funcionalidades

# Importação mínima (modo "minimal")
import vectorbtpro as vbt  # Importa apenas o essencial

# Verificação de importações
vbt.whats_imported()  # Mostra o que foi importado
```

### Configuração do Sistema
```python
# Configurações de importação
vbt.settings['importing']['auto_import'] = True
vbt.settings['importing']['clear_pycache'] = True
vbt.settings['importing']['star_import'] = 'minimal'

# Silenciando warnings específicos
import warnings
warnings.filterwarnings("ignore", category=NumbaExperimentalFeatureWarning)
```

### Acessores Pandas
O VectorBT Pro estende o Pandas através de acessores personalizados:
- `vbt`: Acessor principal
- `signals`: Para processamento de sinais
- `returns`: Para análise de retornos
- `ohlcv`: Para dados OHLCV
- `portfolio`: Para análise de portfólio

### Computação Vetorizada
- Utiliza NumPy para operações vetorizadas
- Suporte à compilação JIT via Numba
- Otimização automática de performance

## 2. Funcionalidades Principais

### Sistema de Wrapping
```python
import vectorbtpro as vbt
import numpy as np
import pandas as pd

# Criar um ArrayWrapper a partir de um objeto
sr = pd.Series([1, 2, 3], name='data')
wrapper = vbt.ArrayWrapper.from_obj(sr)

# Criar um ArrayWrapper a partir de shape
wrapper = vbt.ArrayWrapper.from_shape((100, 3))

# Usar wrapping para manipular arrays
class MyWrapping(vbt.Wrapping):
    def __init__(self, wrapper, array):
        super().__init__(wrapper)
        self._array = array
        
    @property
    def array(self):
        return self._array
        
    def some_operation(self):
        return self.array * 2

# Criar instância
array = np.array([[1, 2], [3, 4]])
wrapper = vbt.ArrayWrapper.from_obj(array)
wrapped = MyWrapping(wrapper, array)

# Operações com grupos
grouped = wrapped.regroup([0, 0, 1])  # agrupa colunas
for key, value in grouped.items():
    print(f"Grupo {key}:")
    print(value.array)
```

### Sistema de Indicadores
```python
import vectorbtpro as vbt
import numpy as np
import pandas as pd

# 1. Usando indicadores pré-construídos
price = pd.DataFrame({
    'a': [1, 2, 3, 4, 5],
    'b': [5, 4, 3, 2, 1]
}, index=pd.date_range('2020-01-01', periods=5))

# Calculando médias móveis
ma = vbt.MA.run(price, [10, 20])
rsi = vbt.RSI.run(price, [14, 21])

# 2. Criando indicador personalizado
@vbt.indicator
def CustomMA(close, window):
    """Média móvel personalizada."""
    return pd.DataFrame.rolling(close, window).mean()

# Usando o indicador personalizado
custom_ma = CustomMA.run(price, window=[10, 20])

# 3. Usando IndicatorFactory
class SuperIndicator(vbt.IndicatorFactory):
    def __init__(self, **kwargs):
        super().__init__(
            input_names=['close'],
            param_names=['window1', 'window2'],
            output_names=['ma1', 'ma2', 'cross_above']
        )
        
    def custom_func(self, close, window1, window2):
        # Cálculos personalizados
        ma1 = pd.DataFrame.rolling(close, window1).mean()
        ma2 = pd.DataFrame.rolling(close, window2).mean()
        cross_above = ma1 > ma2
        return ma1, ma2, cross_above

# Usando o indicador personalizado
super_ind = SuperIndicator.run(
    price,
    window1=[10, 20],
    window2=[20, 30]
)
```

### Manipulação de Dados
```python
# Reshaping de arrays
array = np.array([1, 2, 3, 4])
wrapper = vbt.ArrayWrapper.from_shape(array.shape)

# Broadcast para 2D
array_2d = wrapper.broadcast_array(array)

# Stacking de arrays
wrapper1 = vbt.ArrayWrapper.from_shape((2, 2))
wrapper2 = vbt.ArrayWrapper.from_shape((2, 2))
stacked = wrapper1.column_stack(wrapper2)

# Indexação avançada
subset = wrapped.iloc[0:2, [0, 1]]
```

### Análise de Dados
```python
# Exemplo de carregamento de dados
import vectorbtpro as vbt
data = vbt.YFData.download('AAPL')
```

### Indicadores Técnicos
```python
# Exemplo de cálculo de médias móveis
ma = vbt.MA.run(close, [10, 20, 30])
```

### Backtesting
```python
# Exemplo de backtesting simples
pf = vbt.Portfolio.from_signals(
    close=price,
    entries=entries,
    exits=exits
)
```

## 3. Componentes do Sistema

### Sistema de Dados
- Suporte a múltiplas fontes de dados
- Cache inteligente
- Processamento eficiente

### Sistema de Indicadores Avançado
```python
# 1. Indicador com múltiplos parâmetros e outputs
@vbt.indicator(
    input_names=['close', 'volume'],
    param_names=['fast_window', 'slow_window', 'signal_window'],
    output_names=['macd', 'signal', 'hist']
)
def CustomMACD(close, volume, fast_window, slow_window, signal_window):
    """MACD personalizado com volume."""
    # Cálculo do MACD
    fast_ma = pd.DataFrame.rolling(close, fast_window).mean()
    slow_ma = pd.DataFrame.rolling(close, slow_window).mean()
    macd = fast_ma - slow_ma
    
    # Ajuste pelo volume
    volume_factor = volume / volume.rolling(signal_window).mean()
    macd = macd * volume_factor
    
    # Linha de sinal
    signal = macd.rolling(signal_window).mean()
    hist = macd - signal
    
    return macd, signal, hist

# 2. Uso com otimização de parâmetros
price = pd.DataFrame({
    'close': [1, 2, 3, 4, 5],
    'volume': [10, 20, 15, 30, 25]
}, index=pd.date_range('2020-01-01', periods=5))

# Executando com múltiplos parâmetros
result = CustomMACD.run(
    price['close'],
    price['volume'],
    fast_window=[12, 26],
    slow_window=[26, 52],
    signal_window=[9, 21]
)

# 3. Análise dos resultados
for param_combo in result.items():
    print(f"Parâmetros: {param_combo[0]}")
    print(f"MACD: {param_combo[1].macd}")
    print(f"Signal: {param_combo[1].signal}")
    print(f"Histogram: {param_combo[1].hist}")
```

### Sistema de Portfólio
- Simulação realista de trades
- Análise de performance
- Métricas de risco

### Sistema de Wrapping e Arrays
```python
# Exemplo de uso avançado do sistema de wrapping

# 1. Criação de wrapper personalizado
class CustomWrapper(vbt.ArrayWrapper):
    def __init__(self, *args, custom_param=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_param = custom_param
        
    def custom_method(self):
        return f"Custom param: {self.custom_param}"

# 2. Uso com dados financeiros
import yfinance as yf
data = yf.download('AAPL', start='2020-01-01')
wrapper = vbt.ArrayWrapper.from_obj(data)

# 3. Agrupamento temporal
daily = wrapper.resample('1D')
weekly = wrapper.resample('1W')

# 4. Operações em grupo
groups = wrapper.group_by(['High', 'High', 'Low', 'Low'])
for name, group in groups.items():
    print(f"Grupo {name}:")
    print(group.array)
```

## 4. Configuração e Personalização

### Configurações Globais
```python
# Configurações básicas
vbt.settings['plotting']['layout']['width'] = 800

# Configurações de importação
vbt.settings['importing'].update({
    'auto_import': True,  # Importação automática de módulos
    'clear_pycache': True,  # Limpa cache Python ao iniciar
    'star_import': 'minimal'  # Modo de importação global
})
```

### Temas e Visualização
```python
# Exemplo de mudança de tema
vbt.settings.set_theme('dark')
```

## 5. Análise de Performance

### Métricas Principais
- Retorno total
- Sharpe ratio
- Drawdown máximo
- Outras métricas personalizáveis

### Visualização
```python
# Exemplo de visualização
pf.plot()
```

### Performance de Indicadores
```python
# 1. Análise de cruzamento de médias móveis
ma_cross = vbt.MA.run(
    price,
    [10, 20],
    param_names=['fast', 'slow']
)

# Gerando sinais
entries = ma_cross.fast_ma > ma_cross.slow_ma
exits = ma_cross.fast_ma < ma_cross.slow_ma

# Backtesting
pf = vbt.Portfolio.from_signals(
    close=price,
    entries=entries,
    exits=exits,
    size=1.0,
    freq='1D'
)

# Análise de performance
print(pf.stats())
pf.plot().show()
```

## 6. Otimização e Backtesting

### Otimização de Parâmetros
```python
# Exemplo de otimização
indicator = vbt.IndicatorFactory(...)
params = {'window': range(10, 51, 10)}
result = indicator.run(**params)
```

### Análise de Resultados
- Métricas por parâmetro
- Visualização de resultados
- Seleção de melhores parâmetros

## 7. Boas Práticas

### Performance
1. Use computação vetorizada quando possível
2. Aproveite o cache inteligente
3. Utilize processamento paralelo para tarefas pesadas
4. Configure corretamente o modo de importação para otimizar a memória

### Memória
1. Limpe cache quando necessário
2. Use tipos de dados apropriados
3. Evite cópias desnecessárias
4. Escolha o modo de importação adequado:
   - Use 'minimal' para projetos pequenos
   - Use 'none' para controle total
   - Use 'all' apenas quando necessário

### Indicadores
1. Use vetorização sempre que possível
2. Aproveite o cache para cálculos repetitivos
3. Utilize parâmetros múltiplos para otimização
4. Mantenha indicadores imutáveis
5. Documente inputs, outputs e parâmetros

### Wrapping e Arrays
1. Use ArrayWrapper para metadata consistente
2. Mantenha wrappers imutáveis
3. Aproveite o sistema de grupos
4. Utilize broadcast quando necessário
5. Prefira operações vetorizadas

### Importação e Módulos
1. Importe apenas o necessário
2. Use aliases consistentes (vbt)
3. Gerencie warnings adequadamente
4. Mantenha controle sobre o cache Python

## 8. Exemplos de Uso

### Exemplo Completo de Indicadores
```python
import vectorbtpro as vbt
import numpy as np
import pandas as pd

# 1. Definição do indicador
class VolumeWeightedMACD(vbt.IndicatorFactory):
    def __init__(self, **kwargs):
        # Configuração do indicador
        super().__init__(
            input_names=['close', 'volume'],
            param_names=['fast', 'slow', 'signal', 'volume_factor'],
            output_names=['macd', 'signal', 'hist', 'volume_weight'],
            output_flags=dict(
                macd=dict(title='MACD Line'),
                signal=dict(title='Signal Line'),
                hist=dict(title='Histogram'),
                volume_weight=dict(title='Volume Weight')
            )
        )
        
    def custom_func(self, close, volume, fast, slow, signal, volume_factor):
        # Cálculos
        fast_ma = close.rolling(fast).mean()
        slow_ma = close.rolling(slow).mean()
        macd = fast_ma - slow_ma
        
        # Peso do volume
        volume_sma = volume.rolling(signal).mean()
        volume_weight = (volume / volume_sma) ** volume_factor
        
        # Ajuste do MACD pelo volume
        macd = macd * volume_weight
        signal_line = macd.rolling(signal).mean()
        hist = macd - signal_line
        
        return macd, signal_line, hist, volume_weight

# 2. Uso do indicador
# Dados de exemplo
data = pd.DataFrame({
    'close': np.random.randn(100).cumsum(),
    'volume': np.random.randint(1000, 10000, 100)
}, index=pd.date_range('2020-01-01', periods=100))

# Execução com múltiplos parâmetros
vw_macd = VolumeWeightedMACD.run(
    data['close'],
    data['volume'],
    fast=[12, 26],
    slow=[26, 52],
    signal=[9, 21],
    volume_factor=[0.5, 1.0]
)

# 3. Análise dos resultados
# Plotagem
vw_macd.plot()

# Estatísticas
for param_tuple, param_macd in vw_macd.items():
    print(f"\nParâmetros: {param_tuple}")
    print("Média MACD:", param_macd.macd.mean())
    print("Média Signal:", param_macd.signal.mean())
    print("Média Volume Weight:", param_macd.volume_weight.mean())

# 4. Backtesting
entries = vw_macd.macd > vw_macd.signal
exits = vw_macd.macd < vw_macd.signal

portfolio = vbt.Portfolio.from_signals(
    close=data['close'],
    entries=entries,
    exits=exits,
    init_cash=100000,
    fees=0.001,
    freq='1D'
)

# 5. Análise de performance
print("\nEstatísticas do Portfolio:")
print(portfolio.stats())
portfolio.plot().show()
```

## 9. Recursos Adicionais

### Documentação Oficial
- [Documentação do VectorBT Pro](https://vectorbt.pro/documentation)
- [Exemplos](https://vectorbt.pro/examples)
- [API Reference](https://vectorbt.pro/api)

### Comunidade
- [GitHub](https://github.com/polakowo/vectorbt)
- [Discord](https://discord.gg/vectorbt)
- [Blog](https://vectorbt.pro/blog)

## 1. Conceitos Fundamentais
{{ ... }}

## 2. Funcionalidades Principais
{{ ... }}

### Sistema de Portfólio
```python
import vectorbtpro as vbt
import pandas as pd
import numpy as np

# 1. Simulação Básica de Portfólio
# Dados de exemplo
close = pd.DataFrame({
    'AAPL': [100, 101, 102, 101, 100],
    'GOOGL': [2500, 2510, 2520, 2515, 2500]
}, index=pd.date_range('2024-01-01', periods=5))

# Criando sinais de trading
entries = pd.DataFrame({
    'AAPL': [True, False, True, False, False],
    'GOOGL': [False, True, False, True, False]
}, index=close.index)

exits = pd.DataFrame({
    'AAPL': [False, True, False, True, False],
    'GOOGL': [False, False, True, False, True]
}, index=close.index)

# Simulando o portfólio
pf = vbt.Portfolio.from_signals(
    close=close,
    entries=entries,
    exits=exits,
    init_cash=100000,
    fees=0.001,
    freq='1D'
)

# 2. Análise de Performance
# Métricas básicas
print("Total Return:", pf.total_return())
print("Sharpe Ratio:", pf.sharpe_ratio())
print("Max Drawdown:", pf.max_drawdown())

# Análise de trades
trades = pf.trades
print("\nTrades Statistics:")
print(trades.stats())

# Análise de drawdowns
drawdowns = pf.drawdowns
print("\nDrawdowns Statistics:")
print(drawdowns.stats())

# 3. Otimização de Portfólio
# Definindo parâmetros para otimização
windows = [10, 20, 30]
thresholds = [0.5, 1.0, 1.5]

@vbt.indicator
def custom_signal(close, window, threshold):
    """Indicador personalizado para gerar sinais."""
    ma = close.rolling(window).mean()
    std = close.rolling(window).std()
    upper = ma + threshold * std
    lower = ma - threshold * std
    entries = close < lower
    exits = close > upper
    return entries, exits

# Executando otimização
entries, exits = custom_signal.run(
    close,
    window=windows,
    threshold=thresholds,
    param_product=True
)

# Simulando portfólios com diferentes parâmetros
pf_opt = vbt.Portfolio.from_signals(
    close=close,
    entries=entries,
    exits=exits,
    init_cash=100000,
    fees=0.001,
    freq='1D'
)

# Analisando resultados da otimização
metrics = pd.DataFrame({
    'total_return': pf_opt.total_return(),
    'sharpe_ratio': pf_opt.sharpe_ratio(),
    'max_drawdown': pf_opt.max_drawdown()
})

# 4. Visualização
# Plot do valor do portfólio
pf.plot().show()

# Plot de drawdowns
pf.drawdowns.plot().show()

# Plot de trades
pf.trades.plot().show()

# 5. Análise Avançada
# Análise de risco
print("\nRisk Metrics:")
print("Beta:", pf.beta())
print("Alpha:", pf.alpha())
print("Information Ratio:", pf.information_ratio())

# Análise de trades por período
print("\nTrades por Período:")
print(pf.trades.get_trades_by_period())

# Análise de exposição
print("\nExposição:")
print("Média de Exposição:", pf.exposure())
print("Tempo no Mercado (%):", pf.market_participation())
```

### Sistema de Indicadores
{{ ... }}

### Sistema de Wrapping
{{ ... }}

## 3. Componentes do Sistema

### Sistema de Portfólio Avançado
```python
# 1. Configuração Avançada de Portfólio
pf_config = vbt.PortfolioConfig(
    init_cash=100000,
    fees=0.001,
    slippage=0.001,
    freq='1D',
    cash_sharing=True,
    call_seq='auto',
    ffill_price=True,
    update_value=True,
    fill_pos_info=True
)

# 2. Ordens Avançadas
# Market orders
pf_market = vbt.Portfolio.from_orders(
    close=close,
    size=1000,
    price=close,
    fees=0.001,
    fixed_fees=1.0,
    slippage=0.001,
    min_size=100,
    max_size=10000,
    reject_prob=0.1,
    lock_cash=True,
    allow_partial=True,
    raise_reject=False,
    log=True
)

# Limit orders
limit_price = close * 0.99  # 1% abaixo do preço de fechamento
pf_limit = vbt.Portfolio.from_orders(
    close=close,
    size=1000,
    price=limit_price,
    order_type='limit',
    limit_delta=0.01,
    limit_tif='day',
    limit_expiry=1,
    log=True
)

# 3. Análise de Risco Avançada
# Value at Risk (VaR)
print("Value at Risk (95%):", pf.value_at_risk(confidence=0.95))
print("Conditional VaR (95%):", pf.conditional_value_at_risk(confidence=0.95))

# Métricas de Risco Ajustadas
print("Sortino Ratio:", pf.sortino_ratio())
print("Calmar Ratio:", pf.calmar_ratio())
print("Omega Ratio:", pf.omega_ratio())

# 4. Otimização de Portfólio Avançada
from vectorbtpro.portfolio.pfopt import PortfolioOptimizer

# Configurando otimizador
optimizer = PortfolioOptimizer(
    returns=pf.returns(),
    target_return=0.15,
    risk_free_rate=0.02,
    constraints={
        'min_weight': 0.0,
        'max_weight': 0.5,
        'target_vol': 0.2
    }
)

# Otimizando pesos
optimal_weights = optimizer.optimize()
print("Pesos Otimizados:", optimal_weights)

# 5. Análise de Drawdowns Avançada
drawdowns = pf.drawdowns

# Estatísticas detalhadas
print("\nEstatísticas de Drawdowns:")
print("Número de Drawdowns:", len(drawdowns))
print("Drawdown Médio:", drawdowns.avg_drawdown())
print("Duração Média:", drawdowns.avg_duration())

# Top drawdowns
print("\nTop 5 Drawdowns:")
top_drawdowns = drawdowns.get_top_drawdowns(5)
for dd in top_drawdowns:
    print(f"Start: {dd.start}")
    print(f"Valley: {dd.valley}")
    print(f"End: {dd.end}")
    print(f"Drawdown: {dd.drawdown}")
    print("---")

# 6. Logging e Debug
logs = pf.logs
print("\nLogs de Execução:")
print(logs.records)

# Filtrando logs por tipo
rejected_orders = logs.get_records_of_type('OrderRejected')
print("\nOrdens Rejeitadas:")
print(rejected_orders)
```

### Sistema de Indicadores Avançado
{{ ... }}

### Sistema de Wrapping e Arrays
{{ ... }}

## 4. Configuração e Personalização
{{ ... }}

## 5. Análise de Performance
{{ ... }}

## 6. Otimização e Backtesting
{{ ... }}

## 7. Boas Práticas

### Portfolio
1. Sempre configure o capital inicial adequadamente
2. Use cash_sharing quando apropriado para otimizar recursos
3. Implemente controle de risco com stop-loss e take-profit
4. Monitore custos de transação e slippage
5. Mantenha logs detalhados para debugging
6. Utilize otimização de parâmetros com cuidado
7. Valide resultados com diferentes períodos de tempo
8. Considere rebalanceamento periódico
9. Implemente gestão de risco adequada
10. Documente todas as decisões de trading

### Indicadores
{{ ... }}

### Wrapping e Arrays
{{ ... }}

## 8. Exemplos de Uso
{{ ... }}

## 9. Recursos Adicionais
{{ ... }}

### Sistema de Otimização de Portfólio

O VectorBT Pro inclui um sistema robusto de otimização de portfólio com recursos avançados de alocação de ativos:

#### Otimização de Portfólio

O módulo de otimização de portfólio (`portfolio.pfopt`) oferece diversas funcionalidades para otimização e alocação de ativos:

1. **Métodos de Alocação**:
   - Alocação uniforme (`from_uniform`)
   - Alocação aleatória (`from_random`)
   - Alocação personalizada (`from_allocate_func`)
   - Otimização via função customizada (`from_optimize_func`)

2. **Integrações com Bibliotecas**:
   ```python
   # Exemplo de otimização com PyPortfolioOpt
   pf_opt = vbt.PortfolioOptimizer.from_pypfopt(
       prices=prices_df,        # DataFrame de preços
       method='efficient_risk', # Método de otimização
       target_volatility=0.1,   # Volatilidade alvo
       weight_bounds=(0, 0.5)   # Limites de peso
   )
   ```

   ```python
   # Exemplo de otimização com Riskfolio-Lib
   pf_opt = vbt.PortfolioOptimizer.from_riskfolio(
       returns=returns_df,      # DataFrame de retornos
       model='Classic',         # Modelo de otimização
       rm='MV',                # Risk Measure: Mean-Variance
       obj='Sharpe',           # Objetivo: Maximizar Sharpe
       rf=0.0,                 # Taxa livre de risco
       l=2                     # Fator de aversão ao risco
   )
   ```

3. **Funcionalidades Avançadas**:
   ```python
   # Otimização com janela móvel
   pf_opt = vbt.PortfolioOptimizer.from_optimize_func(
       wrapper=prices.vbt.wrapper,
       optimize_func=custom_optimize,  # Função customizada
       prices=prices,
       window=252,                    # Janela de 1 ano
       every='M'                      # Rebalanceamento mensal
   )
   ```

4. **Recursos de Parametrização**:
   - Suporte a múltiplos grupos de configuração
   - Parametrização flexível de argumentos
   - Otimização com Numba para performance
   - Manipulação avançada de índices temporais

5. **Análise de Resultados**:
   ```python
   # Análise básica
   allocations = pf_opt.allocations              # Alocações atuais
   mean_alloc = pf_opt.mean_allocation          # Alocação média
   filled = pf_opt.filled_allocations           # Alocações preenchidas
   
   # Análise estatística
   stats = pf_opt.stats()
   coverage = stats['coverage']                 # Cobertura das alocações
   total_records = stats['total_records']       # Total de registros
   overlap = stats['overlap_coverage']          # Cobertura com sobreposição
   
   # Visualização
   fig = pf_opt.plot(
       column='AAPL',           # Coluna específica para plotar
       dropna='head',           # Remove NaNs do início
       line_shape='hv',         # Formato da linha
       plot_rb_dates=True       # Mostra datas de rebalanceamento
   )
   fig.show()
   ```

6. **Simulação de Portfólio**:
   ```python
   # Simulação básica
   portfolio = pf_opt.simulate(
       close=close_prices,      # Preços de fechamento
       init_cash=100000,        # Capital inicial
       fees=0.001,             # Taxa de transação
       slippage=0.001,         # Slippage
       freq='1D'               # Frequência dos dados
   )
   
   # Análise da simulação
   stats = portfolio.stats()
   total_return = stats['total_return']         # Retorno total
   sharpe_ratio = stats['sharpe_ratio']         # Índice Sharpe
   max_drawdown = stats['max_drawdown']         # Drawdown máximo
   
   # Visualização da performance
   portfolio.plot().show()                      # Gráfico de performance
   portfolio.plot_drawdown().show()             # Gráfico de drawdown
   portfolio.plot_trades().show()               # Gráfico de trades
   ```

7. **Análise Estatística e Visualização**:
   ```python
   # Métricas disponíveis
   metrics = pf_opt.metrics
   
   # Estatísticas calculadas
   stats = pf_opt.stats()
   
   # Métricas principais
   start_idx = stats['start_index']          # Índice inicial
   end_idx = stats['end_index']              # Índice final
   duration = stats['total_duration']         # Duração total
   coverage = stats['coverage']              # Cobertura das alocações
   overlap = stats['overlap_coverage']       # Cobertura com sobreposição
   mean_alloc = stats['mean_allocation']     # Alocação média
   
   # Visualização das alocações
   fig = pf_opt.plot(
       column='AAPL',           # Coluna específica para plotar
       dropna='head',           # Remove NaNs do início
       line_shape='hv',         # Formato da linha
       plot_rb_dates=True       # Mostra datas de rebalanceamento
   )
   fig.show()
   ```

Esta implementação oferece uma solução completa para otimização de portfólio, permitindo tanto abordagens simples quanto estratégias avançadas de alocação de ativos. O sistema é altamente flexível e pode ser facilmente estendido para incluir novas estratégias de otimização e análise.

{{ ... }}
