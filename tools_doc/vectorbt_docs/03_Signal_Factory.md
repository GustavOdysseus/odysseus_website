# Signal Factory no VectorBT Pro

## Visão Geral
O SignalFactory é um componente fundamental do VectorBT Pro responsável pela geração e manipulação de sinais de trading de forma vetorizada. Este módulo oferece alta performance e flexibilidade para criação de estratégias complexas.

## Funcionalidades Principais

### 1. Geração de Sinais
```python
from vectorbtpro.signals.factory import SignalFactory

# Inicialização
factory = SignalFactory()

# Geração de sinais
signals = factory.generate_both(
    shape=(100,),  # Formato dos dados (períodos, ativos)
    entry_wait=1,  # Espera mínima entre sinais de entrada
    exit_wait=1    # Espera mínima entre sinais de saída
)
```

### 2. Tipos de Geração

#### 2.1 Sinais Completos (Entrada e Saída)
```python
signals = factory.generate_both(
    shape=(100,),
    entry_prob=0.1,    # Probabilidade de entrada
    exit_prob=0.1,     # Probabilidade de saída
    seed=42           # Semente para reprodutibilidade
)
```

#### 2.2 Apenas Entradas
```python
entries = factory.generate_entries(
    shape=(100,),
    entry_prob=0.1,
    seed=42
)
```

#### 2.3 Apenas Saídas
```python
exits = factory.generate_exits(
    shape=(100,),
    exit_prob=0.1,
    seed=42
)
```

### 3. Regras e Restrições

#### 3.1 Intervalos entre Sinais
- `entry_wait`: Períodos mínimos entre entradas
- `exit_wait`: Períodos mínimos entre saídas
```python
signals = factory.generate_both(
    shape=(100,),
    entry_wait=5,    # Mínimo 5 períodos entre entradas
    exit_wait=3      # Mínimo 3 períodos entre saídas
)
```

#### 3.2 Regras de Stop
```python
signals = factory.generate_both(
    shape=(100,),
    sl_stop=0.02,    # Stop Loss em 2%
    tp_stop=0.03,    # Take Profit em 3%
    trail_stop=0.01  # Trailing Stop em 1%
)
```

### 4. Otimizações e Performance

#### 4.1 Processamento Vetorizado
- Utiliza NumPy para operações vetorizadas
- Altamente eficiente para grandes conjuntos de dados
- Suporte a múltiplos ativos simultaneamente

#### 4.2 Cache
- Implementa sistema de cache para otimização
- Evita recálculos desnecessários
- Gerenciamento automático de memória

### 5. Validações e Segurança

#### 5.1 Validação de Parâmetros
- Verifica consistência dos parâmetros
- Previne configurações inválidas
- Mensagens de erro detalhadas

#### 5.2 Integridade dos Sinais
- Garante que não há sinais conflitantes
- Valida sequência lógica de entradas/saídas
- Previne sobreposição de posições

## Exemplos Práticos

### 1. Estratégia Básica
```python
import vectorbtpro as vbt
import numpy as np

# Inicializa factory
factory = SignalFactory()

# Gera sinais
signals = factory.generate_both(
    shape=(1000,),           # 1000 períodos
    entry_prob=0.1,          # 10% chance de entrada
    exit_prob=0.1,           # 10% chance de saída
    entry_wait=5,            # 5 períodos entre entradas
    exit_wait=5,             # 5 períodos entre saídas
    seed=42                  # Semente para reprodutibilidade
)

# Acessa sinais
print("Entradas:", signals.entries.sum())
print("Saídas:", signals.exits.sum())
```

### 2. Estratégia com Stops
```python
# Dados de exemplo
close = np.random.random(1000)

# Gera sinais com stops
signals = factory.generate_both(
    shape=(1000,),
    entry_prob=0.1,
    sl_stop=0.02,           # Stop Loss 2%
    tp_stop=0.03,           # Take Profit 3%
    trail_stop=0.01,        # Trailing Stop 1%
    close=close             # Preços para cálculo de stops
)
```

### 3. Múltiplos Ativos
```python
# Gera sinais para 3 ativos
signals = factory.generate_both(
    shape=(1000, 3),        # 1000 períodos, 3 ativos
    entry_prob=0.1,
    exit_prob=0.1,
    seed=42
)

# Análise por ativo
for col in range(3):
    print(f"Ativo {col}:")
    print(f"Entradas: {signals.entries[:, col].sum()}")
    print(f"Saídas: {signals.exits[:, col].sum()}")
```

## Integração com Backtesting

### 1. Portfolio
```python
# Cria portfolio
pf = vbt.Portfolio.from_signals(
    close=close,
    entries=signals.entries,
    exits=signals.exits,
    init_cash=100000,
    fees=0.001
)

# Análise
print(f"Retorno Total: {pf.total_return():.2%}")
print(f"Sharpe Ratio: {pf.sharpe_ratio():.2f}")
print(f"Drawdown Máximo: {pf.max_drawdown():.2%}")
```

## Melhores Práticas

1. **Reprodutibilidade**
   - Sempre defina uma semente (seed) para resultados consistentes
   - Documente os parâmetros usados

2. **Performance**
   - Use processamento vetorizado quando possível
   - Evite loops em Python puro
   - Aproveite o sistema de cache

3. **Validação**
   - Sempre valide os parâmetros antes de usar
   - Verifique a consistência dos sinais gerados
   - Monitore o uso de memória

4. **Gestão de Risco**
   - Implemente stops adequados
   - Valide a frequência dos sinais
   - Monitore a exposição ao risco

## Conclusão
O SignalFactory é uma ferramenta poderosa e flexível para geração de sinais de trading. Sua implementação vetorizada e otimizada permite criar estratégias complexas mantendo alta performance. A integração com o restante do ecossistema VectorBT Pro facilita a análise e backtesting das estratégias geradas.
