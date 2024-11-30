# Base Tool - Documentação Detalhada

## Visão Geral
O arquivo `base_tool.py` define a estrutura fundamental para todas as ferramentas no framework CrewAI. Esta classe abstrata serve como base para implementação de ferramentas personalizadas e fornece integração com o ecossistema LangChain.

## Estrutura da Classe

### Classe BaseTool

```python
class BaseTool(BaseModel, ABC):
    name: str
    description: str
    args_schema: Type[PydanticBaseModel]
    description_updated: bool = False
    cache_function: Callable = lambda _args=None, _result=None: True
    result_as_answer: bool = False
```

#### Atributos Principais

1. **name** (str)
   - Nome único da ferramenta
   - Deve comunicar claramente seu propósito
   - Usado para identificação no sistema

2. **description** (str)
   - Descrição detalhada da ferramenta
   - Utilizada pelo modelo para entender quando/como usar a ferramenta
   - Automaticamente formatada com informações do schema

3. **args_schema** (Type[PydanticBaseModel])
   - Define a estrutura dos argumentos aceitos pela ferramenta
   - Gerado automaticamente a partir das anotações de tipo do método `_run`
   - Utiliza Pydantic para validação de dados

4. **cache_function** (Callable)
   - Função para controle de cache
   - Determina se o resultado deve ser armazenado em cache
   - Padrão: sempre retorna True

5. **result_as_answer** (bool)
   - Flag para indicar se o resultado deve ser a resposta final do agente
   - Útil para ferramentas que geram respostas conclusivas

## Métodos Principais

### 1. run()
```python
def run(self, *args: Any, **kwargs: Any) -> Any:
    print(f"Using Tool: {self.name}")
    return self._run(*args, **kwargs)
```
- Método público para execução da ferramenta
- Adiciona logging automático
- Delega a execução real para `_run`

### 2. _run() [Abstrato]
```python
@abstractmethod
def _run(self, *args: Any, **kwargs: Any) -> Any:
    """Here goes the actual implementation of the tool."""
```
- Método abstrato que deve ser implementado por subclasses
- Contém a lógica específica da ferramenta
- Deve processar os argumentos e retornar um resultado

### 3. to_langchain()
```python
def to_langchain(self) -> StructuredTool:
    self._set_args_schema()
    return StructuredTool(
        name=self.name,
        description=self.description,
        args_schema=self.args_schema,
        func=self._run,
    )
```
- Converte a ferramenta para formato LangChain
- Permite integração com o ecossistema LangChain
- Mantém compatibilidade com ferramentas existentes

## Recursos Avançados

### 1. Validação de Schema
```python
@validator("args_schema", always=True, pre=True)
def _default_args_schema(cls, v: Type[PydanticBaseModel]) -> Type[PydanticBaseModel]:
```
- Validação automática de argumentos
- Geração de schema baseada em anotações de tipo
- Suporte a tipos complexos e aninhados

### 2. Geração de Descrição
```python
def _generate_description(self):
    args_schema = {
        name: {
            "description": field.description,
            "type": BaseTool._get_arg_annotations(field.annotation),
        }
        for name, field in self.args_schema.model_fields.items()
    }
```
- Geração automática de descrição rica
- Inclui informações sobre argumentos
- Facilita o entendimento pelo modelo de IA

## Decorador @tool

```python
def tool(*args):
    """Decorator to create a tool from a function."""
```

### Características
- Simplifica a criação de ferramentas
- Suporta nomeação explícita
- Gera schema automaticamente

### Uso
```python
@tool
def minha_ferramenta(param: str) -> str:
    """Descrição da ferramenta"""
    return f"Resultado: {param}"

# OU

@tool("nome_personalizado")
def minha_ferramenta(param: str) -> str:
    """Descrição da ferramenta"""
    return f"Resultado: {param}"
```

## Melhores Práticas

### 1. Implementação de Ferramentas
- Mantenha o método `_run` focado e atômico
- Documente claramente os parâmetros esperados
- Implemente tratamento adequado de erros

### 2. Uso de Cache
- Configure `cache_function` apropriadamente
- Considere o custo de execução
- Implemente invalidação quando necessário

### 3. Documentação
- Forneça descrições claras e detalhadas
- Documente tipos de argumentos
- Inclua exemplos de uso quando relevante

## Exemplo de Implementação

```python
class MinhaFerramentaPersonalizada(BaseTool):
    name = "minha_ferramenta"
    description = "Descrição detalhada da ferramenta"
    
    def _run(self, input_text: str, max_length: int = 100) -> str:
        """
        Processa o texto de entrada.
        
        Args:
            input_text: Texto para processar
            max_length: Comprimento máximo do resultado
            
        Returns:
            str: Texto processado
        """
        # Implementação
        resultado = process_text(input_text, max_length)
        return resultado
```

## Considerações de Design

### 1. Extensibilidade
- Design modular permite fácil extensão
- Suporte a tipos personalizados
- Integração com sistemas externos

### 2. Validação
- Validação robusta de argumentos
- Conversão automática de tipos
- Tratamento de erros consistente

### 3. Performance
- Sistema de cache integrado
- Execução eficiente
- Baixo overhead

## Conclusão
O `base_tool.py` fornece uma base sólida e flexível para a criação de ferramentas no CrewAI. Sua arquitetura bem pensada permite a criação de ferramentas robustas e fáceis de usar, mantendo compatibilidade com o ecossistema LangChain e fornecendo recursos avançados como cache e validação automática de argumentos.
