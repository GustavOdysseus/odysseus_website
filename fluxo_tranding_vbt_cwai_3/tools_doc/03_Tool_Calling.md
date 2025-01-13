# Tool Calling - Documentação Detalhada

## Visão Geral
O sistema de chamadas de ferramentas no CrewAI é responsável por gerenciar como as ferramentas são invocadas pelos agentes. Este sistema é composto por duas classes principais: `ToolCalling` e `InstructorToolCalling`.

## Componentes Principais

### 1. ToolCalling
```python
class ToolCalling(BaseModel):
    tool_name: str = Field(
        ..., 
        description="Nome da ferramenta a ser chamada"
    )
    arguments: Optional[Dict[str, Any]] = Field(
        ..., 
        description="Dicionário de argumentos para a ferramenta"
    )
```

### 2. InstructorToolCalling
```python
class InstructorToolCalling(PydanticBaseModel):
    tool_name: str = PydanticField(
        ..., 
        description="Nome da ferramenta a ser chamada"
    )
    arguments: Optional[Dict[str, Any]] = PydanticField(
        ..., 
        description="Dicionário de argumentos para a ferramenta"
    )
```

## Funcionalidades

### 1. Validação de Chamadas
- Verificação de nome da ferramenta
- Validação de argumentos
- Compatibilidade de tipos

### 2. Formatos de Chamada
#### Formato Padrão
```python
{
    "tool_name": "nome_ferramenta",
    "arguments": {
        "arg1": "valor1",
        "arg2": 123
    }
}
```

#### Formato Instructor
```python
{
    "tool_name": "nome_ferramenta",
    "arguments": {
        "input": "dados",
        "config": {"opcao": "valor"}
    }
}
```

## Uso do Sistema

### 1. Chamada Básica
```python
chamada = ToolCalling(
    tool_name="calculadora",
    arguments={
        "operacao": "soma",
        "valores": [1, 2, 3]
    }
)
```

### 2. Chamada com Instructor
```python
chamada = InstructorToolCalling(
    tool_name="processador",
    arguments={
        "input": "texto para processar",
        "config": {
            "max_length": 100,
            "formato": "json"
        }
    }
)
```

## Integração com Tool Usage

### 1. Parsing de Chamadas
```python
def parse_tool_call(tool_string: str) -> ToolCalling:
    """Parse string de chamada para objeto ToolCalling."""
    try:
        parsed = json.loads(tool_string)
        return ToolCalling(
            tool_name=parsed["tool_name"],
            arguments=parsed["arguments"]
        )
    except Exception as e:
        raise ValueError(f"Erro no parsing: {e}")
```

### 2. Execução de Chamadas
```python
def execute_tool_call(calling: ToolCalling) -> Any:
    """Executa uma chamada de ferramenta."""
    tool = find_tool(calling.tool_name)
    return tool.run(**calling.arguments)
```

## Tratamento de Erros

### 1. Validação de Entrada
```python
def validate_tool_call(calling: ToolCalling) -> bool:
    """Valida uma chamada de ferramenta."""
    if not calling.tool_name:
        raise ValueError("Nome da ferramenta é obrigatório")
        
    if calling.arguments is None:
        calling.arguments = {}
        
    return True
```

### 2. Tratamento de Exceções
```python
try:
    result = execute_tool_call(calling)
except ToolNotFoundError:
    handle_tool_not_found()
except InvalidArgumentsError:
    handle_invalid_arguments()
except Exception as e:
    handle_general_error(e)
```

## Melhores Práticas

### 1. Nomeação de Ferramentas
- Use nomes descritivos
- Mantenha consistência
- Evite caracteres especiais

### 2. Argumentos
- Valide tipos
- Use valores padrão
- Documente requisitos

### 3. Tratamento de Erros
- Valide entradas
- Forneça mensagens claras
- Log apropriado

## Considerações Técnicas

### 1. Performance
- Parsing eficiente
- Validação otimizada
- Cache de resultados

### 2. Segurança
- Validação de entrada
- Sanitização
- Controle de acesso

### 3. Extensibilidade
- Design modular
- Interfaces claras
- Versionamento

## Exemplos Completos

### 1. Sistema de Processamento
```python
class ProcessamentoSystem:
    def __init__(self):
        self.tools = load_tools()
        
    def process_call(self, call_string: str) -> Any:
        # Parse chamada
        calling = parse_tool_call(call_string)
        
        # Valida
        validate_tool_call(calling)
        
        # Executa
        return execute_tool_call(calling)
```

### 2. Sistema com Cache
```python
class CachedToolCalling:
    def __init__(self):
        self.cache = {}
        
    def execute(self, calling: ToolCalling) -> Any:
        # Verifica cache
        cache_key = self._make_cache_key(calling)
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        # Executa e cache
        result = execute_tool_call(calling)
        self.cache[cache_key] = result
        return result
```

## Conclusão
O sistema de chamadas de ferramentas do CrewAI fornece uma interface robusta e flexível para a invocação de ferramentas. Sua implementação cuida de aspectos críticos como validação, tratamento de erros e extensibilidade, permitindo uma integração segura e eficiente com o resto do sistema.
