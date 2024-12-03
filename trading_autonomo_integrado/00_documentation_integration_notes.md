# Notas de Integração da Documentação

## Estrutura Atual

### 1. Arquitetura e Sistema Base (01-07)
- **01_system_architecture.md**: Visão geral da arquitetura
- **02_research_system.md**: Sistema de pesquisa
- **03_analysis_system.md**: Sistema de análise
- **04_knowledge_base.md**: Base de conhecimento
- **05_maestro_pipeline.md**: Pipeline principal
- **06_implementation_guide.md**: Guia de implementação
- **07_code_quality_pipeline.md**: Pipeline de qualidade de código

### 2. CrewAI (08-12, 25-30)
- **08-12**: Análise inicial do CrewAI
- **25-30**: Análise detalhada e técnica do CrewAI

### 3. VectorBT Pro (13-24)
- **13-24**: Análise completa do VectorBT Pro

### 4. Sistema Dinâmico
- **dynamic_trading_system_flow.md**: Fluxo do sistema de trading

## Análise Detalhada dos Arquivos

### 1. Arquitetura do Sistema (01_system_architecture.md)
- **Pontos Principais**:
  - Estrutura modular com 6 componentes principais
  - Pipeline Maestro como orquestrador central
  - Fluxo de dados bem definido em diagrama mermaid
  - Requisitos técnicos específicos

- **Oportunidades de Integração**:
  - Expandir diagrama de fluxo com subcomponentes
  - Detalhar interfaces entre módulos
  - Adicionar exemplos de configuração
  - Incluir métricas de performance

### 2. Sistema de Pesquisa (02_research_system.md)
- **Pontos Principais**:
  - Foco em pesquisa científica de trading
  - Integração com arXiv
  - Sistema de extração de modelos matemáticos
  - API bem estruturada

- **Oportunidades de Integração**:
  - Conectar com sistema de análise
  - Expandir documentação de modelos
  - Adicionar exemplos práticos
  - Incluir métricas de avaliação

### 3. Sistema de Análise (03_analysis_system.md)
- **Pontos Principais**:
  - Análise técnica, fundamental e estatística
  - Integração com VectorBT.pro
  - Modelos de ML avançados
  - Pipeline de análise completo

- **Oportunidades de Integração**:
  - Conectar com sistema de pesquisa
  - Expandir exemplos de modelos
  - Adicionar casos de uso
  - Incluir benchmarks

### 4. Base de Conhecimento (04_knowledge_base.md)
- **Pontos Principais**:
  - Sistema central de armazenamento
  - Modelos de dados bem definidos
  - Sistema de busca semântica
  - Gerenciamento de versões

- **Oportunidades de Integração**:
  - Expandir schemas de dados
  - Adicionar exemplos de queries
  - Documentar padrões de uso
  - Incluir métricas de performance

### 5. Pipeline Maestro (05_maestro_pipeline.md)
- **Pontos Principais**:
  - Orquestração central do sistema
  - Fluxos de trabalho detalhados
  - Sistema de recuperação robusto
  - Configuração via Docker

- **Oportunidades de Integração**:
  - Expandir exemplos de configuração
  - Documentar cenários de falha
  - Adicionar diagramas de fluxo
  - Incluir métricas operacionais

### 6. Guia de Implementação (06_implementation_guide.md)
- **Pontos Principais**:
  - Ordem de implementação detalhada
  - Estrutura de diretórios clara
  - Dependências e configurações
  - Práticas de desenvolvimento

- **Oportunidades de Integração**:
  - Expandir exemplos de configuração
  - Adicionar troubleshooting
  - Incluir casos de uso
  - Documentar best practices

### 7. Pipeline de Qualidade (07_code_quality_pipeline.md)
- **Pontos Principais**:
  - Sistema de validação de código
  - Testes automáticos
  - Correção automática
  - Integração CI/CD

- **Oportunidades de Integração**:
  - Expandir exemplos de configuração
  - Adicionar casos de erro comuns
  - Incluir métricas de qualidade
  - Documentar processos de review

## VectorBT Pro Analysis

### System Architecture
1. Core Components
   - Base structures
   - Data management
   - Generic utilities
   - Technical indicators
   - Labeling system
   - OHLCV processing
   - Portfolio management
   - Records system
   - Returns analysis
   - Signal processing

