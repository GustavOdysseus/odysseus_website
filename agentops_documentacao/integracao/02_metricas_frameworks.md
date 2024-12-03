# Métricas por Framework

O AgentOps coleta métricas específicas para cada framework de IA suportado, permitindo uma análise detalhada do desempenho e comportamento dos agentes.

## CrewAI

### Métricas de Agentes
- Tempo de execução por agente
- Taxa de sucesso por tarefa
- Padrões de delegação
- Uso de recursos por agente

### Métricas de Crew
- Tempo total de execução
- Eficiência da colaboração
- Distribuição de tarefas
- Custos por crew

### Métricas de Tarefas
- Tempo médio por tarefa
- Taxa de conclusão
- Dependências entre tarefas
- Gargalos identificados

## LangChain

### Métricas de Agentes
- Tempo de resposta do LLM
- Uso de ferramentas
- Precisão das respostas
- Tokens consumidos

### Métricas de Ferramentas
- Frequência de uso
- Tempo de execução
- Taxa de sucesso
- Erros comuns

### Métricas de Chains
- Performance da chain
- Uso de memória
- Custos por chain
- Latência entre etapas

## AutoGen

### Métricas de Conversas
- Duração das conversas
- Número de turnos
- Qualidade das respostas
- Padrões de interação

### Métricas de Agentes
- Tempo de processamento
- Uso de recursos
- Taxa de conclusão
- Eficiência da comunicação

### Métricas de Grupo
- Dinâmica de grupo
- Eficiência da colaboração
- Distribuição de tarefas
- Custos totais

## LlamaIndex

### Métricas de Indexação
- Tempo de indexação
- Uso de memória
- Qualidade dos embeddings
- Tamanho do índice

### Métricas de Consulta
- Tempo de resposta
- Precisão das respostas
- Uso de recursos
- Latência de recuperação

### Métricas de Documentos
- Taxa de processamento
- Qualidade da extração
- Uso de memória
- Erros de processamento

## Visualização de Métricas

### Dashboard
- Métricas em tempo real
- Histórico de execução
- Comparação entre frameworks
- Análise de tendências

### Alertas
- Limites configuráveis
- Notificações automáticas
- Detecção de anomalias
- Monitoramento proativo

### Relatórios
- Relatórios periódicos
- Análise comparativa
- Insights automáticos
- Recomendações de otimização

## Melhores Práticas

### 1. Coleta de Métricas
- Configure tags apropriadas
- Defina métricas customizadas
- Mantenha sessões organizadas
- Documente eventos importantes

### 2. Análise
- Compare diferentes configurações
- Identifique gargalos
- Monitore custos
- Avalie eficiência

### 3. Otimização
- Use insights para melhorias
- Ajuste configurações
- Otimize recursos
- Reduza custos

## Exemplos de Uso

### Monitoramento de Produção
```python
from agentops import Client

# Configuração com tags específicas
client = Client()
client.configure(api_key="sua_api_key")
client.start_session(
    tags=["production", "crewai"],
    custom_metrics={"cost_center": "team_a"}
)

# Seu código aqui

client.end_session(
    end_state="Success",
    metrics={"total_cost": cost, "tasks_completed": tasks}
)
```

### Análise de Performance
```python
from agentops import Client, Metrics

# Configuração para análise
client = Client()
client.configure(api_key="sua_api_key")

# Obtendo métricas
metrics = Metrics.get_session_metrics(
    session_id="sua_sessao",
    framework="langchain"
)

# Análise dos resultados
performance = metrics.analyze_performance()
costs = metrics.analyze_costs()
```

## Integração com CI/CD

### Pipeline de Testes
```yaml
name: AgentOps Monitoring

on: [push, pull_request]

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup AgentOps
        run: |
          pip install agentops
          agentops configure
      - name: Run Tests
        run: |
          python tests/run_with_monitoring.py
```

### Monitoramento Contínuo
```python
from agentops import Client

client = Client()
client.configure(api_key="sua_api_key")

# Configuração para CI/CD
client.start_session(
    tags=["ci_cd", "automated_tests"],
    environment="testing"
)

try:
    # Seus testes aqui
    pass
except Exception as e:
    client.end_session(
        end_state="Error",
        end_state_reason=str(e)
    )
    raise e
else:
    client.end_session(
        end_state="Success",
        end_state_reason="All tests passed"
    )
```
