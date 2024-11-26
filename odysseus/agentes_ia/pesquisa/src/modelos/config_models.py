"""
Modelos de configuração do sistema Odysseus.

Este módulo contém os modelos Pydantic que definem as configurações
do sistema Odysseus. Todas as configurações são definidas em arquivos YAML
e validadas através destes modelos.

Classes:
    ProcessType: Enum para tipos de processo de execução
    ControlLevel: Modelo para controle de comportamento dos agentes
    AgentConfig: Configuração completa de agentes LLM
    TaskConfig: Configuração de tarefas individuais
    TeamConfig: Configuração de equipes de agentes

Exemplo de arquivo YAML:
```yaml
# config/agents/researcher.yaml
role: "Pesquisador"
goal: "Analisar artigos do arXiv sobre IA"
backstory: "Especialista em análise de artigos científicos"
model: "gpt-4"
temperature: 0.7
max_tokens: 2000

# config/tasks/analysis.yaml
name: "Análise de Tendências"
description: "Identificar tendências em artigos recentes"
priority: 1
tags:
  - "research"
  - "trends"

# config/teams/research_team.yaml
name: "Equipe de Pesquisa"
description: "Equipe focada em análise de artigos"
leader_role: "Coordenador"
hierarchy_type: "hierarchical"
members:
  - role: "Pesquisador"
    config: "agents/researcher.yaml"
```

Uso típico:
```python
import yaml
from src.modelos import AgentConfig

# Carregando configuração do YAML
with open('config/agents/researcher.yaml', 'r') as f:
    config_data = yaml.safe_load(f)

# Validando configuração através do modelo
agent_config = AgentConfig(**config_data)
```
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class ProcessType(str, Enum):
    """
    Define os tipos de processo suportados para execução de equipes.
    
    Valores em YAML:
        sequential: Execução sequencial de tarefas
        hierarchical: Execução hierárquica com delegação
        parallel: Execução paralela de tarefas independentes
    
    Exemplo:
    ```yaml
    process_type: hierarchical
    ```
    """
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"
    PARALLEL = "parallel"

class ControlLevel(BaseModel):
    """
    Modelo para níveis de controle dos agentes no sistema Odysseus.
    
    Este modelo define parâmetros que controlam o comportamento e a saída dos agentes.
    Todas as configurações são definidas via YAML.

    Exemplo YAML:
    ```yaml
    entonacao: formal
    foco_topico: 
      - "machine learning"
      - "deep learning"
    lingua: 
      - "pt-br"
      - "en-us"
    sentimento: neutro
    originalidade: 80
    abstracao: 60
    tempo_verbal: presente
    profundidade: detalhado
    ```

    Atributos:
        entonacao (str): Tom de comunicação do agente (ex: formal, informal)
        foco_topico (Union[str, List[str]]): Tópicos principais a serem abordados
        lingua (List[str]): Lista de idiomas suportados
        sentimento (str): Sentimento geral da comunicação
        criterios_selecao (Optional[List[str]]): Critérios para seleção de informações
        originalidade (Optional[int]): Nível de originalidade (0-100)
        abstracao (Optional[int]): Nível de abstração (0-100)
        tempo_verbal (Optional[str]): Tempo verbal predominante
        profundidade (Optional[str]): Nível de profundidade da análise
    """
    entonacao: str
    foco_topico: Union[str, List[str]]
    lingua: List[str]
    sentimento: str
    criterios_selecao: Optional[List[str]] = None
    originalidade: Optional[int] = None
    abstracao: Optional[int] = None
    tempo_verbal: Optional[str] = None
    profundidade: Optional[str] = None

class AgentConfig(BaseModel):
    """
    Configuração completa dos agentes LLM no sistema Odysseus.
    
    Este modelo define todos os parâmetros necessários para configurar e
    controlar o comportamento de um agente LLM. Todas as configurações
    são definidas em arquivos YAML.

    Exemplo YAML:
    ```yaml
    # Campos Obrigatórios
    role: "Pesquisador"
    goal: "Analisar artigos científicos"
    backstory: "Especialista em análise de literatura acadêmica"
    
    # Configuração do Modelo
    model: "gpt-4"
    tools:
      - "arxiv_search"
      - "pdf_reader"
    
    # Controle de Execução
    max_iter: 25
    verbose: true
    cache: true
    
    # Parâmetros do LLM
    temperature: 0.7
    max_tokens: 2000
    
    # Especialização
    specialties:
      - "machine learning"
      - "deep learning"
    ```

    Atributos:
        role (str): Papel/função do agente na equipe
        goal (str): Objetivo principal do agente
        backstory (str): História/contexto do agente
        model (Optional[str]): Modelo LLM a ser usado
        tools (Optional[List]): Ferramentas disponíveis
        function_calling_llm (Optional[str]): LLM para chamadas de função
        max_iter (Optional[int]): Máximo de iterações (default: 25)
        max_rpm (Optional[int]): Máximo de requisições por minuto
        max_execution_time (Optional[int]): Tempo máximo de execução
        verbose (Optional[bool]): Modo verboso
        allow_delegation (Optional[bool]): Permite delegação de tarefas
        step_callback (Optional[str]): Callback para cada passo
        cache (Optional[bool]): Usa cache (default: True)
        system_template (Optional[str]): Template do prompt do sistema
        prompt_template (Optional[str]): Template de prompts
        response_template (Optional[str]): Template de respostas
        allow_code_execution (Optional[bool]): Permite execução de código
        max_retry_limit (Optional[int]): Limite de tentativas
        use_system_prompt (Optional[bool]): Usa prompt do sistema
        respect_context_window (Optional[bool]): Respeita janela de contexto
        code_execution_mode (Optional[str]): Modo de execução de código
        quantidade (Optional[int]): Número de instâncias
        max_tokens (Optional[int]): Máximo de tokens
        temperature (Optional[float]): Temperatura (default: 0.7)
        top_p (Optional[float]): Top-p sampling
        n (Optional[int]): Número de completions
        stop (Optional[Union[str, List[str]]]): Sequências de parada
        presence_penalty (Optional[float]): Penalidade de presença
        frequency_penalty (Optional[float]): Penalidade de frequência
        logit_bias (Optional[Dict[int, float]]): Viés de logits
        seed (Optional[int]): Seed para reprodutibilidade
        logprobs (Optional[bool]): Retorna log probs
        top_logprobs (Optional[int]): Número de top logprobs
        api_key (Optional[str]): Chave da API
        timeout (Optional[Union[float, int]]): Timeout em segundos
        retry_attempts (Optional[int]): Tentativas de retry
        batch_size (Optional[int]): Tamanho do batch
        specialties (Optional[List[str]]): Especialidades do agente
        memory_config (Optional[Dict]): Configuração de memória
        output_format (Optional[str]): Formato de saída
    """
    # Campos obrigatórios
    role: str
    goal: str
    backstory: str
    
    # Campos opcionais - Configuração do Modelo
    model: Optional[str] = None
    tools: Optional[List] = None
    function_calling_llm: Optional[str] = None
    
    # Campos opcionais - Controle de Execução
    max_iter: Optional[int] = 25
    max_rpm: Optional[int] = None
    max_execution_time: Optional[int] = None
    verbose: Optional[bool] = False
    allow_delegation: Optional[bool] = False
    step_callback: Optional[str] = None
    cache: Optional[bool] = True
    
    # Campos opcionais - Templates
    system_template: Optional[str] = None
    prompt_template: Optional[str] = None
    response_template: Optional[str] = None
    
    # Campos opcionais - Execução de Código
    allow_code_execution: Optional[bool] = False
    max_retry_limit: Optional[int] = 2
    use_system_prompt: Optional[bool] = True
    respect_context_window: Optional[bool] = True
    code_execution_mode: Optional[str] = 'safe'
    
    # Campos opcionais - Configuração de Instâncias
    quantidade: Optional[int] = 1
    
    # Campos opcionais - Parâmetros do LLM
    max_tokens: Optional[int] = None
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = None
    n: Optional[int] = None
    stop: Optional[Union[str, List[str]]] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[Dict[int, float]] = None
    seed: Optional[int] = None
    logprobs: Optional[bool] = None
    top_logprobs: Optional[int] = None
    api_key: Optional[str] = None
    
    # Campos opcionais - Controle de Recursos
    timeout: Optional[Union[float, int]] = None
    retry_attempts: Optional[int] = None
    batch_size: Optional[int] = None
    
    # Campos opcionais - Especialização
    specialties: Optional[List[str]] = None
    memory_config: Optional[Dict] = None
    output_format: Optional[str] = None

class TaskConfig(BaseModel):
    """
    Configuração de tarefas no sistema Odysseus.
    
    Este modelo define os parâmetros necessários para configurar uma tarefa
    individual. Todas as configurações são definidas em arquivos YAML.

    Exemplo YAML:
    ```yaml
    name: "Análise de Tendências"
    description: "Identificar tendências em artigos recentes de ML"
    priority: 1
    deadline: "2024-12-31T23:59:59"
    dependencies:
      - "coleta_dados"
      - "pre_processamento"
    acceptance_criteria:
      - "Mínimo de 100 artigos analisados"
      - "Identificação de 5 principais tendências"
    metrics:
      coverage: 0.95
      confidence: 0.8
    tags:
      - "research"
      - "trends"
      - "machine_learning"
    ```

    Atributos:
        name (str): Nome da tarefa
        description (str): Descrição detalhada da tarefa
        priority (Optional[int]): Prioridade da tarefa (maior = mais prioritário)
        deadline (Optional[datetime]): Prazo de conclusão
        dependencies (Optional[List[str]]): Lista de tarefas dependentes
        acceptance_criteria (Optional[List[str]]): Critérios de aceitação
        metrics (Optional[Dict]): Métricas de avaliação
        review_type (Optional[str]): Tipo de revisão necessária
        version (Optional[str]): Versão da tarefa
        tags (Optional[List[str]]): Tags para categorização
    """
    name: str
    description: str
    priority: Optional[int] = None
    deadline: Optional[datetime] = None
    dependencies: Optional[List[str]] = None
    acceptance_criteria: Optional[List[str]] = None
    metrics: Optional[Dict] = None
    review_type: Optional[str] = None
    version: Optional[str] = None
    tags: Optional[List[str]] = None

class TeamConfig(BaseModel):
    """
    Configuração de equipes de agentes no sistema Odysseus.
    
    Este modelo define a estrutura e comportamento de uma equipe de agentes.
    Todas as configurações são definidas em arquivos YAML.

    Exemplo YAML:
    ```yaml
    name: "Equipe de Pesquisa"
    description: "Equipe focada em análise de artigos científicos"
    leader_role: "Coordenador"
    hierarchy_type: "hierarchical"
    
    members:
      - role: "Pesquisador"
        config: "agents/researcher.yaml"
      - role: "Analista"
        config: "agents/analyst.yaml"
    
    communication_protocol: "round_robin"
    review_protocol:
      type: "peer_review"
      min_reviewers: 2
    
    consensus_rules:
      - "majority_vote"
      - "min_confidence_threshold: 0.8"
    
    resource_limits:
      max_parallel_tasks: 5
      max_tokens_per_hour: 100000
    
    performance_metrics:
      track_completion_time: true
      track_quality_scores: true
    ```

    Atributos:
        name (str): Nome da equipe
        description (str): Descrição da equipe
        leader_role (str): Papel do líder da equipe
        members (List[AgentConfig]): Lista de configurações dos agentes membros
        hierarchy_type (str): Tipo de hierarquia da equipe
        communication_protocol (Optional[str]): Protocolo de comunicação
        review_protocol (Optional[Dict]): Protocolo de revisão
        consensus_rules (Optional[List[str]]): Regras para consenso
        resource_limits (Optional[Dict]): Limites de recursos
        performance_metrics (Optional[Dict]): Métricas de performance
    """
    name: str
    description: str
    leader_role: str
    members: List[AgentConfig]
    hierarchy_type: str
    communication_protocol: Optional[str] = None
    review_protocol: Optional[Dict] = None
    consensus_rules: Optional[List[str]] = None
    resource_limits: Optional[Dict] = None
    performance_metrics: Optional[Dict] = None
