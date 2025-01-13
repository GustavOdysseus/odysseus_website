# Documentação do Base Agent Tools

## Visão Geral
O módulo `base_agent_tools.py` define a classe base `BaseAgentTool` para todas as ferramentas relacionadas a agentes no CrewAI. Esta classe fornece funcionalidades básicas para interação entre agentes, delegação de tarefas e gerenciamento de erros.

## Classe BaseAgentTool

### Atributos
- `agents` (list[BaseAgent]): Lista de agentes disponíveis
- `i18n` (I18N): Configurações de internacionalização

### Métodos Principais

#### `sanitize_agent_name(name: str) -> str`
Sanitiza o nome/papel do agente normalizando espaços em branco e convertendo para minúsculas.

Argumentos:
- `name` (str): Nome do papel do agente para sanitizar

Retorno:
- str: Nome do papel do agente sanitizado

#### `_get_coworker(coworker: Optional[str], **kwargs) -> Optional[str]`
Obtém o nome do coworker a partir dos argumentos fornecidos.

#### `_execute(agent_name: Optional[str], task: str, context: Optional[str] = None) -> str`
Executa a delegação de uma tarefa para um agente.

Argumentos:
- `agent_name`: Nome/papel do agente para delegar (case-insensitive)
- `task`: Pergunta ou tarefa específica para delegar
- `context`: Contexto adicional opcional para execução da tarefa

Retorno:
- str: Resultado da execução do agente delegado ou mensagem de erro

## Fluxo de Execução

1. Sanitização do nome do agente:
   ```python
   sanitized_name = self.sanitize_agent_name(agent_name)
   ```

2. Busca do agente correspondente:
   ```python
   agent = [
       available_agent
       for available_agent in self.agents
       if self.sanitize_agent_name(available_agent.role) == sanitized_name
   ]
   ```

3. Criação e execução da tarefa:
   ```python
   task_with_assigned_agent = Task(
       description=task,
       agent=agent,
       expected_output=agent.i18n.slice("manager_request"),
       i18n=agent.i18n,
   )
   return agent.execute_task(task_with_assigned_agent, context)
   ```

## Tratamento de Erros

A classe implementa tratamento robusto de erros para:
1. Agentes não encontrados
2. Erros de processamento do nome do agente
3. Erros na criação ou execução da tarefa

Exemplo de mensagem de erro:
```python
return self.i18n.errors("agent_tool_unexisting_coworker").format(
    coworkers="\n".join(
        [f"- {self.sanitize_agent_name(agent.role)}" for agent in self.agents]
    ),
    error=f"No agent found with role '{sanitized_name}'"
)
```

## Notas Importantes
1. A classe é projetada para ser extensível e servir como base para ferramentas específicas de agente
2. Implementa suporte a internacionalização (i18n)
3. Inclui logging detalhado para depuração
4. Trata casos especiais com LLMs menos poderosos que podem produzir JSON inválido
5. Fornece mensagens de erro informativas com lista de agentes disponíveis
