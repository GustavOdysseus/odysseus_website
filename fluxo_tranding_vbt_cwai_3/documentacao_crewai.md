# Documentação da Base de Código - CrewAI

## Introdução Geral
O sistema CrewAI é uma plataforma projetada para gerenciar e executar tarefas de forma colaborativa entre agentes. O objetivo principal é permitir que múltiplos agentes trabalhem juntos para resolver problemas complexos, utilizando um modelo de linguagem para facilitar a comunicação e a execução de tarefas. As principais funcionalidades incluem:

- Execução de tarefas de forma síncrona e assíncrona.
- Delegação de tarefas entre agentes.
- Gerenciamento de conhecimento e memória contextual.
- Integração com ferramentas externas para execução de tarefas.

## Documentação por Módulo

### Módulo: `crew.py`
#### Resumo do Módulo
O módulo `crew.py` define a classe `Crew`, que representa um grupo de agentes que colaboram para executar tarefas.

#### Classes
- **Crew**
  - **Responsabilidades**: Gerenciar um conjunto de agentes, coordenar a execução de tarefas e manter o estado do grupo.

#### Métodos
- **add_agent(agent: BaseAgent)**: Adiciona um agente ao grupo.
- **execute_task(task: Task)**: Executa uma tarefa utilizando os agentes disponíveis.

#### Exemplos de Uso
```python
from crewai_ref.crew import Crew
from crewai_ref.agent import Agent
from crewai_ref.task import Task

crew = Crew()
agent = Agent(role="Analista", goal="Analisar dados")
crew.add_agent(agent)

task = Task(description="Analisar dados de vendas", expected_output="Relatório de vendas")
crew.execute_task(task)
```

### Módulo: `task.py`
#### Resumo do Módulo
O módulo `task.py` define a classe `Task`, que representa uma tarefa a ser executada por um agente.

#### Classes
- **Task**
  - **Responsabilidades**: Definir a estrutura de uma tarefa, incluindo descrição, agente responsável e saída esperada.

#### Métodos
- **execute_sync()**: Executa a tarefa de forma síncrona.
- **execute_async()**: Executa a tarefa de forma assíncrona.

#### Exemplos de Uso
```python
from crewai_ref.task import Task

task = Task(description="Gerar relatório", expected_output="Relatório gerado")
task.execute_sync()
```

### Módulo: `agent.py`
#### Resumo do Módulo
O módulo `agent.py` define a classe `Agent`, que representa um agente que pode executar tarefas e interagir com outros agentes.

#### Classes
- **Agent**
  - **Responsabilidades**: Executar tarefas, gerenciar conhecimento e interagir com outros agentes.

#### Métodos
- **execute_task(task: Task)**: Executa uma tarefa específica.
- **create_agent_executor()**: Cria um executor para gerenciar a execução de tarefas.

#### Exemplos de Uso
```python
from crewai_ref.agent import Agent
from crewai_ref.task import Task

agent = Agent(role="Executor", goal="Executar tarefas")
task = Task(description="Processar dados", expected_output="Dados processados")
agent.execute_task(task)
```

## Grafo de Dependências
O grafo de dependências representa as relações entre os módulos do sistema. Cada módulo pode depender de outros módulos para funcionar corretamente. Abaixo está uma representação textual do grafo:

```
Crew <--> Agent
Agent <--> Task
```

### Interações entre Módulos
- O módulo `Crew` gerencia instâncias de `Agent` e coordena a execução de `Task`.
- O módulo `Agent` é responsável por executar `Task` e pode interagir com outros agentes para delegar tarefas.

## Fluxos Críticos
### Como um Dado é Processado de Entrada até o Armazenamento
1. Um agente é criado e recebe uma tarefa.
2. A tarefa é executada, podendo envolver a coleta de dados de várias fontes.
3. Os resultados são processados e armazenados em um formato definido (JSON, Pydantic, etc.).
4. O agente pode delegar tarefas a outros agentes conforme necessário.

Essa documentação fornece uma visão geral do sistema e detalhes técnicos que ajudarão novos desenvolvedores a entenderem a estrutura e funcionamento do CrewAI.
