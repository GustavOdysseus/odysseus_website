# Agent Tools - Documentação Detalhada

## Visão Geral
As ferramentas de agente são componentes especializados que permitem a interação entre agentes no CrewAI. Elas incluem funcionalidades para delegação de trabalho e comunicação entre agentes.

## Componentes

### 1. AgentTools
```python
class AgentTools:
    """Gerenciador de ferramentas relacionadas a agentes."""
    
    def __init__(self, agents: list[BaseAgent], i18n: I18N = I18N()):
        self.agents = agents
        self.i18n = i18n
        
    def tools(self) -> list[BaseTool]:
        """Obtém todas as ferramentas de agente disponíveis."""
        coworkers = ", ".join([f"{agent.role}" for agent in self.agents])
        
        delegate_tool = DelegateWorkTool(
            agents=self.agents,
            i18n=self.i18n,
            description=self.i18n.tools("delegate_work").format(
                coworkers=coworkers
            ),
        )
        
        ask_tool = AskQuestionTool(
            agents=self.agents,
            i18n=self.i18n,
            description=self.i18n.tools("ask_question").format(
                coworkers=coworkers
            ),
        )
        
        return [delegate_tool, ask_tool]
```

## Ferramentas Disponíveis

### 1. DelegateWorkTool
```python
class DelegateWorkToolSchema(BaseModel):
    task: str = Field(..., description="Tarefa a ser delegada")
    context: str = Field(..., description="Contexto para a tarefa")
    coworker: str = Field(
        ...,
        description="Papel/nome do coworker para delegar"
    )

class DelegateWorkTool(BaseAgentTool):
    """Ferramenta para delegação de trabalho."""
    name: str = "Delegate work to coworker"
    args_schema: type[BaseModel] = DelegateWorkToolSchema
    
    def _run(
        self,
        task: str,
        context: str,
        coworker: Optional[str] = None,
        **kwargs,
    ) -> str:
        coworker = self._get_coworker(coworker, **kwargs)
        return self._execute(coworker, task, context)
```

### 2. AskQuestionTool
```python
class AskQuestionToolSchema(BaseModel):
    question: str = Field(..., description="Pergunta a ser feita")
    context: str = Field(..., description="Contexto para a pergunta")
    coworker: str = Field(
        ...,
        description="Papel/nome do coworker para perguntar"
    )

class AskQuestionTool(BaseAgentTool):
    """Ferramenta para fazer perguntas a coworkers."""
    name: str = "Ask question to coworker"
    args_schema: type[BaseModel] = AskQuestionToolSchema
    
    def _run(
        self,
        question: str,
        context: str,
        coworker: Optional[str] = None,
        **kwargs,
    ) -> str:
        coworker = self._get_coworker(coworker, **kwargs)
        return self._execute(coworker, question, context)
```

## Funcionalidades Base

### 1. BaseAgentTool
```python
class BaseAgentTool(BaseTool):
    """Classe base para ferramentas relacionadas a agentes."""
    agents: list[BaseAgent] = Field(
        description="Lista de agentes disponíveis"
    )
    i18n: I18N = Field(
        default_factory=I18N,
        description="Configurações de internacionalização"
    )
    
    def _get_coworker(
        self,
        coworker: Optional[str],
        **kwargs
    ) -> Optional[str]:
        """Obtém coworker da lista de argumentos."""
        coworker = (
            coworker
            or kwargs.get("co_worker")
            or kwargs.get("coworker")
        )
        if coworker:
            is_list = coworker.startswith("[") and coworker.endswith("]")
            if is_list:
                coworker = coworker[1:-1].split(",")[0]
        return coworker
```

## Uso das Ferramentas

### 1. Delegação de Trabalho
```python
# Criação da ferramenta
delegate_tool = DelegateWorkTool(
    agents=agent_list,
    i18n=i18n_config
)

# Uso
result = delegate_tool.run(
    task="Analisar dados de vendas",
    context="Precisamos de uma análise detalhada das vendas Q4",
    coworker="analista_dados"
)
```

### 2. Perguntas entre Agentes
```python
# Criação da ferramenta
ask_tool = AskQuestionTool(
    agents=agent_list,
    i18n=i18n_config
)

# Uso
response = ask_tool.run(
    question="Qual o status do projeto X?",
    context="Precisamos atualizar o cliente",
    coworker="gerente_projeto"
)
```

## Melhores Práticas

### 1. Delegação de Trabalho
- Forneça contexto claro
- Especifique expectativas
- Monitore progresso

### 2. Comunicação
- Seja específico
- Forneça contexto relevante
- Evite ambiguidade

### 3. Gerenciamento de Agentes
- Mantenha lista atualizada
- Verifique disponibilidade
- Monitore carga de trabalho

## Considerações Técnicas

### 1. Performance
- Cache de resultados
- Otimização de comunicação
- Balanceamento de carga

### 2. Segurança
- Validação de agentes
- Controle de acesso
- Auditoria de ações

### 3. Escalabilidade
- Design distribuído
- Gerenciamento de recursos
- Monitoramento

## Exemplos Avançados

### 1. Sistema de Delegação com Prioridade
```python
class PriorityDelegateWorkTool(DelegateWorkTool):
    def _run(self, task: str, context: str, coworker: str, priority: int = 1):
        # Implementa delegação com prioridade
        task_with_priority = f"[P{priority}] {task}"
        return super()._run(task_with_priority, context, coworker)
```

### 2. Sistema de Perguntas com Timeout
```python
class TimedAskQuestionTool(AskQuestionTool):
    def _run(
        self,
        question: str,
        context: str,
        coworker: str,
        timeout: int = 60
    ):
        # Implementa pergunta com timeout
        with timeout_context(timeout):
            return super()._run(question, context, coworker)
```

### 3. Sistema de Delegação com Feedback
```python
class FeedbackDelegateWorkTool(DelegateWorkTool):
    def _run(
        self,
        task: str,
        context: str,
        coworker: str,
        feedback_interval: int = 300
    ):
        # Implementa delegação com feedback periódico
        result = super()._run(task, context, coworker)
        self._schedule_feedback(coworker, task, feedback_interval)
        return result
```

## Conclusão
As ferramentas de agente do CrewAI fornecem uma estrutura robusta para interação entre agentes, permitindo delegação de trabalho e comunicação eficiente. Sua implementação cuida de aspectos críticos como validação, tratamento de erros e internacionalização, facilitando a criação de sistemas multi-agente complexos e eficazes.
