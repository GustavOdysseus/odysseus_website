# Detalhes de Implementação do CrewAI

## 1. Sistema de Memória

### 1.1 Memória Contextual
```python
from crewai.memory.contextual import ContextualMemory
from crewai.memory.storage import RAGStorage

class TradingContextMemory(ContextualMemory):
    def __init__(self):
        super().__init__(
            storage=RAGStorage(
                vector_store="faiss",
                embedding_model="sentence-transformers/all-mpnet-base-v2"
            ),
            window_size=1000,  # Manter últimas 1000 interações
            retrieval_mode="semantic"  # semantic ou exact
        )
    
    def add_market_context(self, data):
        """Adiciona contexto de mercado à memória"""
        self.add({
            "type": "market_data",
            "timestamp": data["timestamp"],
            "content": data["analysis"],
            "metadata": {
                "symbols": data["symbols"],
                "timeframe": data["timeframe"]
            }
        })
```

### 1.2 Armazenamento RAG
```python
from crewai.memory.storage import RAGStorage
from crewai.memory.storage.base_rag_storage import BaseRAGStorage

class MarketRAGStorage(BaseRAGStorage):
    def __init__(self):
        super().__init__(
            collection_name="market_data",
            vector_store_config={
                "engine": "faiss",
                "dimension": 768,
                "metric": "cosine"
            }
        )
    
    def store_analysis(self, analysis_data):
        """Armazena análise de mercado"""
        self.store(
            texts=[analysis_data["content"]],
            metadatas=[{
                "timestamp": analysis_data["timestamp"],
                "analyst": analysis_data["analyst"],
                "confidence": analysis_data["confidence"]
            }]
        )
```

### 1.3 Armazenamento SQLite
```python
from crewai.memory.storage import LTMSQLiteStorage

class TradingHistoryStorage(LTMSQLiteStorage):
    def __init__(self):
        super().__init__(
            db_path="trading_history.db",
            tables={
                "trades": """
                    CREATE TABLE IF NOT EXISTS trades (
                        id TEXT PRIMARY KEY,
                        timestamp DATETIME,
                        symbol TEXT,
                        side TEXT,
                        quantity REAL,
                        price REAL,
                        strategy_id TEXT
                    )
                """,
                "analyses": """
                    CREATE TABLE IF NOT EXISTS analyses (
                        id TEXT PRIMARY KEY,
                        timestamp DATETIME,
                        type TEXT,
                        content TEXT,
                        confidence REAL
                    )
                """
            }
        )
```

## 2. Ferramentas de Agente

### 2.1 Ferramentas Base
```python
from crewai.tools.agent_tools import BaseAgentTools
from crewai.tools.structured_tool import StructuredTool
from pydantic import BaseModel

class MarketAnalysisParams(BaseModel):
    symbol: str
    timeframe: str
    indicators: List[str]

class TradingTools(BaseAgentTools):
    def __init__(self):
        super().__init__()
        self.tools = [
            self.technical_analysis,
            self.fundamental_analysis,
            self.risk_analysis
        ]
    
    @StructuredTool.from_schema(MarketAnalysisParams)
    def technical_analysis(self, params):
        """Executa análise técnica"""
        # Implementação
        pass
```

### 2.2 Delegação de Trabalho
```python
from crewai.tools.agent_tools import DelegateWorkTool

class TradingDelegator(DelegateWorkTool):
    def __init__(self):
        super().__init__(
            allowed_agents=["analyst", "risk_manager", "executor"],
            max_delegations=3
        )
    
    def delegate_analysis(self, task, to_agent):
        """Delega tarefa de análise"""
        return self.delegate(
            task=task,
            to_agent=to_agent,
            context={
                "priority": "high",
                "deadline": "5m"
            }
        )
```

### 2.3 Perguntas e Respostas
```python
from crewai.tools.agent_tools import AskQuestionTool

class MarketQATool(AskQuestionTool):
    def __init__(self):
        super().__init__(
            context_window=1000,
            max_tokens=150
        )
    
    def format_question(self, question):
        """Formata pergunta para incluir contexto de mercado"""
        return f"""
        Context: Current market conditions and recent analysis
        Question: {question}
        Requirements:
        - Consider market volatility
        - Include confidence level
        - Cite data sources
        """
```

## 3. Sistema de Fluxo

### 3.1 Configuração de Fluxo
```python
from crewai.flow import Flow
from crewai.flow.config import FlowConfig

class TradingFlow(Flow):
    def __init__(self):
        super().__init__(
            config=FlowConfig(
                max_parallel=5,
                timeout=300,
                retry_policy={
                    "max_attempts": 3,
                    "backoff": "exponential"
                }
            )
        )
    
    def setup_nodes(self):
        """Configura nós do fluxo de trading"""
        self.add_nodes([
            ("data", self.collect_data, {
                "timeout": 60,
                "retry": True
            }),
            ("analysis", self.analyze_market, {
                "requires": ["data"],
                "timeout": 120
            }),
            ("strategy", self.generate_strategy, {
                "requires": ["analysis"],
                "timeout": 60
            }),
            ("execution", self.execute_trades, {
                "requires": ["strategy"],
                "timeout": 30
            })
        ])
```

