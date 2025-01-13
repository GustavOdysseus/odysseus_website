# Tool Usage - Documentação Detalhada

## Visão Geral
O arquivo `tool_usage.py` implementa o sistema de gerenciamento de uso de ferramentas no CrewAI. Este módulo é responsável por controlar como os agentes interagem com as ferramentas, incluindo execução, cache, tratamento de erros e telemetria.

## Componentes Principais

### 1. Classe ToolUsageErrorException
```python
class ToolUsageErrorException(Exception):
    """Exception raised for errors in the tool usage."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
```

### 2. Classe ToolUsage

#### Atributos Principais
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
    )
```

- **tools_handler**: Gerenciador de ferramentas
- **tools**: Lista de ferramentas disponíveis
- **original_tools**: Ferramentas antes da conversão
- **tools_description**: Descrição das ferramentas
- **function_calling_llm**: Modelo de linguagem para chamadas

## Funcionalidades Principais

### 1. Execução de Ferramentas

#### Método parse()
```python
def parse(self, tool_string: str):
    """Parse the tool string and return the tool calling."""
    return self._tool_calling(tool_string)
```

#### Método use()
```python
def use(self, calling: Union[ToolCalling, InstructorToolCalling], tool_string: str) -> str:
```
- Executa a ferramenta solicitada
- Gerencia erros e retentativas
- Integra com sistema de cache
- Registra telemetria

### 2. Sistema de Cache

#### Características
- Cache automático de resultados
- Função de cache personalizável
- Invalidação inteligente
- Otimização de performance

### 3. Tratamento de Erros

#### Estratégias
- Retentativas automáticas
- Limite configurável de tentativas
- Mensagens de erro internacionalizadas
- Telemetria de erros

### 4. Integração com Modelos de Linguagem

#### Configurações
- Suporte a diferentes modelos
- Ajuste automático de parâmetros
- Otimização por modelo

## Recursos Avançados

### 1. Telemetria
```python
self._telemetry.tool_usage(
    llm=self.function_calling_llm,
    tool_name=tool.name,
    attempts=self._run_attempts,
)
```

### 2. Internacionalização
```python
self._i18n.errors("tool_usage_exception").format(
    error=e,
    tool=tool.name,
    tool_inputs=tool.description
)
```

### 3. Formatação de Resultados
```python
def _format_result(self, result: Any) -> None:
    self.task.used_tools += 1
    if self._should_remember_format():
        result = self._remember_format(result=result)
    return result
```

## Fluxo de Execução

### 1. Inicialização
1. Configuração do handler de ferramentas
2. Carregamento das ferramentas disponíveis
3. Configuração do modelo de linguagem

### 2. Execução
1. Parse da string de chamada
2. Validação de argumentos
3. Verificação de cache
4. Execução da ferramenta
5. Formatação do resultado

### 3. Pós-execução
1. Registro de telemetria
2. Atualização de cache
3. Notificação de eventos

## Integração com Agentes

### 1. Delegação de Trabalho
```python
if calling.tool_name in [
    "Delegate work to coworker",
    "Ask question to coworker",
]:
    coworker = calling.arguments.get("coworker")
    self.task.increment_delegations(coworker)
```

### 2. Gestão de Estado
- Rastreamento de uso de ferramentas
- Contagem de erros
- Histórico de execução

## Otimizações

### 1. Performance
- Cache inteligente
- Retentativas limitadas
- Validação eficiente

### 2. Memória
- Limpeza automática
- Gestão de recursos
- Otimização de objetos

### 3. Escalabilidade
- Design modular
- Baixo acoplamento
- Extensibilidade

## Exemplos de Uso

### 1. Chamada Básica
```python
tool_usage = ToolUsage(
    tools_handler=handler,
    tools=tools,
    original_tools=original_tools,
    tools_description="Descrição das ferramentas",
    tools_names="nomes das ferramentas",
    task=task,
    function_calling_llm=llm,
    agent=agent,
    action=action
)

result = tool_usage.use(
    calling=tool_calling,
    tool_string="string de chamada"
)
```

### 2. Tratamento de Erros
```python
try:
    result = tool_usage.use(calling=tool_calling, tool_string=tool_string)
except ToolUsageErrorException as e:
    print(f"Erro na execução: {e.message}")
```

## Melhores Práticas

### 1. Configuração
- Configure limites de retentativas apropriados
- Defina estratégias de cache adequadas
- Implemente tratamento de erros robusto

### 2. Monitoramento
- Utilize telemetria
- Monitore uso de recursos
- Acompanhe taxas de erro

### 3. Otimização
- Implemente cache quando apropriado
- Otimize validações
- Gerencie recursos adequadamente

## Considerações Técnicas

### 1. Dependências
- Pydantic para validação
- LangChain para integração
- Sistema de eventos

### 2. Performance
- Otimização de cache
- Gestão de memória
- Execução eficiente

### 3. Segurança
- Validação de entrada
- Sanitização de dados
- Proteção contra erros

## Conclusão
O módulo `tool_usage.py` é um componente crítico do CrewAI, fornecendo uma interface robusta e eficiente para o uso de ferramentas por agentes. Sua implementação cuidadosa equilibra funcionalidade, performance e segurança, permitindo uma execução confiável e otimizada de ferramentas no sistema.
