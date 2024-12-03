# Documentação do LTMSQLiteStorage

## Visão Geral

O `LTMSQLiteStorage` é uma implementação especializada de storage que utiliza SQLite para armazenar e gerenciar memórias de longo prazo (Long Term Memory - LTM) no CrewAI. Esta classe é responsável por persistir informações importantes que precisam ser mantidas por longos períodos.

## Estrutura do Storage

### Importações e Dependências
```python
import json
import sqlite3
from typing import Any, Dict, List, Optional, Union
from crewai.utilities import Printer
from crewai.utilities.paths import db_storage_path
```

### Schema do Banco de Dados
```sql
CREATE TABLE IF NOT EXISTS long_term_memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_description TEXT,
    metadata TEXT,
    datetime TEXT,
    score REAL
)
```

## Métodos Principais

### 1. Inicialização

```python
def __init__(
    self,
    db_path: str = f"{db_storage_path()}/long_term_memory_storage.db"
) -> None:
    self.db_path = db_path
    self._printer: Printer = Printer()
    self._initialize_db()
```

#### Características:
- Path padrão do banco
- Inicialização do printer
- Setup automático do DB

### 2. Salvamento

```python
def save(
    self,
    task_description: str,
    metadata: Dict[str, Any],
    datetime: str,
    score: Union[int, float],
) -> None:
```

#### Funcionalidades:
- Persiste memória
- Serializa metadados
- Gerencia scores
- Logging de erros

### 3. Carregamento

```python
def load(
    self,
    task_description: str,
    latest_n: int
) -> Optional[List[Dict[str, Any]]]:
```

#### Características:
- Busca por descrição
- Limitação de resultados
- Ordenação temporal
- Deserialização automática

### 4. Reset

```python
def reset(self) -> None:
```

#### Funcionalidades:
- Limpa todas as memórias
- Operação atômica
- Logging de erros
- Retorno seguro

## Estrutura de Dados

### 1. Memória
```python
{
    "metadata": Dict[str, Any],
    "datetime": str,
    "score": Union[int, float]
}
```

### 2. Campos
- ID autoincremental
- Descrição da tarefa
- Metadados em JSON
- Timestamp
- Score numérico

## Tratamento de Erros

### 1. Conexão
```python
try:
    with sqlite3.connect(self.db_path) as conn:
        # Operações
except sqlite3.Error as e:
    self._printer.print(
        content=f"MEMORY ERROR: {e}",
        color="red"
    )
```

### 2. Validações
- Conexão com banco
- Serialização JSON
- Operações SQL
- Retornos seguros

## Melhores Práticas

### 1. Persistência
- Context managers
- Transações atômicas
- Commits explícitos
- Conexões seguras

### 2. Serialização
- JSON para metadados
- Tipos consistentes
- Validação de dados
- Estrutura uniforme

### 3. Performance
- Índice primário
- Ordenação otimizada
- Limite de resultados
- Queries eficientes

## Considerações de Design

### 1. Estrutura
- Schema simples
- Campos essenciais
- Tipos apropriados
- Constraints adequadas

### 2. Operações
- CRUD básico
- Queries parametrizadas
- Transações atômicas
- Logging integrado

### 3. Segurança
- Paths seguros
- Queries sanitizadas
- Validação de inputs
- Controle de erros

## Extensibilidade

### 1. Campos
- Schema extensível
- Metadados flexíveis
- Scores configuráveis
- Timestamps customizáveis

### 2. Funcionalidades
- Queries adicionais
- Filtros avançados
- Agregações
- Exportação

## Performance

### 1. Otimizações
- Índice primário
- Ordenação eficiente
- Limite de resultados
- Conexões otimizadas

### 2. Monitoramento
- Logging de erros
- Status de operações
- Controle de falhas
- Alertas integrados

## Segurança

### 1. Dados
- Paths seguros
- Sanitização
- Validação
- Backups

### 2. Operações
- Queries seguras
- Transações atômicas
- Logging de erros
- Controle de acesso

## Conclusão

O `LTMSQLiteStorage` fornece:

1. Persistência robusta
2. Operações seguras
3. Serialização eficiente
4. Logging integrado

Esta implementação é crucial para:
- Memória de longo prazo
- Histórico de tarefas
- Análise temporal
- Debugging

O sistema equilibra:
- Simplicidade
- Performance
- Segurança
- Usabilidade

## Notas de Desenvolvimento

### Limitações Atuais
- SQLite local
- Schema fixo
- Sem índices secundários
- Operações síncronas

### Próximos Passos
1. Índices adicionais
2. Queries complexas
3. Backup automático
4. Métricas detalhadas

### Exemplos de Uso

```python
# Inicialização
storage = LTMSQLiteStorage()

# Salvamento de memória
storage.save(
    task_description="Análise de dados",
    metadata={"resultado": "sucesso"},
    datetime="2024-01-20 10:00:00",
    score=0.95
)

# Carregamento de memórias
memories = storage.load(
    task_description="Análise de dados",
    latest_n=5
)

# Reset de memórias
storage.reset()
```

### Considerações de Uso

1. Persistência
- Use context managers
- Valide dados antes de salvar
- Gerencie conexões adequadamente
- Implemente backups regulares

2. Consulta
- Limite número de resultados
- Ordene apropriadamente
- Valide parâmetros
- Cache resultados frequentes

3. Manutenção
- Monitore tamanho do banco
- Implemente limpeza periódica
- Valide integridade
- Backup regular

4. Desenvolvimento
- Documente alterações
- Teste extensivamente
- Valide tipos
- Gerencie dependências
