# Documentação do Base Tool

## Visão Geral
O módulo `base_tool.py` fornece a estrutura base para criar ferramentas no CrewAI. Ele define duas classes principais:
- `BaseTool`: Classe abstrata base para todas as ferramentas
- `Tool`: Implementação concreta que executa uma função fornecida

## Classe BaseTool

### Atributos
- `name` (str): Nome único da ferramenta que comunica claramente seu propósito
- `description` (str): Descrição de como/quando/por que usar a ferramenta
- `args_schema` (PydanticBaseModel): Schema para os argumentos que a ferramenta aceita
- `description_updated` (bool): Flag para verificar se a descrição foi atualizada
- `cache_function` (Callable): Função para determinar se a ferramenta deve ser cacheada
- `result_as_answer` (bool): Flag para indicar se o resultado deve ser a resposta final do agente

### Métodos Principais

#### `run(*args, **kwargs)`
Método público que executa a ferramenta, imprimindo uma mensagem de uso e chamando o método `_run`.

#### `_run(*args, **kwargs)`
Método abstrato que deve ser implementado pelas subclasses com a lógica real da ferramenta.

#### `to_structured_tool()`
Converte a ferramenta em uma instância de `CrewStructuredTool`.

#### `from_langchain(tool)`
Método de classe para criar uma ferramenta a partir de uma ferramenta LangChain.

#### `_set_args_schema()`
Configura o schema de argumentos da ferramenta.

#### `_generate_description()`
Gera uma descrição formatada da ferramenta incluindo nome, argumentos e descrição.

## Classe Tool

### Atributos Adicionais
- `func` (Callable): A função que será executada quando a ferramenta for chamada

### Métodos

#### `_run(*args, **kwargs)`
Implementa o método abstrato executando a função armazenada em `func`.

#### `from_langchain(tool)`
Implementação específica para converter uma ferramenta LangChain em uma Tool.

## Funções Utilitárias

### `to_langchain(tools)`
Converte uma lista de ferramentas CrewAI em ferramentas LangChain.

### `@tool`
Decorador para criar uma ferramenta a partir de uma função. Pode ser usado de duas formas:
1. `@tool` - Usa o nome da função como nome da ferramenta
2. `@tool("nome")` - Usa o nome fornecido como nome da ferramenta

## Exemplo de Uso

```python
from crewai.tools import tool

@tool("calculadora")
def calculadora(x: float, y: float) -> float:
    """Calcula a soma de dois números."""
    return x + y

# Ou usando a classe Tool diretamente
from crewai.tools import Tool

def multiplicar(x: float, y: float) -> float:
    """Multiplica dois números."""
    return x * y

multiplicador = Tool(
    name="multiplicador",
    description="Multiplica dois números",
    func=multiplicar
)
```

## Notas Importantes
1. Todas as ferramentas devem ter um nome único e descritivo
2. A descrição deve ser clara sobre como, quando e por que usar a ferramenta
3. Os argumentos devem ser tipados usando type hints do Python
4. A função deve ter uma docstring descritiva
5. O cache pode ser personalizado através da `cache_function`