2. Data Structures
   - Array wrapper
   - Column grouper
   - Index functions
   - Reshape functions

### Technical Analysis
1. Custom Indicators
   - Indicator factory
   - Vectorized implementation
   - Caching system
   - Parameter management

2. Indicator Pipeline
   - Trend indicators
   - Momentum indicators
   - Volatility indicators
   - Custom combinations

### Portfolio System
1. Position Management
   - Signal-based entries/exits
   - Position sizing
   - Fee handling
   - Slippage modeling

2. Portfolio Optimization
   - Objective functions
   - Constraints handling
   - Weight optimization
   - Performance metrics

### Backtesting System
1. Configuration
   - Parameter grid
   - Strategy setup
   - Execution control
   - Progress tracking

2. Results Analysis
   - Return analysis
   - Risk metrics
   - Trade statistics
   - Performance evaluation

### Real-Time Integration
1. Streaming Processing
   - Tick handling
   - Data updates
   - Indicator recalculation
   - Signal generation

2. Order Management
   - Order placement
   - Order monitoring
   - Trade tracking
   - Position updates

### System Optimization
1. Parallelization
   - Multi-core processing
   - Task distribution
   - Progress tracking
   - Result aggregation

2. Memory Management
   - Cache configuration
   - Memory optimization
   - Cleanup policies
   - Usage monitoring

## VectorBT Pro Labels System

### Core Components
1. Market Labeler
   - Trend labeling
   - Volatility labeling
   - Pattern detection
   - Label validation

2. Pattern Detector
   - Candlestick patterns
   - Chart patterns
   - Technical patterns
   - Pattern validation

### Signal Generation
1. Trend Signals
   - Entry conditions
   - Exit conditions
   - Signal validation
   - Performance tracking

2. Pattern Signals
   - Pattern recognition
   - Signal generation
   - Entry/exit rules
   - Signal filtering

### ML Integration
1. Feature Engineering
   - Technical features
   - Pattern features
   - Label features
   - Feature validation

2. Model Training
   - Data preparation
   - Model selection
   - Training process
   - Performance evaluation

### Analysis Tools
1. Label Analysis
   - Label statistics
   - Transition analysis
   - Duration analysis
   - Quality metrics

2. Pattern Analysis
   - Pattern detection
   - Validation tools
   - Performance metrics
   - Optimization tools

### Best Practices
1. Development
   - Label validation
   - Pattern testing
   - Documentation
   - Code quality

2. Production
   - Quality monitoring
   - Rule updates
   - Signal validation
   - Documentation

## VectorBT Pro Live Execution System

### Core Components
1. Strategy Executor
   - Real-time execution
   - Order management
   - Position tracking
   - Error handling

2. Live Data Manager
   - Market data feeds
   - Data caching
   - Feed management
   - Real-time updates

### Risk Management
1. Live Risk Manager
   - Position sizing
   - Risk limits
   - Exposure control
   - Drawdown monitoring

2. Performance Monitor
   - Real-time metrics
   - Performance tracking
   - Report generation
   - History logging

### Advanced Features
1. Alert System
   - Risk monitoring
   - Market conditions
   - Position alerts
   - System status

2. Error Handling
   - Retry logic
   - Error recovery
   - System failover
   - State management

### Best Practices
1. Execution
   - Latency monitoring
   - Order validation
   - Event logging
   - State tracking

2. Risk Control
   - Exposure limits
   - Stop management
   - Position validation
   - Real-time monitoring

### Production Guidelines
1. Development
   - Extensive testing
   - Failure simulation
   - Process documentation
   - System redundancy

2. Maintenance
   - Performance review
   - Process optimization
   - System updates
   - Log management

## VectorBT Pro Portfolio System

### Core Components
1. Portfolio Management
   - Portfolio creation
   - Performance analysis
   - Position tracking
   - Order management

2. Portfolio Optimization
   - Weight optimization
   - Sharpe ratio maximization
   - Variance minimization
   - Constraint handling

### Risk Analysis
1. Risk Metrics
   - Volatility calculation
   - VaR and CVaR
   - Beta and Alpha
   - Drawdown analysis

2. Trade Analysis
   - Trade statistics
   - PnL tracking
   - Win rate calculation
   - Profit factor analysis

### Advanced Features
1. Portfolio Simulation
   - Monte Carlo simulation
   - Return modeling
   - Signal generation
   - Performance evaluation

