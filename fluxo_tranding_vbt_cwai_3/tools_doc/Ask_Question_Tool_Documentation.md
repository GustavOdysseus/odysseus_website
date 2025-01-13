# Ask Question Tool - Documentação Detalhada

## Visão Geral
O arquivo `ask_question_tool.py` implementa a ferramenta `AskQuestionTool`, que permite a comunicação entre agentes através de perguntas e respostas no CrewAI. Esta ferramenta é fundamental para permitir que agentes obtenham informações uns dos outros de forma estruturada.

## Estrutura do Código

### 1. Schema de Validação
```python
class AskQuestionToolSchema(BaseModel):
    question: str = Field(..., description="The question to ask")
    context: str = Field(..., description="The context for the question")
    coworker: str = Field(..., description="The role/name of the coworker to ask")
```

#### Campos
1. **question**
   - Tipo: `str`
   - Descrição: A pergunta a ser feita
   - Obrigatório: Sim
   - Validação: Via Pydantic

2. **context**
   - Tipo: `str`
   - Descrição: Contexto para a pergunta
   - Obrigatório: Sim
   - Uso: Fornece background necessário

3. **coworker**
   - Tipo: `str`
   - Descrição: Identificador do agente alvo
   - Obrigatório: Sim
   - Formato: Nome/papel do agente

### 2. Implementação da Ferramenta
```python
class AskQuestionTool(BaseAgentTool):
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

#### Atributos
1. **name**
   - Valor: "Ask question to coworker"
   - Uso: Identificador da ferramenta
   - Visibilidade: Para agentes e logs

2. **args_schema**
   - Tipo: `AskQuestionToolSchema`
   - Propósito: Validação de argumentos
   - Integração: Com Pydantic

## Fluxo de Execução

### 1. Recebimento da Pergunta
```python
def _run(self, question: str, context: str, coworker: Optional[str] = None, **kwargs)
```
- Recebe pergunta e contexto
- Aceita coworker opcional
- Suporta argumentos adicionais

### 2. Processamento do Coworker
```python
coworker = self._get_coworker(coworker, **kwargs)
```
- Normaliza nome do coworker
- Lida com formatos diferentes
- Herda lógica da classe base

### 3. Execução
```python
return self._execute(coworker, question, context)
```
- Delega execução à classe base
- Gerencia erros
- Retorna resposta

## Casos de Uso

### 1. Pergunta Simples
```python
from crewai.tools.agent_tools import AskQuestionTool

tool = AskQuestionTool(agents=available_agents)
response = tool.run(
    question="What is the current market trend?",
    context="Financial analysis for Q4 2023",
    coworker="market_analyst"
)
```

### 2. Com Contexto Detalhado
```python
response = tool.run(
    question="Should we invest in this sector?",
    context="""
    Recent market analysis shows:
    - Growth rate: 15%
    - Risk factor: Medium
    - Market cap: $2B
    Please provide investment recommendation.
    """,
    coworker="investment_advisor"
)
```

### 3. Múltiplos Formatos de Coworker
```python
# Formato direto
response = tool.run(
    question="Query?",
    context="Context",
    coworker="analyst"
)

# Formato lista
response = tool.run(
    question="Query?",
    context="Context",
    coworker="[analyst, researcher]"  # Primeiro será usado
)
```

## Melhores Práticas

### 1. Formulação de Perguntas
- Seja específico e claro
- Forneça contexto relevante
- Evite ambiguidades

### 2. Gestão de Contexto
- Inclua informações necessárias
- Mantenha concisão
- Estruture logicamente

### 3. Seleção de Coworker
- Escolha agente apropriado
- Verifique disponibilidade
- Considere especialização

## Considerações Técnicas

### 1. Performance
- Processamento assíncrono
- Gestão de recursos
- Timeout apropriado

### 2. Validação
- Schema Pydantic
- Tipos estáticos
- Tratamento de erros

### 3. Extensibilidade
- Design modular
- Herança clara
- Interfaces consistentes

## Exemplos de Implementação

### 1. Sistema de Consulta
```python
class QuerySystem:
    def __init__(self, agents):
        self.question_tool = AskQuestionTool(agents=agents)
        
    def ask_expert(self, question, expert_role, analysis_context):
        return self.question_tool.run(
            question=question,
            context=analysis_context,
            coworker=expert_role
        )
```

### 2. Sistema de Análise Colaborativa
```python
class CollaborativeAnalysis:
    def __init__(self, agents):
        self.tool = AskQuestionTool(agents=agents)
        
    def analyze_with_experts(self, data, experts):
        insights = []
        for expert in experts:
            response = self.tool.run(
                question="What insights can you provide from this data?",
                context=str(data),
                coworker=expert
            )
            insights.append({"expert": expert, "insight": response})
        return insights
```

### 3. Sistema de Validação Cruzada
```python
class CrossValidation:
    def __init__(self, agents):
        self.tool = AskQuestionTool(agents=agents)
        
    def validate_analysis(self, analysis, validators):
        validations = []
        for validator in validators:
            response = self.tool.run(
                question="Is this analysis correct and complete?",
                context=analysis,
                coworker=validator
            )
            validations.append({"validator": validator, "feedback": response})
        return validations
```

## Conclusão
A ferramenta `AskQuestionTool` é um componente essencial do CrewAI para facilitar a comunicação entre agentes. Seu design robusto, validação forte e flexibilidade a tornam ideal para construir sistemas multi-agente colaborativos e eficientes.
