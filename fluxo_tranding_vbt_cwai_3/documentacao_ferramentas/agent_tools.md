# Documentação do Agent Tools

## Visão Geral
O módulo `agent_tools.py` define a classe `AgentTools`, que atua como um gerenciador para ferramentas relacionadas a agentes no CrewAI. Esta classe é responsável por criar e fornecer as ferramentas básicas que os agentes podem usar para interagir entre si.

## Classe AgentTools

### Atributos
- `agents` (list[BaseAgent]): Lista de agentes disponíveis
- `i18n` (I18N): Configurações de internacionalização

### Métodos

#### `__init__(agents: list[BaseAgent], i18n: I18N = I18N())`
Inicializa o gerenciador de ferramentas com a lista de agentes e configurações de internacionalização.

#### `tools() -> list[BaseTool]`
Retorna todas as ferramentas de agente disponíveis.

Retorno:
- Lista contendo:
  1. `DelegateWorkTool`: Ferramenta para delegar trabalho
  2. `AskQuestionTool`: Ferramenta para fazer perguntas

## Ferramentas Disponíveis

### 1. DelegateWorkTool
Permite que um agente delegue trabalho para outro agente.

### 2. AskQuestionTool
Permite que um agente faça perguntas para outro agente.

## Exemplo de Uso

```python
from crewai.tools import AgentTools
from crewai.agents import BaseAgent
from crewai.utilities import I18N

# Criar alguns agentes
agent1 = BaseAgent(role="Analista")
agent2 = BaseAgent(role="Pesquisador")
agents = [agent1, agent2]

# Criar o gerenciador de ferramentas
agent_tools = AgentTools(agents=agents)

# Obter todas as ferramentas disponíveis
tools = agent_tools.tools()

# As ferramentas podem ser usadas pelos agentes para:
# 1. Delegar trabalho:
#    tools[0].run(coworker="Pesquisador", task="Pesquisar sobre X")
# 
# 2. Fazer perguntas:
#    tools[1].run(coworker="Analista", question="Qual sua análise sobre Y?")
```

## Notas Importantes
1. A classe fornece as ferramentas básicas para interação entre agentes
2. Suporta internacionalização para descrições das ferramentas
3. As descrições das ferramentas incluem a lista de coworkers disponíveis
4. As ferramentas são instanciadas com a mesma lista de agentes e configurações i18n
