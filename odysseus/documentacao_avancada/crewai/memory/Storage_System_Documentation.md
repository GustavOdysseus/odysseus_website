# Documentação do Sistema de Armazenamento (Storage) do CrewAI

## Visão Geral

O sistema de armazenamento do CrewAI é uma implementação modular e extensível que fornece diferentes estratégias de persistência e recuperação de dados para os diversos tipos de memória do framework. O sistema é projetado para ser flexível, permitindo múltiplos backends de armazenamento e otimizações específicas para cada caso de uso.

## Arquitetura do Sistema

### 1. Interface Base (Storage)

```python
class Storage:
    def save(self, value: Any, metadata: Dict[str, Any]) -> None:
        pass

    def search(self, query: str, limit: int, score_threshold: float) -> Dict[str, Any] | List[Any]:
        return {}

    def reset(self) -> None:
        pass
```

#### Métodos:
- `save`: Armazena dados com metadados
- `search`: Busca dados com filtragem
- `reset`: Limpa o armazenamento

### 2. Implementações de Storage

#### 2.1 RAG Storage (Retrieval-Augmented Generation)

```python
class RAGStorage(BaseRAGStorage):
    def __init__(self, type, allow_reset=True, embedder_config=None, crew=None):
        # Inicialização do storage RAG
```

##### Características:
- Baseado em embeddings
- Persistência com ChromaDB
- Busca semântica
- Configuração flexível

#### 2.2 SQLite Storage (Long-Term Memory)

```python
class LTMSQLiteStorage:
    def __init__(self, db_path: str = "..."):
        # Inicialização do storage SQLite
```

##### Características:
- Armazenamento relacional
- Persistência durável
- Queries otimizadas
- Gestão de metadados

#### 2.3 Mem0 Storage

```python
class Mem0Storage(Storage):
    def __init__(self, type, crew=None):
        # Inicialização do storage Mem0
```

##### Características:
- Integração externa
- Múltiplos tipos de memória
- API key requerida
- Gestão contextual

## Componentes Principais

### 1. Base RAG Storage

#### Funcionalidades:
- Geração de embeddings
- Inicialização de apps
- Sanitização de dados
- Configuração flexível

#### Métodos Abstratos:
```python
@abstractmethod
def _generate_embedding(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> Any:
    pass

@abstractmethod
def _initialize_app(self):
    pass
```

### 2. RAG Storage Concreto

#### Funcionalidades:
- Persistência com ChromaDB
- Gestão de coleções
- Configuração de embeddings
- Busca vetorial

#### Características:
- Supressão de logs
- Gestão de contexto
- Tratamento de erros
- Configuração dinâmica

### 3. SQLite Storage

#### Funcionalidades:
- Schema relacional
- Queries SQL
- Serialização JSON
- Gestão de erros

#### Schema:
```sql
CREATE TABLE IF NOT EXISTS long_term_memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_description TEXT,
    metadata TEXT,
    datetime TEXT,
    score REAL
)
```

### 4. Mem0 Storage

#### Funcionalidades:
- Integração com MemoryClient
- Tipos específicos de memória
- Metadados customizados
- Busca contextual

#### Tipos Suportados:
- user
- short_term
- long_term
- entities

## Casos de Uso

### 1. RAG Storage
```python
storage = RAGStorage(
    type="agent_memory",
    allow_reset=True,
    embedder_config={"model": "text-embedding-ada-002"}
)
storage.save("Informação importante", {"contexto": "reunião"})
```

### 2. SQLite Storage
```python
storage = LTMSQLiteStorage()
storage.save(
    task_description="Análise de Dados",
    metadata={"tipo": "financeiro"},
    datetime="2024-01-20",
    score=0.95
)
```

### 3. Mem0 Storage
```python
storage = Mem0Storage(type="user", crew=crew)
storage.save(
    value="Preferência do usuário",
    metadata={"tipo": "configuração"}
)
```

## Melhores Práticas

### 1. Escolha do Storage
- RAG: Busca semântica
- SQLite: Dados estruturados
- Mem0: Integração externa

### 2. Gestão de Dados
- Metadados consistentes
- Sanitização adequada
- Backup regular
- Monitoramento

### 3. Otimização
- Configuração de embeddings
- Índices apropriados
- Limites de busca
- Cache eficiente

## Considerações de Implementação

### 1. RAG Storage
- Configure embeddings
- Gerencie coleções
- Monitore performance
- Otimize busca

### 2. SQLite Storage
- Backup regular
- Índices otimizados
- Queries eficientes
- Gestão de conexões

### 3. Mem0 Storage
- Segurança da API key
- Tipos apropriados
- Gestão de contexto
- Tratamento de erros

## Segurança

### 1. Proteção de Dados
- Sanitização de inputs
- Validação de dados
- Controle de acesso
- Logs seguros

### 2. Credenciais
- Gestão de API keys
- Variáveis de ambiente
- Configuração segura
- Auditoria

## Extensibilidade

### 1. Novos Storages
- Implemente interface
- Mantenha compatibilidade
- Documente métodos
- Teste integração

### 2. Customização
- Configure embeddings
- Expanda metadados
- Adicione índices
- Otimize queries

## Performance

### 1. RAG Storage
- Cache de embeddings
- Otimização de busca
- Gestão de memória
- Monitoramento

### 2. SQLite Storage
- Índices otimizados
- Conexões pooling
- Queries eficientes
- Vacuum regular

### 3. Mem0 Storage
- Cache local
- Batch operations
- Retry mechanism
- Error handling

## Conclusão

O sistema de Storage do CrewAI oferece:

1. Flexibilidade de implementação
2. Múltiplas estratégias
3. Performance otimizada
4. Extensibilidade robusta

Esta implementação é crucial para:
- Persistência eficiente
- Recuperação contextual
- Integração flexível
- Escalabilidade

O sistema equilibra:
- Flexibilidade
- Performance
- Segurança
- Usabilidade

## Notas de Desenvolvimento

### Limitações Atuais
- RAG: Dependência do ChromaDB
- SQLite: Schema fixo
- Mem0: API key requerida

### Próximos Passos
1. Novos backends de storage
2. Otimização de performance
3. Mais opções de configuração
4. Melhor gestão de erros
