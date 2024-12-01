# Documentação do RAGStorage

## Visão Geral

O `RAGStorage` é uma implementação especializada que estende o `BaseRAGStorage` para fornecer capacidades avançadas de armazenamento e busca baseadas em embeddings usando ChromaDB. Esta implementação é otimizada para Retrieval-Augmented Generation (RAG) no CrewAI.

## Estrutura do Storage

### Importações e Dependências
```python
import contextlib
import io
import logging
import os
import shutil
import uuid
from typing import Any, Dict, List, Optional
from chromadb.api import ClientAPI
from crewai.memory.storage.base_rag_storage import BaseRAGStorage
from crewai.utilities.paths import db_storage_path
from crewai.utilities import EmbeddingConfigurator
```

### Componentes Principais
- ChromaDB para armazenamento persistente
- OpenAI para embeddings
- Sistema de logging personalizado
- Gestão de contexto

## Funcionalidades Principais

### 1. Supressão de Logging
```python
@contextlib.contextmanager
def suppress_logging(
    logger_name="chromadb.segment.impl.vector.local_persistent_hnsw",
    level=logging.ERROR,
):
    logger = logging.getLogger(logger_name)
    original_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    with (
        contextlib.redirect_stdout(io.StringIO()),
        contextlib.redirect_stderr(io.StringIO()),
        contextlib.suppress(UserWarning),
    ):
        yield
    logger.setLevel(original_level)
```

#### Características:
- Controle de logs
- Redirecionamento de stdout/stderr
- Supressão de warnings
- Restauração de níveis

### 2. Inicialização

```python
def __init__(self, type, allow_reset=True, embedder_config=None, crew=None):
    super().__init__(type, allow_reset, embedder_config, crew)
    agents = crew.agents if crew else []
    agents = [self._sanitize_role(agent.role) for agent in agents]
    agents = "_".join(agents)
    self.agents = agents
    self.type = type
    self.allow_reset = allow_reset
    self._initialize_app()
```

#### Características:
- Configuração de embeddings
- Gestão de agentes
- Inicialização do ChromaDB
- Configuração flexível

### 3. Configuração de Embeddings

```python
def _set_embedder_config(self):
    configurator = EmbeddingConfigurator()
    self.embedder_config = configurator.configure_embedder(self.embedder_config)
```

#### Funcionalidades:
- Configuração automática
- Integração com OpenAI
- Flexibilidade de modelos
- Gestão de API keys

### 4. Inicialização do ChromaDB

```python
def _initialize_app(self):
    import chromadb
    from chromadb.config import Settings

    self._set_embedder_config()
    chroma_client = chromadb.PersistentClient(
        path=f"{db_storage_path()}/{self.type}/{self.agents}",
        settings=Settings(allow_reset=self.allow_reset),
    )

    self.app = chroma_client
    
    try:
        self.collection = self.app.get_collection(
            name=self.type,
            embedding_function=self.embedder_config
        )
    except Exception:
        self.collection = self.app.create_collection(
            name=self.type,
            embedding_function=self.embedder_config
        )
```

#### Características:
- Cliente persistente
- Coleções dinâmicas
- Configuração de embeddings
- Gestão de erros

### 5. Operações de Memória

#### Salvamento
```python
def save(self, value: Any, metadata: Dict[str, Any]) -> None:
    if not hasattr(self, "app") or not hasattr(self, "collection"):
        self._initialize_app()
    try:
        self._generate_embedding(value, metadata)
    except Exception as e:
        logging.error(f"Error during {self.type} save: {str(e)}")
```

#### Busca
```python
def search(
    self,
    query: str,
    limit: int = 3,
    filter: Optional[dict] = None,
    score_threshold: float = 0.35,
) -> List[Any]:
    if not hasattr(self, "app"):
        self._initialize_app()

    try:
        with suppress_logging():
            response = self.collection.query(
                query_texts=query,
                n_results=limit
            )

        results = []
        for i in range(len(response["ids"][0])):
            result = {
                "id": response["ids"][0][i],
                "metadata": response["metadatas"][0][i],
                "context": response["documents"][0][i],
                "score": response["distances"][0][i],
            }
            if result["score"] >= score_threshold:
                results.append(result)

        return results
    except Exception as e:
        logging.error(f"Error during {self.type} search: {str(e)}")
        return []
```

## Configuração

### 1. ChromaDB
- Cliente persistente
- Coleções por tipo
- Reset configurável
- Path personalizado

### 2. Embeddings
- OpenAI por padrão
- Modelo configurável
- API key via env
- Função customizável

### 3. Logging
- Níveis configuráveis
- Supressão seletiva
- Redirecionamento
- Gestão de contexto

## Melhores Práticas

### 1. Inicialização
- Configure embeddings
- Valide paths
- Gerencie coleções
- Trate erros

### 2. Operações
- Use metadata
- Configure thresholds
- Gerencie recursos
- Monitore performance

### 3. Manutenção
- Reset periódico
- Backup de dados
- Monitoramento
- Logging adequado

## Considerações de Design

### 1. Arquitetura
- Persistência local
- Embeddings vetoriais
- Busca semântica
- Metadata flexível

### 2. Performance
- Logging otimizado
- Busca eficiente
- Thresholds ajustáveis
- Gestão de memória

### 3. Segurança
- API keys seguras
- Paths sanitizados
- Dados persistentes
- Controle de acesso

## Performance

### 1. Otimizações
- Supressão de logs
- Thresholds de score
- Limite de resultados
- Caching implícito

### 2. Monitoramento
- Logging de erros
- Tracking de operações
- Gestão de recursos
- Métricas implícitas

## Segurança

### 1. Dados
- Persistência segura
- Sanitização de paths
- Metadata validada
- Reset controlado

### 2. Configuração
- API keys via env
- Paths seguros
- Acesso controlado
- Reset limitado

## Conclusão

O `RAGStorage` fornece:

1. Armazenamento vetorial eficiente
2. Busca semântica avançada
3. Persistência robusta
4. Configuração flexível

Esta implementação é crucial para:
- RAG eficiente
- Busca semântica
- Persistência de dados
- Gestão de contexto

O sistema equilibra:
- Performance
- Segurança
- Flexibilidade
- Usabilidade

## Notas de Desenvolvimento

### Limitações Atuais
- Dependência do ChromaDB
- OpenAI para embeddings
- Persistência local
- Reset manual

### Próximos Passos
1. Mais backends
2. Embeddings alternativos
3. Persistência distribuída
4. Métricas avançadas

### Exemplos de Uso

```python
# Inicialização
storage = RAGStorage(
    type="semantic",
    allow_reset=True,
    crew=crew_instance
)

# Salvamento
storage.save(
    value="Informação importante",
    metadata={"contexto": "documento"}
)

# Busca
results = storage.search(
    query="informação",
    limit=5,
    score_threshold=0.5
)
```

### Considerações de Uso

1. Configuração
- Configure ChromaDB
- Defina embeddings
- Valide paths
- Gerencie collections

2. Operação
- Use metadata
- Configure busca
- Monitore scores
- Gerencie recursos

3. Manutenção
- Backup regular
- Monitore uso
- Valide dados
- Reset periódico

4. Desenvolvimento
- Teste embeddings
- Valide busca
- Monitore performance
- Gerencie dependências
