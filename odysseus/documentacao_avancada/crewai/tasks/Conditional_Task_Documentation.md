# Documentação Detalhada: ConditionalTask do CrewAI

## Visão Geral
O `ConditionalTask` é uma extensão especializada da classe `Task` no CrewAI que permite a execução condicional de tarefas baseada em resultados anteriores. Esta classe é fundamental para criar fluxos de trabalho dinâmicos e adaptáveis.

## Implementação

```python
from typing import Any, Callable
from pydantic import Field
from crewai.task import Task
from crewai.tasks.output_format import OutputFormat
from crewai.tasks.task_output import TaskOutput

class ConditionalTask(Task):
    """
    Uma tarefa que pode ser executada condicionalmente baseada na saída de outra tarefa.
    Nota: Esta não pode ser a única tarefa em sua crew e não pode ser a primeira, já que 
    precisa de contexto da tarefa anterior.
    """

    condition: Callable[[TaskOutput], bool] = Field(
        default=None,
        description="Função de condição que determina se a tarefa deve ser executada."
    )

    def __init__(
        self,
        condition: Callable[[Any], bool],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.condition = condition

    def should_execute(self, context: TaskOutput) -> bool:
        return self.condition(context)

    def get_skipped_task_output(self):
        return TaskOutput(
            description=self.description,
            raw="",
            agent=self.agent.role if self.agent else "",
            output_format=OutputFormat.RAW
        )
```

## Análise Detalhada

### 1. Herança e Estrutura
- Herda de `Task`
- Adiciona funcionalidade de execução condicional
- Mantém todas as capacidades da classe base

### 2. Atributos Principais

#### condition
- **Tipo**: `Callable[[TaskOutput], bool]`
- **Propósito**: Define a lógica de execução condicional
- **Características**:
  - Recebe um `TaskOutput` como entrada
  - Retorna um booleano
  - Determina se a tarefa deve ser executada

### 3. Métodos Principais

#### should_execute
```python
def should_execute(self, context: TaskOutput) -> bool:
    return self.condition(context)
```
- **Propósito**: Avalia se a tarefa deve ser executada
- **Parâmetros**:
  - `context`: Resultado da tarefa anterior
- **Retorno**: `True` se a tarefa deve executar, `False` caso contrário

#### get_skipped_task_output
```python
def get_skipped_task_output(self):
    return TaskOutput(
        description=self.description,
        raw="",
        agent=self.agent.role if self.agent else "",
        output_format=OutputFormat.RAW
    )
```
- **Propósito**: Gera uma saída padrão quando a tarefa é pulada
- **Características**:
  - Mantém a descrição original
  - Saída vazia
  - Preserva informação do agente
  - Formato RAW

## Casos de Uso

### 1. Análise de Sentimento Condicional
```python
def check_sentiment(previous_output: TaskOutput) -> bool:
    return "positivo" in previous_output.raw.lower()

sentiment_task = ConditionalTask(
    description="Realizar análise detalhada do sentimento",
    condition=check_sentiment,
    agent=detailed_analyzer
)
```

### 2. Processamento de Dados com Threshold
```python
def check_data_quality(previous_output: TaskOutput) -> bool:
    try:
        data = previous_output.json_dict
        return data.get('quality_score', 0) > 0.8
    except:
        return False

processing_task = ConditionalTask(
    description="Processar dados de alta qualidade",
    condition=check_data_quality,
    agent=data_processor
)
```

### 3. Fluxo de Trabalho Adaptativo
```python
def check_market_conditions(previous_output: TaskOutput) -> bool:
    market_data = previous_output.pydantic
    return (
        market_data.volatility > 0.2 and 
        market_data.volume > 1000000
    )

trading_task = ConditionalTask(
    description="Executar estratégia de alta volatilidade",
    condition=check_market_conditions,
    agent=trading_agent
)
```

## Padrões de Implementação

