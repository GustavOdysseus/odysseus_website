"""
Modelos de estado do sistema Odysseus.

Este módulo define os modelos Pydantic que validam as configurações YAML
relacionadas ao estado do sistema Odysseus, incluindo estados da equipe,
cache e condições de execução. Os modelos servem como esquemas de validação
para as configurações definidas em YAML.

Classes:
    CrewState: Modelo para estado de uma equipe
    AnalysisCache: Modelo para cache de análises
    ConditionType: Tipos de condições de execução
    ExecutionCondition: Modelo para condições de execução
    TimedEventType: Tipos de eventos temporizados
    TimedEvent: Modelo para eventos temporizados
    PropagationRule: Modelo para regras de propagação
    Feedback: Modelo para feedback do sistema

Exemplo de arquivo YAML:
```yaml
# state/crew_state.yaml
crew_state:
  crew_id: "research_team_001"
  status: "active"
  active_tasks:
    - "analyze_papers"
    - "generate_report"
  completed_tasks:
    - "data_collection"
    - "initial_review"
  metrics:
    papers_analyzed: 45
    avg_relevance: 0.85
  resources:
    api_credits: 1000
    storage_quota: 5000
  metadata:
    project: "ML Research"
    priority: "high"

analysis_cache:
  articles:
    "2401.12345":
      title: "Advanced ML"
      cached_at: "2024-01-15T10:00:00"
  analyses:
    "analysis_001":
      status: "completed"
      results: {...}
  metrics:
    relevance: [0.85, 0.92, 0.78]
  expiration: "2024-02-15T00:00:00"
  size_limit: 1000000

execution_conditions:
  - condition_type: "metric"
    condition_data:
      metric_name: "relevance_score"
      threshold: 0.8
      operator: ">"
    timeout: 3600
    retry_count: 3
    priority: 1

timed_events:
  - event_type: "checkpoint"
    schedule_time: "2024-01-15T12:00:00"
    repeat_interval: 3600
    max_occurrences: 24
    data:
      save_path: "/checkpoints"
      compress: true

propagation_rules:
  - source_event: "new_paper"
    target_events: ["analyze", "update_cache"]
    conditions:
      - condition_type: "metric"
        condition_data:
          metric: "relevance"
          min_value: 0.7

feedback:
  - feedback_id: "fb_001"
    source: "analysis_pipeline"
    feedback_type: "warning"
    content: "High processing time detected"
    severity: "medium"
    metadata:
      affected_component: "paper_processor"
```
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class CrewState(BaseModel):
    """
    Modelo para validação de configurações de estado de uma equipe.
    
    Este modelo define a estrutura esperada para configurações YAML
    do estado de uma equipe de pesquisa.

    Exemplo:
    ```yaml
    crew_id: "research_team_001"
    status: "active"
    active_tasks:
      - "analyze_papers"
      - "generate_report"
    completed_tasks:
      - "data_collection"
    metrics:
      papers_analyzed: 45
      avg_relevance: 0.85
    resources:
      api_credits: 1000
      storage_quota: 5000
    metadata:
      project: "ML Research"
    ```

    Atributos:
        crew_id (str): ID único da equipe
        status (str): Estado atual da equipe
        active_tasks (List[str]): Tarefas em andamento
        completed_tasks (List[str]): Tarefas concluídas
        metrics (Dict[str, float]): Métricas da equipe
        resources (Dict[str, Any]): Recursos disponíveis
        last_update (datetime): Última atualização
        metadata (Optional[Dict]): Metadados adicionais
    """
    crew_id: str
    status: str
    active_tasks: List[str]
    completed_tasks: List[str]
    metrics: Dict[str, float]
    resources: Dict[str, Any]
    last_update: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict] = None

class AnalysisCache(BaseModel):
    """
    Modelo para validação de configurações de cache de análises.l
    
    Este modelo define a estrutura esperada para configurações YAML
    do cache de análises do sistema.

    Exemplo:
    ```yaml
    articles:
      "2401.12345":
        title: "Advanced ML"
        cached_at: "2024-01-15T10:00:00"
    analyses:
      "analysis_001":
        status: "completed"
        results: {...}
    metrics:
      relevance: [0.85, 0.92, 0.78]
    expiration: "2024-02-15T00:00:00"
    size_limit: 1000000
    ```

    Atributos:
        articles (Dict[str, Any]): Cache de artigos
        analyses (Dict[str, Any]): Cache de análises
        metrics (Dict[str, List[float]]): Cache de métricas
        last_update (datetime): Última atualização
        expiration (Optional[datetime]): Data de expiração
        size_limit (Optional[int]): Limite de tamanho
    """
    articles: Dict[str, Any] = Field(default_factory=dict)
    analyses: Dict[str, Any] = Field(default_factory=dict)
    metrics: Dict[str, List[float]] = Field(default_factory=dict)
    last_update: datetime = Field(default_factory=datetime.now)
    expiration: Optional[datetime] = None
    size_limit: Optional[int] = None

class ConditionType(str, Enum):
    """
    Define os tipos de condições de execução.
    
    Valores:
        METRIC: Condição baseada em métrica
        TIME: Condição baseada em tempo
        EVENT: Condição baseada em evento
        STATE: Condição baseada em estado
        CUSTOM: Condição customizada
    """
    METRIC = "metric"
    TIME = "time"
    EVENT = "event"
    STATE = "state"
    CUSTOM = "custom"

class ExecutionCondition(BaseModel):
    """
    Modelo para validação de configurações de condições de execução.
    
    Este modelo define a estrutura esperada para configurações YAML
    de condições de execução do sistema.

    Exemplo:
    ```yaml
    condition_type: "metric"
    condition_data:
      metric_name: "relevance_score"
      threshold: 0.8
      operator: ">"
    timeout: 3600
    retry_count: 3
    priority: 1
    metadata:
      description: "Check relevance threshold"
    ```

    Atributos:
        condition_type (ConditionType): Tipo da condição
        condition_data (Dict[str, Any]): Dados da condição
        timeout (Optional[float]): Tempo limite em segundos
        retry_count (Optional[int]): Número de tentativas
        priority (Optional[int]): Prioridade da condição
        metadata (Optional[Dict]): Metadados adicionais
    """
    condition_type: ConditionType
    condition_data: Dict[str, Any]
    timeout: Optional[float] = None
    retry_count: Optional[int] = None
    priority: Optional[int] = None
    metadata: Optional[Dict] = None

class TimedEventType(str, Enum):
    """
    Define os tipos de eventos temporizados.
    
    Valores:
        CHECKPOINT: Evento de checkpoint
        METRIC_COLLECTION: Coleta de métricas
        STATE_UPDATE: Atualização de estado
        CLEANUP: Limpeza de recursos
        CUSTOM: Evento customizado
    """
    CHECKPOINT = "checkpoint"
    METRIC_COLLECTION = "metric_collection"
    STATE_UPDATE = "state_update"
    CLEANUP = "cleanup"
    CUSTOM = "custom"

class TimedEvent(BaseModel):
    """
    Modelo para validação de configurações de eventos temporizados.
    
    Este modelo define a estrutura esperada para configurações YAML
    de eventos temporizados do sistema.

    Exemplo:
    ```yaml
    event_type: "checkpoint"
    schedule_time: "2024-01-15T12:00:00"
    repeat_interval: 3600
    max_occurrences: 24
    data:
      save_path: "/checkpoints"
      compress: true
    metadata:
      description: "Hourly checkpoint"
    ```

    Atributos:
        event_type (TimedEventType): Tipo do evento
        schedule_time (datetime): Horário agendado
        repeat_interval (Optional[float]): Intervalo de repetição
        max_occurrences (Optional[int]): Máximo de ocorrências
        data (Dict[str, Any]): Dados do evento
        metadata (Optional[Dict]): Metadados adicionais
    """
    event_type: TimedEventType
    schedule_time: datetime
    repeat_interval: Optional[float] = None
    max_occurrences: Optional[int] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Optional[Dict] = None

class PropagationRule(BaseModel):
    """
    Modelo para validação de configurações de regras de propagação.
    
    Este modelo define a estrutura esperada para configurações YAML
    de regras de propagação de eventos.

    Exemplo:
    ```yaml
    source_event: "new_paper"
    target_events:
      - "analyze"
      - "update_cache"
    conditions:
      - condition_type: "metric"
        condition_data:
          metric: "relevance"
          min_value: 0.7
    transformations:
      paper_id: "analysis_id"
    metadata:
      description: "Paper analysis flow"
    ```

    Atributos:
        source_event (str): Evento fonte
        target_events (List[str]): Eventos alvo
        conditions (List[ExecutionCondition]): Condições
        transformations (Optional[Dict[str, str]]): Transformações
        metadata (Optional[Dict]): Metadados adicionais
    """
    source_event: str
    target_events: List[str]
    conditions: List[ExecutionCondition]
    transformations: Optional[Dict[str, str]] = None
    metadata: Optional[Dict] = None

class Feedback(BaseModel):
    """
    Modelo para validação de configurações de feedback.
    
    Este modelo define a estrutura esperada para configurações YAML
    de feedback do sistema.

    Exemplo:
    ```yaml
    feedback_id: "fb_001"
    source: "analysis_pipeline"
    feedback_type: "warning"
    content: "High processing time detected"
    severity: "medium"
    metadata:
      affected_component: "paper_processor"
      action_required: true
    ```

    Atributos:
        feedback_id (str): ID único do feedback
        source (str): Fonte do feedback
        feedback_type (str): Tipo do feedback
        content (Any): Conteúdo do feedback
        timestamp (datetime): Timestamp do feedback
        severity (Optional[str]): Severidade
        metadata (Optional[Dict]): Metadados adicionais
    """
    feedback_id: str
    source: str
    feedback_type: str
    content: Any
    timestamp: datetime = Field(default_factory=datetime.now)
    severity: Optional[str] = None
    metadata: Optional[Dict] = None
