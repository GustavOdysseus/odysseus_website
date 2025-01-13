# Tool Usage Events - Documentação Detalhada

## Visão Geral
O arquivo `tool_usage_events.py` define as estruturas de eventos relacionados ao uso de ferramentas no CrewAI. Este módulo implementa um sistema de eventos que permite rastrear e monitorar a execução de ferramentas pelos agentes.

## Estruturas de Eventos

### 1. Classe Base: ToolUsageEvent

```python
class ToolUsageEvent(BaseModel):
    agent_key: str
    agent_role: str
    tool_name: str
    tool_args: Dict[str, Any]
    tool_class: str
    run_attempts: int | None = None
    delegations: int | None = None
```

#### Atributos
1. **agent_key** (str)
   - Identificador único do agente
   - Usado para rastreamento
   - Permite correlação de eventos

2. **agent_role** (str)
   - Papel/função do agente
   - Define o contexto de uso
   - Auxilia na análise de comportamento

3. **tool_name** (str)
   - Nome da ferramenta utilizada
   - Identificador da funcionalidade
   - Referência para análise

4. **tool_args** (Dict[str, Any])
   - Argumentos passados para a ferramenta
   - Parâmetros de execução
   - Contexto de uso

5. **tool_class** (str)
   - Classe da ferramenta
   - Tipo de operação
   - Categoria de funcionalidade

6. **run_attempts** (int | None)
   - Número de tentativas de execução
   - Opcional
   - Métrica de confiabilidade

7. **delegations** (int | None)
   - Contagem de delegações
   - Opcional
   - Métricas de colaboração

### 2. Classe ToolUsageFinished

```python
class ToolUsageFinished(ToolUsageEvent):
    started_at: datetime
    finished_at: datetime
    from_cache: bool = False
```

#### Características Adicionais
- **started_at**: Timestamp de início
- **finished_at**: Timestamp de conclusão
- **from_cache**: Indicador de uso de cache

#### Uso
- Rastreamento de tempo de execução
- Análise de performance
- Métricas de cache

### 3. Classe ToolUsageError

```python
class ToolUsageError(ToolUsageEvent):
    error: str
```

#### Características Adicionais
- **error**: Descrição do erro ocorrido

#### Uso
- Registro de falhas
- Diagnóstico de problemas
- Análise de confiabilidade

## Casos de Uso

### 1. Monitoramento de Execução
```python
# Registro de início de execução
event = ToolUsageEvent(
    agent_key="agent_123",
    agent_role="data_analyzer",
    tool_name="data_processor",
    tool_args={"file": "data.csv"},
    tool_class="DataProcessingTool",
    run_attempts=1
)

# Registro de conclusão
finished_event = ToolUsageFinished(
    agent_key="agent_123",
    agent_role="data_analyzer",
    tool_name="data_processor",
    tool_args={"file": "data.csv"},
    tool_class="DataProcessingTool",
    started_at=datetime.now(),
    finished_at=datetime.now(),
    from_cache=False
)
```

### 2. Registro de Erros
```python
# Registro de erro na execução
error_event = ToolUsageError(
    agent_key="agent_123",
    agent_role="data_analyzer",
    tool_name="data_processor",
    tool_args={"file": "data.csv"},
    tool_class="DataProcessingTool",
    error="File not found: data.csv"
)
```

## Integrações

### 1. Sistema de Telemetria
- Coleta de métricas
- Análise de performance
- Monitoramento de uso

### 2. Sistema de Logging
- Registro de eventos
- Diagnóstico de problemas
- Auditoria de uso

### 3. Análise de Performance
- Tempos de execução
- Taxas de erro
- Eficiência de cache

## Melhores Práticas

### 1. Registro de Eventos
- Capture todos os eventos relevantes
- Inclua contexto suficiente
- Mantenha consistência nos dados

### 2. Tratamento de Erros
- Registre erros detalhadamente
- Inclua stack traces quando relevante
- Categorize tipos de erro

### 3. Análise de Dados
- Monitore padrões de uso
- Identifique gargalos
- Otimize baseado em métricas

## Considerações Técnicas

### 1. Performance
- Eventos são leves e eficientes
- Validação via Pydantic
- Serialização otimizada

### 2. Extensibilidade
- Fácil adição de novos eventos
- Campos flexíveis
- Herança clara

### 3. Integração
- Compatível com sistemas de logging
- Suporte a telemetria
- Exportação de dados

## Exemplos de Implementação

### 1. Sistema de Monitoramento
```python
class ToolMonitor:
    def record_event(self, event: ToolUsageEvent):
        if isinstance(event, ToolUsageFinished):
            self.log_execution_time(event)
        elif isinstance(event, ToolUsageError):
            self.alert_error(event)
        
    def log_execution_time(self, event: ToolUsageFinished):
        duration = event.finished_at - event.started_at
        print(f"Tool {event.tool_name} executed in {duration}")
        
    def alert_error(self, event: ToolUsageError):
        print(f"Error in {event.tool_name}: {event.error}")
```

### 2. Análise de Performance
```python
class PerformanceAnalyzer:
    def analyze_tool_usage(self, events: List[ToolUsageFinished]):
        cache_hits = sum(1 for e in events if e.from_cache)
        avg_duration = sum(
            (e.finished_at - e.started_at).total_seconds()
            for e in events
        ) / len(events)
        return {
            "cache_hit_rate": cache_hits / len(events),
            "avg_duration": avg_duration
        }
```

## Conclusão
O sistema de eventos de uso de ferramentas do CrewAI fornece uma base sólida para monitoramento, análise e otimização do uso de ferramentas pelos agentes. Sua estrutura bem definida e extensível permite um rastreamento eficiente e análise detalhada do comportamento das ferramentas no sistema.
