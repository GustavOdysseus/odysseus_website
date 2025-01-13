# Documentação do Structured Tool

## Visão Geral
O módulo `structured_tool.py` define a classe `CrewStructuredTool`, que fornece uma implementação estruturada de ferramentas com validação de argumentos e execução flexível. Esta ferramenta foi projetada para substituir o `StructuredTool` com uma implementação personalizada que se integra melhor com o ecossistema CrewAI.

## Classe CrewStructuredTool

### Atributos
- `name` (str): Nome da ferramenta
- `description` (str): Descrição do que a ferramenta faz
- `args_schema` (BaseModel): Schema Pydantic para os argumentos da ferramenta
- `func` (Callable): Função a ser executada quando a ferramenta é chamada
- `result_as_answer` (bool): Se deve retornar a saída diretamente
- `_logger` (Logger): Logger para a ferramenta

### Métodos Principais

#### `__init__(name, description, args_schema, func, result_as_answer=False)`
Inicializa a ferramenta estruturada com os parâmetros necessários e valida a assinatura da função.

#### `from_function(func, name=None, description=None, return_direct=False, args_schema=None, infer_schema=True, **kwargs)`
Método de classe para criar uma ferramenta a partir de uma função.

Exemplo:
```python
def add(a: int, b: int) -> int:
    '''Add two numbers'''
    return a + b

tool = CrewStructuredTool.from_function(add)
```

#### `invoke(input, config=None, **kwargs)`
Método principal para execução da ferramenta. Processa os argumentos e executa a função.

#### `ainvoke(input, config=None, **kwargs)`
Versão assíncrona do método `invoke`. Suporta tanto funções síncronas quanto assíncronas.

### Métodos Auxiliares

#### `_create_schema_from_function(name, func)`
Cria um schema Pydantic a partir da assinatura da função.

#### `_validate_function_signature()`
Valida se a assinatura da função corresponde ao schema de argumentos.

#### `_parse_args(raw_args)`
Processa e valida os argumentos de entrada contra o schema.

#### `args`
Propriedade que retorna o schema de argumentos de entrada da ferramenta.

## Exemplo de Uso

```python
from crewai.tools import CrewStructuredTool
from pydantic import BaseModel

# Definindo um schema de argumentos
class CalculatorSchema(BaseModel):
    x: float
    y: float

def calculator(x: float, y: float) -> float:
    """Calcula a soma de dois números."""
    return x + y

# Criando a ferramenta
tool = CrewStructuredTool(
    name="calculadora",
    description="Calcula a soma de dois números",
    args_schema=CalculatorSchema,
    func=calculator
)

# Usando a ferramenta
result = tool.invoke({"x": 5, "y": 3})  # Retorna 8

# Usando de forma assíncrona
async def main():
    result = await tool.ainvoke({"x": 5, "y": 3})
    print(result)  # 8
```

## Notas Importantes
1. A ferramenta valida automaticamente os argumentos usando o schema Pydantic
2. Suporta tanto funções síncronas quanto assíncronas
3. Pode inferir o schema de argumentos a partir da assinatura da função
4. Fornece mensagens de erro claras para argumentos inválidos
5. Integra-se bem com o sistema de logging do CrewAI
