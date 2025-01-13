# Agent Tools - Documentação Detalhada

## Visão Geral
O módulo `agent_tools` implementa um conjunto de ferramentas que permitem a interação e colaboração entre agentes no CrewAI. Este sistema fornece funcionalidades para delegação de tarefas e comunicação entre agentes.

## Estrutura do Diretório
```
agent_tools/
├── agent_tools.py
├── ask_question_tool.py
├── base_agent_tools.py
└── delegate_work_tool.py
```

## Componentes Principais

### 1. BaseAgentTool (base_agent_tools.py)
Classe base que fornece funcionalidades comuns para todas as ferramentas de agente.

```python
class BaseAgentTool(BaseTool):
    agents: list[BaseAgent]
    i18n: I18N
```

#### Métodos Principais
1. **_get_coworker**
   ```python
   def _get_coworker(self, coworker: Optional[str], **kwargs) -> Optional[str]
   ```
   - Processa e normaliza nomes de coworkers
   - Suporta formato de lista
   - Remove caracteres especiais

2. **_execute**
   ```python
   def _execute(self, agent_name: Union[str, None], task: str, context: Union[str, None]) -> str
   ```
   - Executa tarefas delegadas
   - Gerencia erros
   - Suporta internacionalização

### 2. AgentTools (agent_tools.py)
Classe gerenciadora que fornece acesso a todas as ferramentas de agente disponíveis.

```python
class AgentTools:
    def __init__(self, agents: list[BaseAgent], i18n: I18N = I18N()):
        self.agents = agents
        self.i18n = i18n
```

#### Métodos
1. **tools()**
   ```python
   def tools(self) -> list[BaseTool]
   ```
   - Retorna lista de ferramentas disponíveis
   - Configura descrições internacionalizadas
   - Inicializa ferramentas com agentes

### 3. AskQuestionTool (ask_question_tool.py)
Ferramenta para fazer perguntas a outros agentes.

```python
class AskQuestionToolSchema(BaseModel):
    question: str
    context: str
    coworker: str

class AskQuestionTool(BaseAgentTool):
    name: str = "Ask question to coworker"
    args_schema: type[BaseModel] = AskQuestionToolSchema
```

#### Funcionalidades
- Permite comunicação entre agentes
- Fornece contexto para perguntas
- Valida parâmetros via schema

### 4. DelegateWorkTool (delegate_work_tool.py)
Ferramenta para delegar trabalho entre agentes.

```python
class DelegateWorkToolSchema(BaseModel):
    task: str
    context: str
    coworker: str

class DelegateWorkTool(BaseAgentTool):
    name: str = "Delegate work to coworker"
    args_schema: type[BaseModel] = DelegateWorkToolSchema
```

#### Funcionalidades
- Permite delegação de tarefas
- Fornece contexto para tarefas
- Valida parâmetros via schema

## Fluxos de Trabalho

### 1. Delegação de Tarefas
```python
from crewai.tools.agent_tools import AgentTools

# Configuração
agents = [agent1, agent2]
tools = AgentTools(agents).tools()

# Uso
delegate_tool = tools[0]
result = delegate_tool.run(
    task="Analyze market data",
    context="Q4 2023 financial report",
    coworker="analyst"
)
```

### 2. Comunicação entre Agentes
```python
# Configuração
ask_tool = tools[1]

# Uso
response = ask_tool.run(
    question="What are the key metrics?",
    context="Market analysis project",
    coworker="data_scientist"
)
```

## Internacionalização

### 1. Configuração
```python
from crewai.utilities import I18N

i18n = I18N(language="pt-br")
tools = AgentTools(agents, i18n=i18n).tools()
```

### 2. Mensagens
- Descrições de ferramentas
- Mensagens de erro
- Respostas de agentes

## Melhores Práticas

### 1. Delegação de Tarefas
- Forneça contexto claro
- Especifique agente correto
- Valide resultados

### 2. Comunicação
- Seja específico nas perguntas
- Inclua contexto relevante
- Gerencie timeouts

### 3. Gestão de Erros
- Trate agentes inexistentes
- Valide entradas
- Forneça feedback claro

## Considerações Técnicas

### 1. Performance
- Execução assíncrona
- Gestão de recursos
- Timeouts apropriados

### 2. Extensibilidade
- Ferramentas personalizadas
- Novos tipos de interação
- Plugins de terceiros

### 3. Segurança
- Validação de entrada
- Controle de acesso
- Logging de ações

## Exemplos de Implementação

### 1. Sistema Multi-Agente
```python
class MultiAgentSystem:
    def __init__(self, agents):
        self.tools = AgentTools(agents).tools()
        
    def collaborative_task(self, main_task):
        # Delegar subtarefas
        subtask_results = []
        for subtask in self.decompose_task(main_task):
            result = self.tools[0].run(
                task=subtask.description,
                context=subtask.context,
                coworker=subtask.assigned_to
            )
            subtask_results.append(result)
            
        return self.aggregate_results(subtask_results)
```

### 2. Sistema de Consulta
```python
class QuerySystem:
    def __init__(self, agents):
        self.ask_tool = AgentTools(agents).tools()[1]
        
    def distributed_query(self, question, experts):
        responses = []
        for expert in experts:
            response = self.ask_tool.run(
                question=question,
                context="Expert consultation",
                coworker=expert
            )
            responses.append(response)
        
        return self.synthesize_responses(responses)
```

## Conclusão
O sistema de ferramentas de agente do CrewAI fornece uma base robusta para construir sistemas multi-agente colaborativos. Sua arquitetura modular, suporte a internacionalização e validação forte de tipos o tornam ideal para aplicações complexas de IA.
