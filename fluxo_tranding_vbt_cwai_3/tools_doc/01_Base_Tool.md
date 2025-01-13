# Base Tool - Documentação Detalhada

## Visão Geral
A classe `BaseTool` é o componente fundamental do sistema de ferramentas do CrewAI. Ela define a interface e funcionalidades básicas que todas as ferramentas devem implementar.

## Estrutura Base

### Atributos Principais
```python
class BaseTool(BaseModel, ABC):
    name: str
    description: str
    args_schema: Type[PydanticBaseModel]
    description_updated: bool = False
    cache_function: Callable = lambda _args=None, _result=None: True
    result_as_answer: bool = False
```

#### Descrição dos Atributos
- **name**: Nome único que identifica a ferramenta
- **description**: Descrição detalhada da funcionalidade
- **args_schema**: Schema Pydantic para validação de argumentos
- **description_updated**: Flag para controle de atualização da descrição
- **cache_function**: Função para controle de cache
- **result_as_answer**: Flag para indicar se o resultado é resposta final

## Funcionalidades Principais

### 1. Execução de Ferramentas
```python
def run(self, *args: Any, **kwargs: Any) -> Any:
    """Método público para execução da ferramenta."""
    print(f"Using Tool: {self.name}")
    return self._run(*args, **kwargs)

@abstractmethod
def _run(self, *args: Any, **kwargs: Any) -> Any:
    """Implementação específica da ferramenta."""
```

### 2. Validação de Argumentos
O sistema utiliza Pydantic para validação automática:
- Tipos de dados
- Valores obrigatórios
- Valores padrão
- Conversões automáticas

### 3. Sistema de Cache
```python
cache_function: Callable = lambda _args=None, _result=None: True
```
- Controle granular de cache
- Função customizável por ferramenta
- Otimização de performance

## Criando Novas Ferramentas

### 1. Herança Básica
```python
class MinhaFerramenta(BaseTool):
    name = "nome_ferramenta"
    description = "Descrição detalhada"
    
    def _run(self, *args, **kwargs):
        # Implementação
        pass
```

### 2. Com Schema Personalizado
```python
class MinhaFerramentaSchema(BaseModel):
    param1: str = Field(..., description="Descrição do parâmetro")
    param2: int = Field(default=10, description="Parâmetro opcional")

class MinhaFerramenta(BaseTool):
    name = "nome_ferramenta"
    description = "Descrição detalhada"
    args_schema = MinhaFerramentaSchema
    
    def _run(self, param1: str, param2: int = 10):
        # Implementação
        pass
```

### 3. Com Cache Personalizado
```python
class MinhaFerramenta(BaseTool):
    name = "nome_ferramenta"
    description = "Descrição detalhada"
    
    def cache_function(self, args, result):
        # Lógica personalizada de cache
        return should_cache
        
    def _run(self, *args, **kwargs):
        # Implementação
        pass
```

## Integração com LangChain

### 1. Conversão para LangChain
```python
def to_structured_tool(self) -> CrewStructuredTool:
    """Converte para formato LangChain."""
    self._set_args_schema()
    return CrewStructuredTool(
        name=self.name,
        description=self.description,
        args_schema=self.args_schema,
        func=self._run
    )
```

### 2. Importação de LangChain
```python
@classmethod
def from_langchain(cls, tool: Any) -> "BaseTool":
    """Cria ferramenta a partir de LangChain."""
    if not hasattr(tool, "func"):
        raise ValueError("Tool must have func attribute")
        
    return cls(
        name=tool.name,
        description=tool.description,
        func=tool.func,
        args_schema=tool.args_schema
    )
```

## Melhores Práticas

### 1. Nomeação
- Use nomes descritivos e únicos
- Siga padrões consistentes
- Evite caracteres especiais

### 2. Descrições
- Seja detalhado e claro
- Inclua exemplos de uso
- Documente todos os parâmetros

### 3. Implementação
- Mantenha métodos focados
- Implemente tratamento de erros
- Considere performance

### 4. Cache
- Use cache apropriadamente
- Implemente invalidação
- Monitore uso de memória

## Considerações Técnicas

### 1. Performance
- Validação eficiente
- Cache inteligente
- Otimização de memória

### 2. Segurança
- Validação de entrada
- Sanitização de dados
- Controle de acesso

### 3. Extensibilidade
- Design modular
- Interfaces claras
- Baixo acoplamento

## Exemplos Completos

### 1. Ferramenta Básica
```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class CalculadoraSchema(BaseModel):
    operacao: str = Field(..., description="Operação matemática")
    valores: list[float] = Field(..., description="Lista de valores")

class Calculadora(BaseTool):
    name = "calculadora"
    description = "Executa operações matemáticas básicas"
    args_schema = CalculadoraSchema
    
    def _run(self, operacao: str, valores: list[float]):
        if operacao == "soma":
            return sum(valores)
        elif operacao == "media":
            return sum(valores) / len(valores)
        else:
            raise ValueError(f"Operação não suportada: {operacao}")
```

### 2. Ferramenta com Cache
```python
class ProcessadorDados(BaseTool):
    name = "processador_dados"
    description = "Processa conjunto de dados"
    
    def cache_function(self, args, result):
        # Cache apenas para conjuntos grandes
        return len(args.get("dados", [])) > 1000
        
    def _run(self, dados: list[dict]):
        return self._processar(dados)
```

## Conclusão
A classe `BaseTool` fornece uma base sólida e flexível para a criação de ferramentas no CrewAI. Sua arquitetura bem pensada permite a criação de ferramentas robustas e fáceis de usar, mantendo compatibilidade com o ecossistema LangChain e fornecendo recursos avançados como cache e validação automática de argumentos.
