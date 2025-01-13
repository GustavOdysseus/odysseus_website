# Structured Tool - Documentação Detalhada

## Visão Geral
A classe `CrewStructuredTool` é uma implementação especializada que estende o conceito de ferramentas estruturadas do LangChain, adaptando-as para o ecossistema CrewAI. Esta ferramenta oferece uma interface mais rica e funcionalidades adicionais.

## Características Principais

### Estrutura Base
```python
class CrewStructuredTool:
    def __init__(
        self,
        name: str,
        description: str,
        args_schema: type[BaseModel],
        func: Callable[..., Any],
        result_as_answer: bool = False,
    ):
        self.name = name
        self.description = description
        self.args_schema = args_schema
        self.func = func
        self._logger = Logger()
        self.result_as_answer = result_as_answer
```

## Funcionalidades

### 1. Criação a partir de Funções
```python
@classmethod
def from_function(
    cls,
    func: Callable,
    name: Optional[str] = None,
    description: Optional[str] = None,
    return_direct: bool = False,
    args_schema: Optional[type[BaseModel]] = None,
    infer_schema: bool = True,
    **kwargs: Any,
) -> CrewStructuredTool:
```

#### Exemplo de Uso
```python
def calcular_media(valores: list[float]) -> float:
    """Calcula a média de uma lista de valores."""
    return sum(valores) / len(valores)

ferramenta = CrewStructuredTool.from_function(
    func=calcular_media,
    name="calculadora_media",
    description="Calcula média de valores"
)
```

### 2. Schema Automático
O sistema gera automaticamente schemas Pydantic baseados na assinatura da função:

```python
@staticmethod
def _create_schema_from_function(
    name: str,
    func: Callable,
) -> type[BaseModel]:
    # Obtém assinatura da função
    sig = inspect.signature(func)
    # Obtém type hints
    type_hints = get_type_hints(func)
    
    # Cria definições de campos
    fields = {}
    for param_name, param in sig.parameters.items():
        if param_name in ("self", "cls"):
            continue
            
        annotation = type_hints.get(param_name, Any)
        default = ... if param.default == param.empty else param.default
        fields[param_name] = (annotation, Field(default=default))
        
    # Cria modelo
    schema_name = f"{name.title()}Schema"
    return create_model(schema_name, **fields)
```

### 3. Execução Assíncrona
```python
async def ainvoke(
    self,
    input: Union[str, dict],
    config: Optional[dict] = None,
    **kwargs: Any,
) -> Any:
    parsed_args = self._parse_args(input)
    
    if inspect.iscoroutinefunction(self.func):
        return await self.func(**parsed_args, **kwargs)
    else:
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: self.func(**parsed_args, **kwargs)
        )
```

## Validação e Parsing

### 1. Validação de Argumentos
```python
def _parse_args(self, raw_args: Union[str, dict]) -> dict:
    """Parse e valida argumentos de entrada."""
    if isinstance(raw_args, str):
        try:
            raw_args = json.loads(raw_args)
        except json.JSONDecodeError as e:
            raise ValueError(f"Falha ao parsear JSON: {e}")
            
    try:
        validated_args = self.args_schema.model_validate(raw_args)
        return validated_args.model_dump()
    except Exception as e:
        raise ValueError(f"Validação falhou: {e}")
```

### 2. Validação de Assinatura
```python
def _validate_function_signature(self) -> None:
    """Valida que a assinatura da função corresponde ao schema."""
    sig = inspect.signature(self.func)
    schema_fields = self.args_schema.model_fields
    
    for param_name, param in sig.parameters.items():
        if param_name in ("self", "cls"):
            continue
            
        if param.kind in (
            inspect.Parameter.VAR_KEYWORD,
            inspect.Parameter.VAR_POSITIONAL,
        ):
            continue
            
        if param.default == inspect.Parameter.empty:
            if param_name not in schema_fields:
                raise ValueError(
                    f"Parâmetro obrigatório '{param_name}' "
                    f"não encontrado no schema"
                )
```

## Padrões de Uso

### 1. Ferramenta Básica
```python
def processar_texto(texto: str, max_length: int = 100) -> str:
    """Processa e limita tamanho do texto."""
    return texto[:max_length]

ferramenta = CrewStructuredTool.from_function(
    func=processar_texto,
    name="processador_texto",
    description="Processa e limita textos"
)
```

### 2. Com Schema Personalizado
```python
class ProcessadorSchema(BaseModel):
    texto: str = Field(..., description="Texto para processar")
    max_length: int = Field(
        default=100,
        description="Tamanho máximo"
    )

ferramenta = CrewStructuredTool(
    name="processador",
    description="Processa textos",
    args_schema=ProcessadorSchema,
    func=processar_texto
)
```

### 3. Execução Assíncrona
```python
async def processar_async(texto: str) -> str:
    await asyncio.sleep(1)  # Simulação de operação async
    return texto.upper()

ferramenta = CrewStructuredTool.from_function(
    func=processar_async,
    name="processador_async",
    description="Processamento assíncrono"
)

# Uso
resultado = await ferramenta.ainvoke({"texto": "teste"})
```

## Melhores Práticas

### 1. Definição de Schemas
- Use tipos apropriados
- Documente campos
- Defina valores padrão

### 2. Funções
- Mantenha funções puras
- Use type hints
- Documente comportamento

### 3. Execução
- Use async quando apropriado
- Trate erros adequadamente
- Valide entradas

## Considerações Técnicas

### 1. Performance
- Validação eficiente
- Execução otimizada
- Cache quando possível

### 2. Compatibilidade
- Suporte a LangChain
- Integração com CrewAI
- Extensibilidade

### 3. Segurança
- Validação de entrada
- Sanitização
- Limites de execução

## Conclusão
A `CrewStructuredTool` fornece uma implementação robusta e flexível para ferramentas estruturadas no CrewAI. Seu design permite fácil criação e uso de ferramentas, mantendo segurança e performance.
