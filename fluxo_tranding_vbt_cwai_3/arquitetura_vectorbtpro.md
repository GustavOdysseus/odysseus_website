# Arquitetura do VectorBT Pro

## 1. Estrutura Principal

### Módulo Core (vectorbtpro/)
- **Propósito**: Framework para análise vetorizada de dados financeiros
- **Componentes Principais**:
  - Base: Classes e utilidades fundamentais
  - Data: Gerenciamento de dados
  - Generic: Funcionalidades genéricas
  - Indicators: Indicadores técnicos
  - Portfolio: Gerenciamento de portfólio
  - Returns: Análise de retornos
  - Signals: Processamento de sinais
  - Utils: Utilitários diversos
  - OHLCV: Processamento de dados OHLCV
  - Labels: Sistema de rotulagem
  - PX: Extensões específicas
  - Records: Sistema de registros
  - Registries: Sistema de registros globais

### Sistema de Inicialização (__init__.py)
- **Propósito**: Configuração e inicialização do framework
- **Funcionalidades**:
  - Auto-importação inteligente de módulos
  - Configuração de warnings e mensagens
  - Gerenciamento de cache Python
  - Sistema flexível de importação ("star import")
  - Tipos de importação:
    - "all": Importa tudo
    - "vbt": Importa apenas o namespace VBT
    - "minimal": Importa apenas o essencial
    - "none": Não importa automaticamente

### Sistema de Base (base/)
- **Propósito**: Fornece funcionalidades fundamentais para manipulação de dados
- **Componentes**:
  - **Wrapping**: Sistema de encapsulamento de arrays NumPy
    - ArrayWrapper: Metadata para arrays NumPy
    - Wrapping: Classe base para objetos encapsulados
  - **Indexing**: Sistema avançado de indexação
    - Suporte a múltiplas dimensões
    - Indexação flexível
    - Seleção de grupos
  - **Grouping**: Sistema de agrupamento
    - Grouper: Gerenciamento de grupos
    - Operações por grupo
  - **Resampling**: Sistema de reamostragem
    - Resampler: Controle de frequência
    - Agregação temporal
  - **Chunking**: Processamento em chunks
  - **Combining**: Combinação de dados
  - **Reshaping**: Remodelagem de arrays
  - **Merging**: Fusão de dados
  - **Preparing**: Preparação de dados
  - **Decorators**: Decoradores utilitários

### Sistema de Indicadores (indicators/)
- **Propósito**: Criação e gerenciamento de indicadores técnicos
- **Componentes**:
  - **Factory**: Sistema de fábrica de indicadores
    - IndicatorFactory: Classe para construção de indicadores
    - IndicatorBase: Classe base para todos indicadores
  - **Custom**: Indicadores personalizados
    - Implementações específicas
    - Templates reutilizáveis
  - **Expressões**: Sistema de expressões
    - Avaliação dinâmica
    - Otimização de performance
  - **Integrações**:
    - TA-Lib: Biblioteca técnica
    - Pandas-TA: Extensão do Pandas
    - Custom: Indicadores próprios
  - **Enums**: Enumerações para indicadores
  - **Configs**: Configurações padrão

### Sistema de Portfólio (portfolio/)
- **Propósito**: Simulação e análise de portfólios
- **Componentes**:
  - **Base**: Framework principal
    - Portfolio: Classe base para simulação
    - Simulação de trades
    - Análise de performance
  - **Orders**: Sistema de ordens
    - Gerenciamento de ordens
    - Execução de trades
  - **Trades**: Sistema de trades
    - Registro de trades
    - Análise de posições
  - **PFOpt**: Otimização de portfólio
    - Algoritmos de otimização
    - Métricas de performance
  - **Logs**: Sistema de logging
    - Registro de eventos
    - Debugging
  - **Enums**: Enumerações
    - Tipos de ordens
    - Estados de trades
  - **Chunking**: Processamento em chunks
  - **Preparing**: Preparação de dados

### Sistema de Acessores (accessors.py)
- **Propósito**: Extensão das funcionalidades do pandas
- **Hierarquia**:
  ```
  BaseIDXAccessor
  BaseSR/DFAccessor
      -> GenericSR/DFAccessor
          -> SignalsSR/DFAccessor
          -> ReturnsSR/DFAccessor
          -> OHLCVDFAccessor
      -> PXSR/DFAccessor
  ```

## 2. Sistemas Principais

### Sistema de Wrapping
- **Propósito**: Encapsulamento e manipulação de arrays NumPy
- **Componentes**:
  - **ArrayWrapper**:
    - Armazena metadata (index, columns, shape)
    - Integração com Grouper
    - Imutável por design
    - Métodos group-aware
  - **Wrapping**:
    - Classe base para objetos encapsulados
    - Suporte a stacking (row/column)
    - Indexação avançada
    - Reamostragem
    - Iteração por grupos

### Sistema de Indicadores
- **Propósito**: Framework para criação e execução de indicadores técnicos
- **Componentes**:
  - **IndicatorFactory**:
    - Construção de indicadores
    - Configuração de parâmetros
    - Gerenciamento de cache
    - Otimização de performance
  - **IndicatorBase**:
    - Classe base para indicadores
    - Gerenciamento de inputs/outputs
    - Suporte a parâmetros múltiplos
    - Operações vetorizadas
  - **Pipeline de Execução**:
    - Preparação de parâmetros
    - Broadcasting de arrays
    - Execução otimizada
    - Cache de resultados

