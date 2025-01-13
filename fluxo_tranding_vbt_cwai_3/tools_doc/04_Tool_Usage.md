# Tool Usage - Documentação Detalhada

## Visão Geral
O sistema de uso de ferramentas (`ToolUsage`) é responsável por gerenciar todo o ciclo de vida da execução de ferramentas no CrewAI. Ele lida com aspectos como parsing de chamadas, execução, cache, telemetria e tratamento de erros.

## Arquitetura

### Componentes Principais
```python
class ToolUsage:
    def __init__(
        self,
        tools_handler: ToolsHandler,
        tools: List[BaseTool],
        original_tools: List[Any],
        tools_description: str,
        tools_names: str,
        task: Task,
        function_calling_llm: Any,
        agent: Any,
        action: Any,
    ):
        self._i18n: I18N = agent.i18n
        self._printer: Printer = Printer()
        self._telemetry: Telemetry = Telemetry()
        self._run_attempts: int = 1
        self._max_parsing_attempts: int = 3
        self._remember_format_after_usages: int = 3
```

## Funcionalidades Principais

### 1. Execução de Ferramentas
```python
def use(
    self,
    calling: Union[ToolCalling, InstructorToolCalling],
    tool_string: str
) -> Any:
    """Executa uma ferramenta com base na chamada."""
    tool = self._select_tool(calling.tool_name)
    return self._use(tool_string, tool, calling)
```

### 2. Sistema de Cache
```python
def _check_cache(self, tool: BaseTool, args: Dict[str, Any]) -> Optional[Any]:
    """Verifica cache para argumentos específicos."""
    cache_key = self._make_cache_key(tool, args)
    return self.cache.get(cache_key)

def _update_cache(self, tool: BaseTool, args: Dict[str, Any], result: Any):
    """Atualiza cache com novo resultado."""
    if tool.cache_function(args, result):
        cache_key = self._make_cache_key(tool, args)
        self.cache[cache_key] = result
```

### 3. Telemetria e Eventos
```python
def on_tool_use_finished(
    self,
    tool: Any,
    tool_calling: ToolCalling,
    from_cache: bool,
    started_at: float
) -> None:
    """Registra conclusão do uso da ferramenta."""
    finished_at = time.time()
    event_data = self._prepare_event_data(tool, tool_calling)
    event_data.update({
        "started_at": datetime.datetime.fromtimestamp(started_at),
        "finished_at": datetime.datetime.fromtimestamp(finished_at),
        "from_cache": from_cache,
    })
    events.emit(source=self, event=ToolUsageFinished(**event_data))
```

## Ciclo de Vida da Execução

### 1. Parsing de Chamadas
```python
def parse(self, tool_string: str) -> ToolCalling:
    """Parse string de chamada para objeto ToolCalling."""
    attempts = 0
    while attempts < self._max_parsing_attempts:
        try:
            return self._function_calling(tool_string)
        except Exception as e:
            attempts += 1
            if attempts == self._max_parsing_attempts:
                raise ToolUsageErrorException(str(e))
```

### 2. Seleção de Ferramenta
```python
def _select_tool(self, tool_name: str) -> BaseTool:
    """Seleciona ferramenta pelo nome."""
    for tool in self.tools:
        if tool.name.lower() == tool_name.lower():
            return tool
    raise ToolUsageErrorException(
        self._i18n.errors("tool_not_found").format(
            tool_name=tool_name,
            available_tools=self.tools_names
        )
    )
```

### 3. Execução
```python
def _use(
    self,
    tool_string: str,
    tool: Any,
    calling: Union[ToolCalling, InstructorToolCalling],
) -> Any:
    """Executa ferramenta com tratamento de cache e eventos."""
    started_at = time.time()
    from_cache = False
    
    try:
        # Verifica cache
        cached = self._check_cache(tool, calling.arguments)
        if cached is not None:
            from_cache = True
            return cached
            
        # Executa ferramenta
        result = tool.run(**calling.arguments)
        
        # Atualiza cache
        self._update_cache(tool, calling.arguments, result)
        
        return result
    except Exception as e:
        self.on_tool_error(tool, calling, e)
        raise
    finally:
        self.on_tool_use_finished(tool, calling, from_cache, started_at)
```

## Tratamento de Erros

### 1. Exceções Personalizadas
```python
class ToolUsageErrorException(Exception):
    """Exceção para erros no uso de ferramentas."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
```

### 2. Manipulação de Erros
```python
def on_tool_error(
    self,
    tool: Any,
    tool_calling: ToolCalling,
    e: Exception
) -> None:
    """Manipula erros durante execução."""
    event_data = self._prepare_event_data(tool, tool_calling)
    events.emit(
        source=self,
        event=ToolUsageError(**{**event_data, "error": str(e)})
    )
```

## Melhores Práticas

### 1. Cache
- Use cache apropriadamente
- Implemente invalidação
- Monitore uso de memória

### 2. Telemetria
- Registre eventos importantes
- Monitore performance
- Analise padrões de uso

### 3. Tratamento de Erros
- Capture exceções específicas
- Forneça mensagens claras
- Mantenha logs detalhados

## Considerações Técnicas

### 1. Performance
- Cache eficiente
- Parsing otimizado
- Execução assíncrona

### 2. Segurança
- Validação de entrada
- Sanitização
- Controle de acesso

### 3. Monitoramento
- Eventos detalhados
- Métricas de uso
- Logs de erro

## Exemplos de Implementação

### 1. Sistema Básico
```python
class SimpleToolUsage:
    def __init__(self, tools: List[BaseTool]):
        self.tools = tools
        self.cache = {}
        
    def execute(self, tool_string: str) -> Any:
        # Parse chamada
        calling = self.parse(tool_string)
        
        # Seleciona ferramenta
        tool = self._select_tool(calling.tool_name)
        
        # Executa
        return self._use(tool_string, tool, calling)
```

### 2. Com Telemetria Avançada
```python
class MonitoredToolUsage(ToolUsage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics = MetricsCollector()
        
    def _use(self, *args, **kwargs):
        with self.metrics.measure_time():
            return super()._use(*args, **kwargs)
```

### 3. Sistema Distribuído
```python
class DistributedToolUsage(ToolUsage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.distributed_cache = RedisCache()
        
    def _check_cache(self, tool, args):
        return self.distributed_cache.get(
            self._make_cache_key(tool, args)
        )
```

## Conclusão
O sistema de uso de ferramentas do CrewAI fornece uma implementação robusta e flexível para gerenciar a execução de ferramentas. Sua arquitetura cuida de aspectos críticos como cache, telemetria e tratamento de erros, permitindo uma execução eficiente e confiável das ferramentas do sistema.
