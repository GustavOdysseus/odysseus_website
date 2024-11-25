"""
Modelos de fluxo do sistema Odysseus.

Este módulo define os modelos Pydantic que validam as configurações YAML
dos fluxos de execução do sistema. Os fluxos são definidos em arquivos YAML
e este módulo garante que sigam a estrutura correta.

Classes:
    EventPriority: Enum para níveis de prioridade de eventos
    EventType: Enum para tipos de eventos do sistema
    MetricType: Enum para tipos de métricas
    Metric: Modelo para métricas do sistema
    Decision: Modelo para decisões de equipes
    FlowEvent: Modelo para eventos de fluxo
    FlowState: Modelo para estado global do flow
    ResearchFlowState: Modelo para estado do fluxo de pesquisa

Exemplo de arquivo YAML:
```yaml
# flows/research_flow.yaml
flow_id: "research_001"
type: "research"
steps:
  - id: "collect_papers"
    type: "task"
    config:
      query: "machine learning"
      max_papers: 100
    next: "analyze_papers"
    
  - id: "analyze_papers"
    type: "task"
    config:
      metrics:
        - type: "performance"
          threshold: 0.8
    next: "generate_report"
    
  - id: "generate_report"
    type: "task"
    config:
      format: "pdf"
      include_metrics: true

events:
  - type: "checkpoint"
    trigger: "papers_collected"
    action: "validate_papers"
  
  - type: "metric_threshold"
    trigger: "low_confidence"
    action: "request_review"

metrics:
  - type: "performance"
    target: 0.9
  - type: "quality"
    target: 0.85
```

O flow_manager usará estes modelos para:
1. Validar os arquivos YAML de configuração dos fluxos
2. Carregar as configurações em objetos Python tipados
3. Gerenciar o estado da execução dos fluxos
4. Propagar eventos e métricas conforme definido
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class EventPriority(str, Enum):
    """
    Define níveis de prioridade para eventos no sistema.
    
    Valores:
        LOW: Prioridade baixa
        MEDIUM: Prioridade média
        HIGH: Prioridade alta
        CRITICAL: Prioridade crítica
    
    Exemplo:
    ```yaml
    event_priority: critical
    ```
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class EventType(str, Enum):
    """
    Define os tipos de eventos que podem ocorrer durante a execução do flow.
    
    Valores:
        TASK_COMPLETE: Tarefa concluída
        STATE_CHANGE: Mudança de estado
        ERROR: Erro ocorrido
        FEEDBACK: Feedback recebido
        CONDITION_MET: Condição atingida
        CHECKPOINT: Ponto de verificação
        ROLLBACK: Reversão de estado
        TIMEOUT: Tempo limite excedido
        METRIC_THRESHOLD: Limite de métrica atingido
    
    Exemplo:
    ```yaml
    event_type: task_complete
    data:
      task_id: "task_001"
      status: "success"
    ```
    """
    TASK_COMPLETE = "task_complete"
    STATE_CHANGE = "state_change"
    ERROR = "error"
    FEEDBACK = "feedback"
    CONDITION_MET = "condition_met"
    CHECKPOINT = "checkpoint"
    ROLLBACK = "rollback"
    TIMEOUT = "timeout"
    METRIC_THRESHOLD = "metric_threshold"

class MetricType(str, Enum):
    """
    Define os tipos de métricas disponíveis no sistema.
    
    Valores:
        PERFORMANCE: Métricas de desempenho
        CONFIDENCE: Nível de confiança
        COST: Custo de execução
        LATENCY: Latência de operações
        QUALITY: Qualidade dos resultados
    
    Exemplo:
    ```yaml
    metric_type: performance
    value: 0.95
    metadata:
      model: "gpt-4"
      task: "analysis"
    ```
    """
    PERFORMANCE = "performance"
    CONFIDENCE = "confidence"
    COST = "cost"
    LATENCY = "latency"
    QUALITY = "quality"

class Metric(BaseModel):
    """
    Modelo para métricas do sistema.
    
    Este modelo define a estrutura de métricas coletadas durante
    a execução do sistema.

    Exemplo:
    ```yaml
    type: performance
    value: 0.95
    timestamp: "2024-01-01T12:00:00"
    metadata:
      model: "gpt-4"
      task: "analysis"
      batch_size: 100
    ```

    Atributos:
        type (MetricType): Tipo da métrica
        value (float): Valor da métrica
        timestamp (datetime): Momento da coleta
        metadata (Dict[str, Any]): Metadados adicionais
    """
    type: MetricType
    value: float
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Decision(BaseModel):
    """
    Modelo para decisões tomadas por uma equipe.
    
    Este modelo registra decisões importantes tomadas durante
    a execução do fluxo.

    Exemplo:
    ```yaml
    crew_id: "research_team_001"
    decision: "Aumentar amostragem de artigos"
    context:
      current_sample: 100
      target_sample: 200
      reason: "Baixa confiança estatística"
    metrics:
      - type: confidence
        value: 0.75
    timestamp: "2024-01-01T12:00:00"
    ```

    Atributos:
        crew_id (str): ID da equipe que tomou a decisão
        decision (str): Descrição da decisão
        context (Dict[str, Any]): Contexto da decisão
        metrics (List[Metric]): Métricas relacionadas
        timestamp (datetime): Momento da decisão
    """
    crew_id: str
    decision: str
    context: Dict[str, Any] = Field(default_factory=dict)
    metrics: List[Metric] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)

