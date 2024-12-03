# Integração com Frameworks

## LangChain
[Ref: Módulo `langchain_integration`, arquivo: agentops/integrations/langchain.py]

### 1. Configuração
[Ref: Classe `LangChainIntegration`, L10-50]
```python
from agentops.integrations.langchain import setup_langchain_monitoring

# Configuração básica
setup_langchain_monitoring(
    api_key="seu-api-key",
    project_name="meu-projeto"
)
```

### 2. Callbacks
[Ref: Classe `LangChainCallbacks`, L60-100]
- Eventos de LLM [Ref: Método `on_llm_start`, L65-75]
- Eventos de Chain [Ref: Método `on_chain_start`, L80-90]
- Eventos de Tool [Ref: Método `on_tool_start`, L95-105]

### 3. Métricas Específicas
[Ref: Classe `LangChainMetrics`, L110-150]
- Chain Performance [Ref: Método `track_chain_performance`, L115-125]
- Tool Usage [Ref: Método `track_tool_usage`, L130-140]
- Memory Usage [Ref: Método `track_memory_usage`, L145-155]

## LlamaIndex
[Ref: Módulo `llamaindex_integration`, arquivo: agentops/integrations/llamaindex.py]

### 1. Configuração
[Ref: Classe `LlamaIndexIntegration`, L10-50]
```python
from agentops.integrations.llamaindex import setup_llamaindex_monitoring

# Configuração básica
setup_llamaindex_monitoring(
    api_key="seu-api-key",
    project_name="meu-projeto"
)
```

### 2. Callbacks
[Ref: Classe `LlamaIndexCallbacks`, L60-100]
- Eventos de Query [Ref: Método `on_query_start`, L65-75]
- Eventos de Index [Ref: Método `on_index_start`, L80-90]
- Eventos de Retrieval [Ref: Método `on_retrieval_start`, L95-105]

### 3. Métricas Específicas
[Ref: Classe `LlamaIndexMetrics`, L110-150]
- Query Performance [Ref: Método `track_query_performance`, L115-125]
- Index Stats [Ref: Método `track_index_stats`, L130-140]
- Retrieval Quality [Ref: Método `track_retrieval_quality`, L145-155]

## Haystack
[Ref: Módulo `haystack_integration`, arquivo: agentops/integrations/haystack.py]

### 1. Configuração
[Ref: Classe `HaystackIntegration`, L10-50]
```python
from agentops.integrations.haystack import setup_haystack_monitoring

# Configuração básica
setup_haystack_monitoring(
    api_key="seu-api-key",
    project_name="meu-projeto"
)
```

### 2. Callbacks
[Ref: Classe `HaystackCallbacks`, L60-100]
- Eventos de Pipeline [Ref: Método `on_pipeline_start`, L65-75]
- Eventos de Node [Ref: Método `on_node_start`, L80-90]
- Eventos de Reader [Ref: Método `on_reader_start`, L95-105]

### 3. Métricas Específicas
[Ref: Classe `HaystackMetrics`, L110-150]
- Pipeline Performance [Ref: Método `track_pipeline_performance`, L115-125]
- Node Stats [Ref: Método `track_node_stats`, L130-140]
- Reader Quality [Ref: Método `track_reader_quality`, L145-155]

## LiteLLM
[Ref: Módulo `litellm_integration`, arquivo: agentops/integrations/litellm.py]

### 1. Configuração
[Ref: Classe `LiteLLMIntegration`, L10-50]
```python
from agentops.integrations.litellm import setup_litellm_monitoring

# Configuração básica
setup_litellm_monitoring(
    api_key="seu-api-key",
    project_name="meu-projeto"
)
```

### 2. Callbacks
[Ref: Classe `LiteLLMCallbacks`, L60-100]
- Eventos de Completion [Ref: Método `on_completion_start`, L65-75]
- Eventos de Embedding [Ref: Método `on_embedding_start`, L80-90]
- Eventos de Router [Ref: Método `on_router_start`, L95-105]

### 3. Métricas Específicas
[Ref: Classe `LiteLLMMetrics`, L110-150]
- Completion Stats [Ref: Método `track_completion_stats`, L115-125]
- Router Performance [Ref: Método `track_router_performance`, L130-140]
- Cost Analysis [Ref: Método `track_cost_analysis`, L145-155]

## Troubleshooting de Integrações
[Ref: Módulo `integration_troubleshooting`, arquivo: agentops/troubleshooting.py]

### 1. Problemas Comuns
[Ref: Classe `IntegrationTroubleshooting`, L10-100]
- Configuração incorreta [Ref: Método `check_config`, L15-35]
- Conflitos de versão [Ref: Método `check_version_conflicts`, L40-60]
- Problemas de callback [Ref: Método `check_callbacks`, L65-85]

### 2. Soluções
[Ref: Classe `IntegrationSolutions`, L110-200]
- Validação de setup [Ref: Método `validate_setup`, L115-135]
- Debug de callbacks [Ref: Método `debug_callbacks`, L140-160]
- Otimização de performance [Ref: Método `optimize_performance`, L165-185]

## Anti-Patterns de Integração
[Ref: Módulo `integration_patterns`, arquivo: agentops/patterns.py]

### 1. Configuração
[Ref: Seção `ConfigurationPatterns`, L10-50]
- ❌ Credenciais hardcoded [Ref: L15-25]
- ✅ Uso de variáveis de ambiente [Ref: L30-40]
- ❌ Configuração duplicada [Ref: L45-55]

### 2. Callbacks
[Ref: Seção `CallbackPatterns`, L60-100]
- ❌ Callbacks bloqueantes [Ref: L65-75]
- ✅ Processamento assíncrono [Ref: L80-90]
- ❌ Ignorar erros de callback [Ref: L95-105]

### 3. Métricas
[Ref: Seção `MetricPatterns`, L110-150]
- ❌ Logging excessivo [Ref: L115-125]
- ✅ Amostragem inteligente [Ref: L130-140]
- ❌ Métricas redundantes [Ref: L145-155]