2. Order Management
   - Trade execution
   - Position sizing
   - Cost analysis
   - Slippage modeling

### Best Practices
1. Portfolio Management
   - Diversification
   - Rebalancing
   - Risk control
   - Monitoring

2. Performance Analysis
   - Multiple metrics
   - Robustness testing
   - Cross validation
   - Sensitivity analysis

### Production Guidelines
1. Execution
   - Cost control
   - Liquidity management
   - Risk monitoring
   - Real-time tracking

2. Maintenance
   - Strategy review
   - Data updates
   - Code optimization
   - Log management

## VectorBT Pro Strategy System

### Core Components
1. Signal Generation
   - Crossover signals
   - Breakout detection
   - Custom indicators
   - Signal validation

2. Strategy Optimization
   - Parameter grid search
   - Performance metrics
   - Cross validation
   - Cost analysis

### Risk Management
1. Position Sizing
   - Risk-based sizing
   - Stop loss calculation
   - Position tracking
   - Equity management

2. Risk Controls
   - Stop loss systems
   - Take profit rules
   - Exposure limits
   - Drawdown controls

### Strategy Types
1. Momentum Strategies
   - Trend following
   - Breakout systems
   - Volatility trading
   - Parameter optimization

2. Mean Reversion
   - Statistical arbitrage
   - Bollinger Bands
   - RSI strategies
   - Range trading

### Real-Time Integration
1. Strategy Execution
   - Live data handling
   - Order management
   - Position tracking
   - Performance monitoring

2. Market Integration
   - Broker APIs
   - Data streams
   - Order routing
   - Status monitoring

### Best Practices
1. Development
   - Vectorized code
   - Risk management
   - Testing protocols
   - Documentation

2. Production
   - Performance monitoring
   - Alert systems
   - Backup procedures
   - Process documentation

## VectorBT Pro Extended Data Module

### Core Infrastructure
1. Data Management
   - Unified interface
   - Cache system
   - Processing pipeline
   - Source management

2. Data Adapters
   - Binance integration
   - SQL databases
   - DuckDB optimization
   - Custom adapters

### Data Processing
1. Pipeline System
   - Data cleaning
   - Resampling
   - Returns calculation
   - Validation

2. Persistence System
   - HDF5 storage
   - Parquet format
   - Compression
   - Versioning

### Advanced Features
1. Update System
   - Periodic updates
   - Data merging
   - Retry logic
   - Scheduling

2. Performance
   - Optimized formats
   - Efficient caching
   - Chunk processing
   - Resource management

### Best Practices
1. Data Quality
   - Validation
   - Backup strategy
   - Version control
   - Documentation

2. Production
   - Latency monitoring
   - Redundancy
   - Cost management
   - Resource optimization

### Integration
1. Market APIs
   - Real-time data
   - Historical data
   - Order execution
   - Market status

2. Storage Systems
   - Databases
   - File systems
   - Cloud services
   - Cache layers

## VectorBT Pro Indicators Module

### Core Components
1. Indicator Factory
   - Base factory system
   - Custom indicators
   - Expression system
   - Parameter handling

2. Built-in Indicators
   - Bollinger Bands
   - MACD
   - RSI
   - Custom implementations

### Advanced Systems
1. Signal Detection
   - Pattern recognition
   - Threshold detection
   - Signal analysis
   - Performance metrics

2. Statistical Analysis
   - OLS regression
   - Trend analysis
   - Pivot points
   - Support/resistance

3. Vectorized Operations
   - Rolling windows
   - Parallel processing
   - Memory optimization
   - Cache management

### Performance Features
1. Optimization
   - Vectorized calculations
   - Parallel execution
   - Memory efficiency
   - Cache strategies

2. Best Practices
   - Factory patterns
   - Documentation
   - Validation
   - Compatibility

### Implementation Details
1. Technical Analysis
   - Price indicators
   - Volume indicators
   - Momentum studies
   - Volatility measures

2. Custom Development
   - Factory extension
   - Parameter handling
   - Signal generation
   - Performance tuning

## VectorBT Pro Portfolio Module

### Core Components
1. Portfolio Management
   - Portfolio simulation
   - Order management
   - Trade analysis
   - Performance metrics

2. Order System
   - Order creation
   - Execution handling
   - Context management
   - Trade tracking

