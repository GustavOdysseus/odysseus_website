# Documentação do KickoffTaskOutputsSQLiteStorage

## Visão Geral

O `KickoffTaskOutputsSQLiteStorage` é uma implementação especializada de storage que utiliza SQLite para armazenar e gerenciar os outputs de tarefas de kickoff no CrewAI. Esta classe é responsável por persistir os resultados de execução de tarefas, permitindo recuperação e análise posterior.

## Estrutura do Storage

### Importações e Dependências
```python
import json
import sqlite3
from typing import Any, Dict, List, Optional
from crewai.task import Task
from crewai.utilities import Printer
from crewai.utilities.crew_json_encoder import CrewJSONEncoder
from crewai.utilities.paths import db_storage_path
```

### Schema do Banco de Dados
```sql
CREATE TABLE IF NOT EXISTS latest_kickoff_task_outputs (
    task_id TEXT PRIMARY KEY,
    expected_output TEXT,
    output JSON,
    task_index INTEGER,
    inputs JSON,
    was_replayed BOOLEAN,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

## Métodos Principais

### 1. Inicialização

```python
def __init__(
    self,
    db_path: str = f"{db_storage_path()}/latest_kickoff_task_outputs.db"
) -> None:
    self.db_path = db_path
    self._printer: Printer = Printer()
    self._initialize_db()
```

#### Características:
- Path padrão do banco
- Inicialização do printer
- Setup automático do DB

### 2. Adição de Dados

```python
def add(
    self,
    task: Task,
    output: Dict[str, Any],
    task_index: int,
    was_replayed: bool = False,
    inputs: Dict[str, Any] = {},
):
```

#### Funcionalidades:
- Insere ou atualiza task
- Serializa JSON
- Gerencia índices
- Controle de replay

### 3. Atualização

```python
def update(
    self,
    task_index: int,
    **kwargs,
):
```

#### Características:
- Atualização dinâmica
- Suporte a kwargs
- Serialização automática
- Validação de existência

### 4. Carregamento

```python
def load(self) -> Optional[List[Dict[str, Any]]]:
```

#### Funcionalidades:
- Carrega todos os outputs
- Ordenação por índice
- Deserialização JSON
- Estrutura consistente

### 5. Deleção

```python
def delete_all(self):
```

#### Características:
- Limpa todos os dados
- Mantém estrutura
- Operação atômica
- Logging de erros

## Estrutura de Dados

### 1. Task Output
```python
{
    "task_id": str,
    "expected_output": str,
    "output": Dict[str, Any],
    "task_index": int,
    "inputs": Dict[str, Any],
    "was_replayed": bool,
    "timestamp": str
}
```

### 2. Metadados
- Task ID como chave primária
- Índice numérico para ordenação
- Timestamp automático
- Flags de controle

## Tratamento de Erros

### 1. Conexão
```python
try:
    with sqlite3.connect(self.db_path) as conn:
        # Operações
except sqlite3.Error as e:
    self._printer.print(
        content=f"ERROR: {e}",
        color="red"
    )
```

### 2. Validações
- Verificação de existência
- Validação de índices
- Controle de transações
- Logging estruturado

## Melhores Práticas

### 1. Persistência
- Uso de context managers
- Transações atômicas
- Commits explícitos
- Conexões seguras

### 2. Serialização
- JSON encoder customizado
- Tratamento de tipos
- Validação de dados
- Estrutura consistente

### 3. Performance
- Índices apropriados
- Queries otimizadas
- Conexões reutilizadas
- Batch operations

## Considerações de Design

### 1. Estrutura
- Schema otimizado
- Campos essenciais
- Tipos apropriados
- Constraints adequadas

### 2. Operações
- CRUD completo
- Queries parametrizadas
- Transações atômicas
- Logging integrado

### 3. Segurança
- Paths seguros
- Queries sanitizadas
- Validação de inputs
- Controle de acesso

## Extensibilidade

### 1. Campos Adicionais
- Schema flexível
- JSON para extras
- Metadados expansíveis
- Timestamps automáticos

### 2. Funcionalidades
- Queries customizadas
- Filtros avançados
- Agregações
- Exportação

## Performance

### 1. Otimizações
- Índices adequados
- Conexões pooling
- Queries eficientes
- Batch operations

### 2. Monitoramento
- Logging de erros
- Métricas de tempo
- Status de operações
- Alertas de falha

## Segurança

### 1. Dados
- Paths seguros
- Sanitização
- Validação
- Backups

### 2. Operações
- Transações seguras
- Queries parametrizadas
- Controle de acesso
- Logging de ações

## Conclusão

O `KickoffTaskOutputsSQLiteStorage` fornece:

1. Persistência robusta
2. Operações atômicas
3. Serialização segura
4. Logging integrado

Esta implementação é crucial para:
- Rastreamento de tarefas
- Análise de outputs
- Replay de execuções
- Debugging

O sistema equilibra:
- Performance
- Segurança
- Usabilidade
- Extensibilidade

## Notas de Desenvolvimento

### Limitações Atuais
- SQLite local
- Schema fixo
- Sem índices customizados
- Operações síncronas

### Próximos Passos
1. Índices adicionais
2. Queries avançadas
3. Backup automático
4. Métricas detalhadas

### Exemplos de Uso

```python
# Inicialização
storage = KickoffTaskOutputsSQLiteStorage()

# Adição de output
storage.add(
    task=task,
    output={"result": "success"},
    task_index=1,
    inputs={"param": "value"}
)

# Atualização
storage.update(
    task_index=1,
    output={"result": "updated"}
)

# Carregamento
outputs = storage.load()

# Limpeza
storage.delete_all()
```
