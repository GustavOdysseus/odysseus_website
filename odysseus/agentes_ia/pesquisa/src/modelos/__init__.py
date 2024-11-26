"""
Módulo de modelos do sistema Odysseus.

Este pacote contém todos os modelos Pydantic utilizados no sistema Odysseus,
organizados em módulos específicos por funcionalidade.
"""

from .config_models import (
    ProcessType, ControlLevel, AgentConfig,
    TaskConfig, TeamConfig
)

from .research_models import (
    ArxivArticle, ArticleAnalysis,
    ReviewReport, ResearchOutput
)

from .flow_models import (
    EventPriority, EventType, MetricType,
    Metric, Decision, FlowEvent,
    FlowState, ResearchFlowState
)

from .state_models import (
    CrewState, AnalysisCache,
    ConditionType, ExecutionCondition,
    TimedEventType, TimedEvent,
    PropagationRule, Feedback
)

__all__ = [
    # Config Models
    'ProcessType', 'ControlLevel', 'AgentConfig',
    'TaskConfig', 'TeamConfig',
    
    # Research Models
    'ArxivArticle', 'ArticleAnalysis',
    'ReviewReport', 'ResearchOutput',
    
    # Flow Models
    'EventPriority', 'EventType', 'MetricType',
    'Metric', 'Decision', 'FlowEvent',
    'FlowState', 'ResearchFlowState',
    
    # State Models
    'CrewState', 'AnalysisCache',
    'ConditionType', 'ExecutionCondition',
    'TimedEventType', 'TimedEvent',
    'PropagationRule', 'Feedback'
]