### Advanced Features
1. Portfolio Optimization
   - Sharpe optimization
   - Risk parity
   - Custom objectives
   - Constraint handling

2. Trade Analysis
   - Performance metrics
   - Trade statistics
   - Win/loss analysis
   - Risk assessment

3. Data Preparation
   - Price data handling
   - Returns calculation
   - Weight normalization
   - Data validation

### System Features
1. Logging System
   - Trade logging
   - Performance tracking
   - Error handling
   - Report generation

2. Chunking System
   - Large data handling
   - Memory optimization
   - Parallel processing
   - Result merging

### Best Practices
1. Risk Management
   - Dynamic stops
   - Exposure control
   - Drawdown management
   - Diversification

2. Performance
   - Vectorized operations
   - Caching strategies
   - Resource monitoring
   - Optimization techniques

### Implementation
1. Development
   - Testing protocols
   - Code standards
   - Documentation
   - Validation

2. Production
   - Resource management
   - Failsafe systems
   - Backup strategies
   - Monitoring tools

## VectorBT Pro Backtesting System

### Core Components
1. Backtest Engine
   - Strategy execution
   - Performance tracking
   - Results analysis
   - Report generation

2. Performance Analysis
   - Metric calculation
   - Return analysis
   - Risk assessment
   - Trade statistics

### Advanced Features
1. Parameter Optimization
   - Grid search
   - Walk-forward analysis
   - Cross validation
   - Metric optimization

2. Robustness Testing
   - Monte Carlo simulation
   - Data shuffling
   - Statistical validation
   - Sensitivity analysis

### Best Practices
1. Backtesting
   - Historical data quality
   - Transaction costs
   - Slippage modeling
   - Result validation

2. Optimization
   - Overfitting prevention
   - Multiple metrics
   - Cross validation
   - Robustness checks

### Production Guidelines
1. Development
   - Comprehensive testing
   - Documentation
   - Data validation
   - Code modularity

2. Maintenance
   - Strategy review
   - Data updates
   - Code optimization
   - Log management

## CrewAI Integration Details

### Agent Architecture
1. Development Agent
   - Code execution capabilities
   - File management
   - Docker environment control
   - Project structure setup

2. Research Agent
   - Scientific paper search
   - Content analysis
   - Model extraction
   - Results compilation

### Core Components
1. Safe Code Execution
   - Docker containerization
   - Resource allocation
   - Code validation
   - Security checks

2. File Management System
   - Directory structure creation
   - File versioning
   - Git integration
   - Automated commits

3. Task Orchestration
   - Development pipeline
   - Resource management
   - Task validation
   - Result tracking

4. Monitoring & Security
   - Execution logging
   - Performance monitoring
   - Access control
   - Environment isolation

## CrewAI Core Capabilities

### Architecture Components
1. Core Components
   - Agent tracking system (AgentOps)
   - Contextual memory management
   - Cache system
   - LLM integration
   - Custom prompt templates
   - Monitoring callbacks

2. Knowledge System
   - Custom embeddings
   - Multiple knowledge sources
   - Flexible storage system
   - Processing utilities
   - Embedder integrations

### Trading-Specific Features
1. Market Data Integration
   - DataFrame source integration
   - Market data knowledge management
   - Custom metadata handling

2. Strategy Execution
   - Structured trading tools
   - Order execution system
   - Market analysis agents
   - Strategy optimization

3. VectorBT.pro Integration
   - Backtesting tools
   - Strategy optimization
   - Performance analysis
   - Portfolio management

### Security & Best Practices
1. Secure Execution
   - Docker isolation
   - Input validation
   - Rate limiting
   - Configurable timeouts

2. Resource Management
   - Credential management
   - Resource monitoring
   - Performance tracking
   - Caching strategies

## CrewAI Native Resources

### Agent System
1. Agent Executor
   - Maximum iterations control
   - Callback management
   - Error handling
   - Integrated logging
   - RPM limits
   - Context validation

2. Agent Builder
   - Role and goal system
   - LLM integration
   - Tool management
   - Memory control
   - Prompt formatting

### Knowledge System
1. Knowledge Sources
   - CSV support
   - Excel support
   - JSON support
   - PDF support
   - Text file support
   - XML support
   - MDX support
   - DOCX support

2. Embedding System
   - Custom embeddings
   - Multiple model integration
   - Embedding cache

