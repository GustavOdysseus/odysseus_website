# Agent Tools Manager - Documentação Detalhada

## Visão Geral
O arquivo `agent_tools.py` implementa a classe `AgentTools`, que atua como um gerenciador central para todas as ferramentas relacionadas a agentes no CrewAI. Esta classe é responsável por inicializar e fornecer acesso às ferramentas de interação entre agentes.

## Estrutura da Classe

### AgentTools
```python
class AgentTools:
    def __init__(self, agents: list[BaseAgent], i18n: I18N = I18N()):
        self.agents = agents
        self.i18n = i18n
```

#### Atributos
1. **agents**
   - Tipo: `list[BaseAgent]`
   - Descrição: Lista de agentes disponíveis
   - Uso: Compartilhado entre todas as ferramentas

2. **i18n**
   - Tipo: `I18N`
   - Descrição: Configurações de internacionalização
   - Valor padrão: Nova instância de `I18N()`

## Métodos

### tools()
```python
def tools(self) -> list[BaseTool]:
    """Get all available agent tools"""
    coworkers = ", ".join([f"{agent.role}" for agent in self.agents])
    
    delegate_tool = DelegateWorkTool(
        agents=self.agents,
        i18n=self.i18n,
        description=self.i18n.tools("delegate_work").format(coworkers=coworkers),
    )

    ask_tool = AskQuestionTool(
        agents=self.agents,
        i18n=self.i18n,
        description=self.i18n.tools("ask_question").format(coworkers=coworkers),
    )

    return [delegate_tool, ask_tool]
```

#### Funcionalidade
- Inicializa todas as ferramentas de agente disponíveis
- Configura descrições internacionalizadas
- Compartilha contexto entre ferramentas

#### Retorno
Lista contendo:
1. `DelegateWorkTool`: Para delegação de tarefas
2. `AskQuestionTool`: Para comunicação entre agentes

## Ferramentas Disponíveis

### 1. DelegateWorkTool
- **Propósito**: Delegação de tarefas entre agentes
- **Configuração**:
  ```python
  delegate_tool = DelegateWorkTool(
      agents=self.agents,
      i18n=self.i18n,
      description=self.i18n.tools("delegate_work").format(coworkers=coworkers),
  )
  ```

### 2. AskQuestionTool
- **Propósito**: Comunicação e consulta entre agentes
- **Configuração**:
  ```python
  ask_tool = AskQuestionTool(
      agents=self.agents,
      i18n=self.i18n,
      description=self.i18n.tools("ask_question").format(coworkers=coworkers),
  )
  ```

## Internacionalização

### 1. Configuração de Descrições
```python
coworkers = ", ".join([f"{agent.role}" for agent in self.agents])
description = self.i18n.tools("tool_key").format(coworkers=coworkers)
```

### 2. Componentes
- Lista de coworkers formatada
- Descrições traduzidas
- Mensagens de erro localizadas

## Casos de Uso

### 1. Inicialização Básica
```python
from crewai.tools.agent_tools import AgentTools

# Criar lista de agentes
agents = [agent1, agent2, agent3]

# Inicializar gerenciador
tools_manager = AgentTools(agents)

# Obter ferramentas
available_tools = tools_manager.tools()
```

### 2. Com Internacionalização Personalizada
```python
from crewai.utilities import I18N

# Configurar internacionalização
i18n = I18N(language="pt-br")

# Inicializar com configurações personalizadas
tools_manager = AgentTools(agents, i18n=i18n)
```

### 3. Uso em Sistema Multi-Agente
```python
class MultiAgentSystem:
    def __init__(self, agents):
        self.tools_manager = AgentTools(agents)
        self.tools = self.tools_manager.tools()
        
    def setup_agent(self, agent):
        # Fornecer ferramentas ao agente
        agent.tools = self.tools
```

## Melhores Práticas

### 1. Inicialização
- Inicialize uma única instância por sistema
- Compartilhe as ferramentas entre agentes
- Configure internacionalização adequadamente

### 2. Uso de Ferramentas
- Acesse via método `tools()`
- Mantenha referência às ferramentas
- Atualize quando lista de agentes mudar

### 3. Gestão de Recursos
- Reutilize instâncias quando possível
- Mantenha consistência de estado
- Atualize descrições quando necessário

## Considerações Técnicas

### 1. Performance
- Inicialização eficiente
- Reutilização de recursos
- Compartilhamento de contexto

### 2. Extensibilidade
- Fácil adição de novas ferramentas
- Configuração flexível
- Design modular

### 3. Manutenção
- Código organizado
- Responsabilidades bem definidas
- Fácil atualização

## Exemplos de Implementação

### 1. Sistema Básico
```python
class BasicSystem:
    def __init__(self, agents):
        self.tools_manager = AgentTools(agents)
        
    def get_tools(self):
        return self.tools_manager.tools()
```

### 2. Sistema com Atualização Dinâmica
```python
class DynamicSystem:
    def __init__(self):
        self.agents = []
        self.tools_manager = None
        
    def add_agent(self, agent):
        self.agents.append(agent)
        self.update_tools()
        
    def update_tools(self):
        self.tools_manager = AgentTools(self.agents)
        tools = self.tools_manager.tools()
        self.update_all_agents(tools)
```

### 3. Sistema com Monitoramento
```python
class MonitoredSystem:
    def __init__(self, agents):
        self.tools_manager = AgentTools(agents)
        self.tools = self.tools_manager.tools()
        self.usage_stats = {}
        
    def track_tool_usage(self, tool_name):
        if tool_name not in self.usage_stats:
            self.usage_stats[tool_name] = 0
        self.usage_stats[tool_name] += 1
```

## Conclusão
A classe `AgentTools` fornece uma interface centralizada e eficiente para gerenciar ferramentas de agente no CrewAI. Seu design modular, suporte a internacionalização e facilidade de uso a tornam um componente fundamental para sistemas multi-agente.