class FlowEvent(BaseModel):
    """
    Modelo para eventos de fluxo no sistema.
    
    Este modelo registra eventos que ocorrem durante a execução
    do fluxo de trabalho.

    Exemplo:
    ```yaml
    event_id: "evt_001"
    event_type: "task_complete"
    timestamp: "2024-01-01T12:00:00"
    flow_id: "flow_001"
    step_id: "step_001"
    status: "success"
    data:
      task: "article_analysis"
      articles_processed: 100
      confidence: 0.95
    metadata:
      model: "gpt-4"
      execution_time: 120
    next_steps:
      - "generate_report"
      - "update_metrics"
    ```

    Atributos:
        event_id (str): Identificador único do evento
        event_type (str): Tipo do evento
        timestamp (datetime): Momento do evento
        flow_id (str): ID do fluxo relacionado
        step_id (str): ID do passo relacionado
        status (str): Status do evento
        data (Dict[str, Any]): Dados do evento
        metadata (Optional[Dict]): Metadados adicionais
        next_steps (Optional[List[str]]): Próximos passos
    """
    event_id: str
    event_type: str
    timestamp: datetime
    flow_id: str
    step_id: str
    status: str
    data: Dict[str, Any]
    metadata: Optional[Dict] = None
    next_steps: Optional[List[str]] = None

class FlowState(BaseModel):
    """
    Modelo para estado global do flow.
    
    Este modelo mantém o estado completo do sistema, incluindo
    estados de equipes, eventos, métricas e regras.

    Exemplo:
    ```yaml
    shared_state:
      current_phase: "analysis"
      total_articles: 500
    crew_states:
      research_team:
        status: "active"
        current_task: "article_review"
    event_history:
      - event_id: "evt_001"
        event_type: "task_complete"
    active_crews:
      - "research_team"
      - "review_team"
    metrics_history:
      - type: "performance"
        value: 0.95
    ```

    Atributos:
        shared_state (Dict[str, Any]): Estado compartilhado
        crew_states (Dict[str, CrewState]): Estados das equipes
        event_history (List[FlowEvent]): Histórico de eventos
        active_crews (List[str]): Equipes ativas
        execution_context (Dict[str, Any]): Contexto de execução
        metrics_history (List[Metric]): Histórico de métricas
        decisions_history (List[Decision]): Histórico de decisões
        checkpoints (Dict[str, Dict]): Pontos de verificação
        analysis_cache (AnalysisCache): Cache de análises
        timed_events (List[TimedEvent]): Eventos temporizados
        propagation_rules (Dict[EventType, List[PropagationRule]]): Regras de propagação
        feedback_history (List[Feedback]): Histórico de feedback
        feedback_rules (Dict[str, List[Dict[str, Any]]]): Regras de feedback
        execution_conditions (Dict[str, List[ExecutionCondition]]): Condições de execução
    """
    shared_state: Dict[str, Any] = Field(default_factory=dict)
    crew_states: Dict[str, 'CrewState'] = Field(default_factory=dict)
    event_history: List[FlowEvent] = Field(default_factory=list)
    active_crews: List[str] = Field(default_factory=list)
    execution_context: Dict[str, Any] = Field(default_factory=dict)
    metrics_history: List[Metric] = Field(default_factory=list)
    decisions_history: List[Decision] = Field(default_factory=list)
    checkpoints: Dict[str, Dict] = Field(default_factory=dict)
    analysis_cache: 'AnalysisCache' = Field(default_factory=lambda: AnalysisCache())
    timed_events: List['TimedEvent'] = Field(default_factory=list)
    propagation_rules: Dict[EventType, List['PropagationRule']] = Field(default_factory=dict)
    feedback_history: List['Feedback'] = Field(default_factory=list)
    feedback_rules: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict)
    execution_conditions: Dict[str, List['ExecutionCondition']] = Field(default_factory=dict)

class ResearchFlowState(BaseModel):
    """
    Modelo para estado do fluxo de pesquisa.
    
    Este modelo mantém o estado específico de um fluxo de pesquisa,
    incluindo progresso, métricas e eventos.

    Exemplo:
    ```yaml
    flow_id: "research_001"
    status: "in_progress"
    progress: 0.75
    current_step: "article_analysis"
    metrics:
      - type: "performance"
        value: 0.95
    events:
      - event_id: "evt_001"
        event_type: "task_complete"
    metadata:
      total_articles: 500
      analyzed_articles: 375
    timestamp: "2024-01-01T12:00:00"
    ```

    Atributos:
        flow_id (str): Identificador do fluxo
        status (str): Status atual do fluxo
        progress (float): Progresso atual (0.0 a 1.0)
        current_step (str): Passo atual
        metrics (List[Metric]): Métricas do fluxo
        events (List[FlowEvent]): Eventos do fluxo
        metadata (Dict[str, Any]): Metadados adicionais
        timestamp (datetime): Última atualização
    """
    flow_id: str
    status: str
    progress: float = 0.0
    current_step: str
    metrics: List[Metric] = Field(default_factory=list)
    events: List[FlowEvent] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)

# Atualizando referências circulares
from .state_models import CrewState, AnalysisCache, ExecutionCondition, TimedEvent, PropagationRule, Feedback