### Memory System
1. Memory Types
   - Contextual memory
   - Entity memory
   - Long-term memory
   - Short-term memory
   - User memory

2. Storage Options
   - Multiple backends
   - Indexing support
   - Compression
   - Efficient retrieval

### Flow System
1. Flow Management
   - Pipeline definition
   - Execution control
   - Dependency management
   - Parallelism support

2. Flow Visualization
   - Diagram generation
   - HTML templates
   - Custom legends
   - Visualization utilities

### Trading Implementation
1. Market Data Sources
   - Price data integration
   - Fundamentals data
   - Custom metadata

2. Trading Memory
   - Redis storage
   - Trade recording
   - Configurable TTL

3. Trading Flow
   - Parallel execution
   - Timeout configuration
   - Pipeline setup
   - Node dependencies

4. Specialized Agents
   - Market analysis
   - Technical analysis
   - Fundamental analysis
   - Sentiment analysis

## CrewAI Implementation Details

### Memory System Implementation
1. Contextual Memory
   - RAG storage integration
   - FAISS vector store
   - Semantic retrieval
   - Market context management

2. Storage Systems
   - RAG storage for analysis
   - SQLite for trading history
   - Custom metadata handling
   - Efficient retrieval

### Agent Tools Implementation
1. Base Tools
   - Technical analysis
   - Fundamental analysis
   - Risk analysis
   - Structured parameters

2. Work Delegation
   - Agent role management
   - Task prioritization
   - Deadline handling
   - Context propagation

3. Q&A System
   - Context window management
   - Market-specific formatting
   - Confidence tracking
   - Source citation

### Flow System Implementation
1. Flow Configuration
   - Parallel execution
   - Timeout handling
   - Retry policies
   - Node dependencies

2. Flow Visualization
   - HTML templates
   - Timing analysis
   - Dependency visualization
   - Metric tracking

### VectorBT.pro Integration
1. Backtesting Tools
   - Portfolio simulation
   - Signal generation
   - Performance metrics
   - Trade analysis

2. Strategy Optimization
   - Parameter grid search
   - Performance evaluation
   - Best parameter selection
   - Metric comparison

### Monitoring & Security
1. Telemetry System
   - Custom metrics
   - Trade tracking
   - Performance monitoring
   - Tagged data

2. Advanced Logging
   - Strategy execution logs
   - Performance tracking
   - Error handling
   - Structured data

3. Security Features
   - Input validation
   - Rate limiting
   - API protection
   - Request windowing

## CrewAI Tools Analysis

### Data Processing Tools
1. Search Tools
   - CSV search
   - JSON search
   - PDF search
   - Text search
   - XML search
   - MDX search
   - DOCX search

2. Database Tools
   - MySQL search
   - PostgreSQL search
   - NL2SQL conversion

### Web Tools
1. Web Scraping
   - Basic website scraping
   - Selenium integration
   - Web crawler
   - FireCrawl tools
   - Scrapfly integration
   - Serply API

2. Search Tools
   - Website search
   - GitHub search
   - Serper.dev integration
   - YouTube tools

### AI & ML Tools
1. Language Processing
   - LlamaIndex integration
   - RAG implementation
   - Document processing
   - Semantic search

2. Computer Vision
   - DALL-E integration
   - Image processing

### Development Tools
1. Code Tools
   - Code interpretation
   - Documentation search
   - File management
   - Directory handling

2. Adapters
   - Embedchain integration
   - PDF processing
   - LanceDB integration

### Implementation Examples
1. Market Data Processing
   - CSV data handling
   - JSON processing
   - Vector database storage
   - Data integration

2. Financial Web Scraping
   - Price data extraction
   - News aggregation
   - Market analysis
   - Data validation

3. Document Analysis
   - PDF data extraction
   - RAG processing
   - Embedding storage
   - Financial analysis

4. API Integration
   - GitHub integration
   - Market research
   - News analysis
   - Data aggregation

## Padrões Identificados

### 1. Estrutura de Documentação
- Todos os arquivos seguem estrutura similar:
  1. Visão Geral
  2. Componentes Principais
  3. Detalhamento Técnico
  4. Implementação
  5. APIs/Interfaces

### 2. Elementos Comuns
- Diagramas de fluxo
- Exemplos de código
- Estruturas de dados
- Endpoints de API