### 1. Condição Simples
```python
def basic_condition(output: TaskOutput) -> bool:
    return "trigger_word" in output.raw
```

### 2. Condição com Análise Estruturada
```python
def structured_condition(output: TaskOutput) -> bool:
    if output.output_format == OutputFormat.JSON:
        data = output.json_dict
        return data.get('status') == 'success'
    return False
```

### 3. Condição com Múltiplos Critérios
```python
def complex_condition(output: TaskOutput) -> bool:
    try:
        data = output.to_dict()
        return all([
            data.get('score', 0) > 0.7,
            data.get('confidence', 0) > 0.9,
            data.get('errors', []) == []
        ])
    except:
        return False
```

## Melhores Práticas

### 1. Tratamento de Erros
```python
def safe_condition(output: TaskOutput) -> bool:
    try:
        # Lógica principal
        return True
    except Exception as e:
        logger.warning(f"Erro na condição: {e}")
        return False
```

### 2. Documentação Clara
```python
def well_documented_condition(output: TaskOutput) -> bool:
    """
    Verifica se os critérios de qualidade são atendidos.
    
    Args:
        output: Resultado da tarefa anterior
        
    Returns:
        bool: True se critérios atendidos, False caso contrário
    """
    # Implementação
    pass
```

### 3. Condições Compostas
```python
def create_combined_condition(*conditions):
    def combined_condition(output: TaskOutput) -> bool:
        return all(c(output) for c in conditions)
    return combined_condition
```

## Integração com o Sistema

### 1. Encadeamento de Tarefas
```python
crew = Crew(
    tasks=[
        Task(description="Coletar dados"),
        ConditionalTask(
            description="Analisar dados",
            condition=lambda x: len(x.raw) > 0
        ),
        ConditionalTask(
            description="Gerar relatório",
            condition=lambda x: "análise completa" in x.raw
        )
    ]
)
```

### 2. Feedback Loop
```python
def create_feedback_loop(threshold: float):
    def feedback_condition(output: TaskOutput) -> bool:
        score = float(output.raw)
        return score < threshold
    
    return ConditionalTask(
        description="Refinar resultado",
        condition=feedback_condition
    )
```

## Considerações de Performance

### 1. Complexidade da Condição
- Mantenha condições simples e eficientes
- Evite operações pesadas dentro da condição
- Cache resultados intermediários quando possível

### 2. Gestão de Recursos
- Libere recursos em caso de skip
- Evite processamento desnecessário
- Considere timeout para condições complexas

### 3. Logging e Monitoramento
```python
def monitored_condition(output: TaskOutput) -> bool:
    start_time = time.time()
    result = actual_condition(output)
    duration = time.time() - start_time
    
    logger.info(f"Condição avaliada em {duration}s: {result}")
    return result
```

## Extensibilidade

### 1. Condições Parametrizadas
```python
class ParameterizedCondition:
    def __init__(self, threshold: float):
        self.threshold = threshold
    
    def __call__(self, output: TaskOutput) -> bool:
        return float(output.raw) > self.threshold
```

### 2. Condições Compostas
```python
class CompositeCondition:
    def __init__(self, conditions: List[Callable]):
        self.conditions = conditions
    
    def __call__(self, output: TaskOutput) -> bool:
        return all(c(output) for c in self.conditions)
```

## Conclusão

O `ConditionalTask` é uma implementação poderosa que permite criar fluxos de trabalho dinâmicos e adaptáveis no CrewAI. Sua flexibilidade em aceitar funções de condição personalizadas, combinada com a capacidade de integração com o sistema de saída estruturado do CrewAI, torna-o uma ferramenta versátil para construção de pipelines de processamento complexos.

A classe demonstra um equilíbrio entre simplicidade de uso e poder de expressão, permitindo implementações desde simples verificações de texto até complexas análises de dados estruturados. Sua integração com o sistema de tipos do Python e o framework Pydantic garante segurança e previsibilidade no processamento condicional de tarefas.