### 3.2 Visualização
```python
from crewai.flow import FlowVisualizer
from crewai.flow.html_template_handler import HTMLTemplateHandler

class TradingFlowVisualizer(FlowVisualizer):
    def __init__(self):
        super().__init__(
            template_handler=HTMLTemplateHandler(
                template_path="templates/trading_flow.html"
            )
        )
    
    def generate_report(self):
        """Gera relatório visual do fluxo"""
        return self.visualize(
            show_timing=True,
            show_dependencies=True,
            include_metrics=True
        )
```

## 4. Integração com VectorBT.pro

### 4.1 Ferramentas de Backtesting
```python
from crewai.tools import StructuredTool
import vectorbt as vbt

class BacktestTool(StructuredTool):
    name = "vectorbt_backtest"
    description = "Executa backtesting usando VectorBT.pro"
    
    def _execute(self, strategy_config):
        # Configuração do backtest
        portfolio = vbt.Portfolio.from_signals(
            close=strategy_config["data"],
            entries=strategy_config["entries"],
            exits=strategy_config["exits"],
            freq=strategy_config["timeframe"],
            init_cash=strategy_config["capital"]
        )
        
        # Análise de resultados
        return {
            "total_return": portfolio.total_return(),
            "sharpe_ratio": portfolio.sharpe_ratio(),
            "max_drawdown": portfolio.max_drawdown(),
            "trades": portfolio.trades.records_readable
        }
```

### 4.2 Otimização de Estratégias
```python
class StrategyOptimizer(StructuredTool):
    name = "optimize_strategy"
    description = "Otimiza parâmetros da estratégia"
    
    def _execute(self, config):
        # Grid search de parâmetros
        params_grid = {
            "window": range(10, 51, 5),
            "threshold": np.linspace(0.1, 0.5, 10)
        }
        
        # Otimização usando VectorBT.pro
        entries, exits = vbt.indicators.MA.run_combs(
            close=config["data"],
            window=params_grid["window"],
            thresh=params_grid["threshold"]
        )
        
        # Backtesting das combinações
        portfolio = vbt.Portfolio.from_signals(
            close=config["data"],
            entries=entries,
            exits=exits
        )
        
        # Seleção dos melhores parâmetros
        metrics = portfolio.metrics
        best_combo = metrics.idxmax()
        
        return {
            "best_params": best_combo,
            "performance": metrics.loc[best_combo]
        }
```

## 5. Monitoramento e Logging

### 5.1 Telemetria
```python
from crewai.telemetry import Telemetry

class TradingTelemetry(Telemetry):
    def __init__(self):
        super().__init__(
            namespace="trading",
            metrics=[
                "execution_time",
                "success_rate",
                "profit_loss",
                "drawdown"
            ]
        )
    
    def record_trade(self, trade_data):
        """Registra métricas de trade"""
        self.record_metric(
            name="trade_execution",
            value=trade_data["profit_loss"],
            tags={
                "symbol": trade_data["symbol"],
                "strategy": trade_data["strategy"],
                "side": trade_data["side"]
            }
        )
```

### 5.2 Logging Avançado
```python
from crewai.utilities.logger import Logger

class TradingLogger(Logger):
    def __init__(self):
        super().__init__(
            log_level="INFO",
            log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    def log_strategy_execution(self, strategy_data):
        """Log de execução de estratégia"""
        self.info(
            "Strategy execution",
            extra={
                "strategy_id": strategy_data["id"],
                "signals": len(strategy_data["signals"]),
                "confidence": strategy_data["confidence"],
                "execution_time": strategy_data["execution_time"]
            }
        )
```

## 6. Segurança e Validação

### 6.1 Validação de Inputs
```python
from pydantic import BaseModel, validator
from typing import List, Optional

class TradeRequest(BaseModel):
    symbol: str
    side: Literal["buy", "sell"]
    quantity: float
    price: Optional[float]
    stop_loss: Optional[float]
    take_profit: Optional[float]
    
    @validator("quantity")
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be positive")
        return v
    
    @validator("price")
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Price must be positive")
        return v
```

### 6.2 Rate Limiting
```python
from crewai.utilities import RateLimiter

class APIRateLimiter(RateLimiter):
    def __init__(self):
        super().__init__(
            max_requests=60,
            time_window=60  # 60 requests per minute
        )
    
    async def execute_api_call(self, func, *args, **kwargs):
        """Executa chamada API com rate limiting"""
        async with self:
            return await func(*args, **kwargs)
```