### 3. Interdependências
- Sistema de Pesquisa → Base de Conhecimento
- Sistema de Análise → VectorBT Pro
- Pipeline Maestro → Todos os componentes

## Proposta de Melhorias

### 1. Padronização
- Usar mesma estrutura em todos os documentos
- Padronizar exemplos de código
- Unificar terminologia
- Manter consistência visual

### 2. Integração
- Criar links entre documentos relacionados
- Adicionar referências cruzadas
- Manter rastreabilidade
- Documentar dependências

### 3. Exemplos e Casos de Uso
- Adicionar exemplos práticos
- Incluir casos de uso reais
- Fornecer snippets de código
- Documentar melhores práticas

## Próximos Passos

1. **Análise Completa**
   - Continuar leitura dos arquivos
   - Identificar mais padrões
   - Mapear todas as dependências
   - Documentar pontos de integração

2. **Plano de Reorganização**
   - Definir nova estrutura
   - Criar templates
   - Estabelecer padrões
   - Planejar migração

3. **Implementação**
   - Reorganizar conteúdo
   - Adicionar exemplos
   - Criar links
   - Validar mudanças

## Observações Importantes

1. **Manter Rastreabilidade**
   - Preservar histórico
   - Documentar mudanças
   - Manter referências

2. **Garantir Consistência**
   - Formato
   - Terminologia
   - Estilo

3. **Facilitar Manutenção**
   - Modularidade
   - Versionamento
   - Automação

## Recomendações

1. **Imediatas**
   - Criar índice global
   - Padronizar formato
   - Remover redundâncias

2. **Curto Prazo**
   - Reorganizar estrutura
   - Adicionar exemplos
   - Melhorar navegação

3. **Médio Prazo**
   - Implementar versionamento
   - Adicionar automação
   - Expandir tutoriais

4. **Longo Prazo**
   - Criar sistema de feedback
   - Implementar CI/CD
   - Desenvolver portal

## Padrões Identificados

### 1. Estrutura de Código
- Classes bem definidas
- Tipagem forte
- Documentação inline
- Tratamento de erros

### 2. Padrões de Implementação
- Desenvolvimento em fases
- Testes automatizados
- CI/CD integrado
- Monitoramento contínuo

### 3. Práticas de Qualidade
- Code review
- Testes automáticos
- Métricas de qualidade
- Documentação automática

## Recomendações de Integração

### 1. Documentação Técnica
- **Estrutura de Código**:
  ```python
  class CoreComponents:
      """Componentes principais do sistema"""
      - Research
      - Analysis
      - Execution
      - Monitoring
  ```

- **Padrões de Implementação**:
  ```python
  class ImplementationPatterns:
      """Padrões de implementação"""
      - Development
      - Testing
      - Deployment
      - Maintenance
  ```

### 2. Fluxos de Trabalho
- **Pipeline de Desenvolvimento**:
  ```mermaid
  graph TD
      A[Código] --> B[Validação]
      B --> C[Testes]
      C --> D[Review]
      D --> E[Deploy]
  ```

- **Pipeline de Qualidade**:
  ```mermaid
  graph TD
      A[Análise] --> B[Correção]
      B --> C[Testes]
      C --> D[Métricas]
      D --> E[Relatório]
  ```

### 3. Monitoramento e Métricas
- **Métricas de Qualidade**:
  - Complexidade de código
  - Cobertura de testes
  - Taxa de bugs
  - Tempo de resolução

- **Alertas**:
  - Falhas de build
  - Testes quebrados
  - Métricas abaixo do limite
  - Erros de deploy

## Proposta de Nova Estrutura

### 1. Documentação Core
- **Arquitetura**
  - Componentes
  - Fluxos
  - Interfaces
  - Requisitos

- **Implementação**
  - Setup
  - Configuração
  - Deployment
  - Manutenção

### 2. Documentação Técnica
- **Desenvolvimento**
  - Padrões
  - Práticas
  - Ferramentas
  - Processos

- **Qualidade**
  - Validação
  - Testes
  - Métricas
  - Reviews

### 3. Guias Operacionais
- **DevOps**
  - CI/CD
  - Monitoring
  - Alerting
  - Maintenance

- **Troubleshooting**
  - Problemas comuns
  - Soluções
  - Prevenção
  - Recuperação

```
