# Delegate Work Tool - Documentação Detalhada

## Visão Geral
O arquivo `delegate_work_tool.py` implementa a ferramenta `DelegateWorkTool`, um componente crucial do CrewAI que permite a delegação de tarefas entre agentes. Esta ferramenta facilita a distribuição eficiente de trabalho em um sistema multi-agente.

## Estrutura do Código

### 1. Schema de Validação
```python
class DelegateWorkToolSchema(BaseModel):
    task: str = Field(..., description="The task to delegate")
    context: str = Field(..., description="The context for the task")
    coworker: str = Field(
        ..., description="The role/name of the coworker to delegate to"
    )
```

#### Campos
1. **task**
   - Tipo: `str`
   - Descrição: A tarefa a ser delegada
   - Obrigatório: Sim
   - Validação: Via Pydantic

2. **context**
   - Tipo: `str`
   - Descrição: Contexto para a tarefa
   - Obrigatório: Sim
   - Uso: Fornece informações de background

3. **coworker**
   - Tipo: `str`
   - Descrição: Agente que receberá a tarefa
   - Obrigatório: Sim
   - Formato: Nome/papel do agente

### 2. Implementação da Ferramenta
```python
class DelegateWorkTool(BaseAgentTool):
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

#### Atributos
1. **name**
   - Valor: "Delegate work to coworker"
   - Uso: Identificador da ferramenta
   - Visibilidade: Para agentes e logs

2. **args_schema**
   - Tipo: `DelegateWorkToolSchema`
   - Propósito: Validação de argumentos
   - Integração: Com Pydantic

## Fluxo de Execução

### 1. Recebimento da Tarefa
```python
def _run(self, task: str, context: str, coworker: Optional[str] = None, **kwargs)
```
- Recebe descrição da tarefa
- Aceita contexto detalhado
- Permite coworker opcional

### 2. Processamento do Coworker
```python
coworker = self._get_coworker(coworker, **kwargs)
```
- Normaliza identificador do coworker
- Suporta múltiplos formatos
- Herda lógica da classe base

### 3. Execução da Delegação
```python
return self._execute(coworker, task, context)
```
- Delega tarefa ao agente
- Gerencia erros
- Retorna resultado

## Casos de Uso

### 1. Delegação Simples
```python
from crewai.tools.agent_tools import DelegateWorkTool

tool = DelegateWorkTool(agents=available_agents)
result = tool.run(
    task="Analyze market data for Q4 2023",
    context="Focus on technology sector trends",
    coworker="data_analyst"
)
```

### 2. Delegação com Contexto Complexo
```python
result = tool.run(
    task="Develop investment strategy",
    context="""
    Market conditions:
    - High volatility
    - Rising interest rates
    - Tech sector correction
    Required: Risk assessment and allocation strategy
    """,
    coworker="portfolio_manager"
)
```

### 3. Delegação com Múltiplos Formatos
```python
# Formato direto
result = tool.run(
    task="Task description",
    context="Context info",
    coworker="analyst"
)

# Formato lista
result = tool.run(
    task="Task description",
    context="Context info",
    coworker="[analyst, researcher]"  # Primeiro será usado
)
```

## Melhores Práticas

### 1. Definição de Tarefas
- Seja claro e específico
- Defina objetivos mensuráveis
- Estabeleça prazos se necessário

### 2. Fornecimento de Contexto
- Inclua informações relevantes
- Estruture dados importantes
- Evite informações desnecessárias

### 3. Seleção de Agentes
- Escolha baseada em capacidades
- Considere carga de trabalho
- Verifique disponibilidade

## Considerações Técnicas

### 1. Performance
- Delegação assíncrona
- Gestão de recursos
- Monitoramento de execução

### 2. Validação
- Schema Pydantic robusto
- Tipos fortemente tipados
- Tratamento de erros abrangente

### 3. Extensibilidade
- Design modular
- Herança bem definida
- Interfaces consistentes

## Exemplos de Implementação

### 1. Sistema de Distribuição de Trabalho
```python
class WorkDistributor:
    def __init__(self, agents):
        self.delegate_tool = DelegateWorkTool(agents=agents)
        
    def distribute_tasks(self, tasks, context):
        results = []
        for task in tasks:
            agent = self.select_best_agent(task)
            result = self.delegate_tool.run(
                task=task.description,
                context=context,
                coworker=agent
            )
            results.append({"task": task, "result": result})
        return results
```

### 2. Pipeline de Processamento
```python
class ProcessingPipeline:
    def __init__(self, agents):
        self.tool = DelegateWorkTool(agents=agents)
        
    def process_data(self, data_chunks):
        processed_results = []
        for chunk in data_chunks:
            result = self.tool.run(
                task="Process data chunk",
                context=str(chunk),
                coworker="data_processor"
            )
            processed_results.append(result)
        return self.aggregate_results(processed_results)
```

### 3. Sistema de Workflow
```python
class WorkflowSystem:
    def __init__(self, agents):
        self.tool = DelegateWorkTool(agents=agents)
        self.workflows = {}
        
    def execute_workflow(self, workflow_name, initial_data):
        workflow = self.workflows[workflow_name]
        current_data = initial_data
        
        for step in workflow:
            result = self.tool.run(
                task=step.task_description,
                context=str(current_data),
                coworker=step.assigned_agent
            )
            current_data = self.update_workflow_data(current_data, result)
            
        return current_data
```

## Conclusão
A ferramenta `DelegateWorkTool` é um componente fundamental do CrewAI para gerenciar a distribuição de trabalho entre agentes. Seu design robusto, validação forte e flexibilidade a tornam essencial para construir sistemas multi-agente eficientes e escaláveis.