### Sistema de Portfólio
- **Propósito**: Framework para simulação e análise de portfólios
- **Componentes**:
  - **Simulação**:
    - Gerenciamento de cash
    - Execução de ordens
    - Tracking de posições
    - Cálculo de retornos
  - **Análise**:
    - Métricas de performance
    - Análise de drawdowns
    - Estatísticas de trades
    - Visualização de resultados
  - **Otimização**:
    - Otimização de pesos
    - Backtesting de estratégias
    - Análise de sensibilidade
    - Métricas de risco

### Sistema de Dados
- **Propósito**: Gerenciamento e manipulação de dados financeiros
- **Componentes**:
  - Leitores de dados
  - Processadores
  - Transformadores
  - Cache de dados

## 3. Sistemas de Suporte

### Sistema de Indexação
- **Propósito**: Gerenciamento avançado de índices
- **Características**:
  - Indexação multi-dimensional
  - Seleção flexível de colunas
  - Suporte a grupos
  - Indexação baseada em range

### Sistema de Agrupamento
- **Propósito**: Operações em grupos de dados
- **Funcionalidades**:
  - Agrupamento flexível
  - Operações por grupo
  - Integração com wrapping
  - Cache de grupos

### Sistema de Ordens
- **Propósito**: Gerenciamento de ordens de trading
- **Funcionalidades**:
  - Tipos de ordens
  - Execução de ordens
  - Validação
  - Logging

### Sistema de Trades
- **Propósito**: Registro e análise de trades
- **Funcionalidades**:
  - Registro de entradas/saídas
  - Cálculo de P&L
  - Análise de performance
  - Estatísticas de trades

### Sistema de Cache
- **Propósito**: Otimização de performance
- **Tipos**:
  - Cache de dados
  - Cache de computação
  - Cache de resultados

### Sistema de Configuração
- **Propósito**: Gerenciamento de configurações globais
- **Características**:
  - Configurações aninhadas
  - Chaves congeladas
  - Configurações flexíveis
- **Opções de Configuração**:
  - importing: Controle de importação automática
  - clear_pycache: Limpeza de cache Python
  - auto_import: Importação automática de módulos
  - star_import: Controle de importação global

### Sistema de Tipos
- **Propósito**: Tipagem estática e validação
- **Categorias**:
  - Tipos básicos
  - Arrays
  - Datetime
  - Indexação

## 4. Integrações

### Integrações Externas
- Pandas
- NumPy
- Plotly
- TA-Lib
- Pandas-TA
- Technical Analysis Library
- Custom Indicators

### Integrações de Dados
- Yahoo Finance
- Binance
- Alpha Vantage
- Polygon
- Outras fontes de dados

## 5. Sistema de Extensões

### Mecanismo de Plugins
- **Propósito**: Extensibilidade do framework
- **Tipos**:
  - Indicadores customizados
  - Fontes de dados
  - Estratégias de trading

### Sistema de Indicadores Customizados
- **Propósito**: Extensão do framework de indicadores
- **Tipos**:
  - Indicadores personalizados
  - Wrappers de bibliotecas
  - Expressões customizadas
- **Features**:
  - Hot-reloading
  - Cache inteligente
  - Otimização automática

## 6. Dependências e Requisitos

### Dependências Obrigatórias
- Python >= 3.7
- NumPy
- Pandas
- Numba
- Typing (para type hints)
- Importlib (para importação dinâmica)
- Pkgutil (para iteração de módulos)

### Dependências Opcionais
- Plotly (visualização)
- TA-Lib (indicadores técnicos)
- Outras bibliotecas específicas

## 7. Fluxo de Dados

### Pipeline de Portfólio
1. Inicialização
   - Configuração inicial
   - Definição de capital
   - Setup de posições
2. Simulação
   - Processamento de ordens
   - Execução de trades
   - Tracking de posições
3. Análise
   - Cálculo de retornos
   - Métricas de performance
   - Análise de risco
4. Otimização
   - Ajuste de parâmetros
   - Backtesting
   - Análise de resultados

### Pipeline de Indicadores
1. Definição
   - Parâmetros
   - Inputs/Outputs
   - Funções de cálculo
2. Preparação
   - Broadcasting
   - Validação
   - Cache setup
3. Execução
   - Vetorização
   - Otimização
   - Caching
4. Pós-processamento
   - Reshaping
   - Indexação
   - Agrupamento

### Pipeline Principal
1. Entrada de Dados
   - Wrapping de arrays NumPy
   - Configuração de metadata
2. Pré-processamento
   - Agrupamento
   - Indexação
   - Reshaping
3. Análise/Computação
   - Operações vetorizadas
   - Processamento por grupo
4. Pós-processamento
   - Reamostragem
   - Combinação
   - Merge
5. Visualização/Exportação

### Otimização de Performance
- Computação vetorizada
- Cache inteligente
- Processamento paralelo
- Compilação JIT
