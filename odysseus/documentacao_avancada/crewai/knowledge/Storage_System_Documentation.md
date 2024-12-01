# Sistema de Armazenamento do CrewAI

## Visão Geral
O sistema de armazenamento do CrewAI é uma implementação sofisticada baseada em banco de dados vetorial (ChromaDB) para armazenamento e recuperação eficiente de conhecimento. O sistema oferece persistência, busca por similaridade e gerenciamento avançado de embeddings.

## Arquitetura

### 1. Interface Base (BaseKnowledgeStorage)

```python
class BaseKnowledgeStorage(ABC):
    @abstractmethod
    def search(
        self,
        query: List[str],
        limit: int = 3,
        filter: Optional[dict] = None,
        score_threshold: float = 0.35,
    ) -> List[Dict[str, Any]]: ...

    @abstractmethod
    def save(
        self,
        documents: List[str],
        metadata: Dict[str, Any] | List[Dict[str, Any]]
    ) -> None: ...

    @abstractmethod
    def reset(self) -> None: ...
```

#### Métodos Abstratos:

1. **search**
   - Propósito: Buscar documentos na base de conhecimento
   - Parâmetros:
     - query: Lista de strings para busca
     - limit: Número máximo de resultados
     - filter: Filtros opcionais
     - score_threshold: Limiar de similaridade
   - Retorno: Lista de documentos encontrados

2. **save**
   - Propósito: Salvar documentos na base
   - Parâmetros:
     - documents: Lista de documentos
     - metadata: Metadados associados
   - Comportamento: Persistência atômica

3. **reset**
   - Propósito: Resetar a base de conhecimento
   - Comportamento: Limpeza completa

### 2. Implementação Principal (KnowledgeStorage)

```python
class KnowledgeStorage(BaseKnowledgeStorage):
    collection: Optional[chromadb.Collection] = None
    collection_name: Optional[str] = "knowledge"
    app: Optional[ClientAPI] = None
```

#### Características Principais:

1. **Persistência**
   - Armazenamento em disco via ChromaDB
   - Gerenciamento de coleções
   - Recuperação resiliente

2. **Busca Vetorial**
   - Busca por similaridade
   - Filtragem avançada
   - Threshold configurável

3. **Gestão de Embeddings**
   - Configuração flexível
   - Suporte a múltiplos modelos
   - Fallback para OpenAI

## Funcionalidades Avançadas

### 1. Sistema de Persistência

```python
def initialize_knowledge_storage(self):
    base_path = os.path.join(db_storage_path(), "knowledge")
    chroma_client = chromadb.PersistentClient(
        path=base_path,
        settings=Settings(allow_reset=True),
    )
```

- Armazenamento persistente em disco
- Gerenciamento de coleções
- Configurações flexíveis

### 2. Busca Avançada

```python
def search(
    self,
    query: List[str],
    limit: int = 3,
    filter: Optional[dict] = None,
    score_threshold: float = 0.35,
) -> List[Dict[str, Any]]:
```

Características:
- Busca multi-query
- Filtragem contextual
- Score threshold adaptativo
- Metadados enriquecidos

### 3. Sistema de Salvamento

```python
def save(
    self,
    documents: List[str],
    metadata: Union[Dict[str, Any], List[Dict[str, Any]]],
):
```

Funcionalidades:
- Hash único por documento
- Upsert automático
- Validação de dimensionalidade
- Tratamento de erros robusto

## Uso Prático

### 1. Inicialização Básica

```python
storage = KnowledgeStorage(collection_name="minha_base")
storage.initialize_knowledge_storage()
```

### 2. Salvando Documentos

```python
documents = ["documento1", "documento2"]
metadata = [
    {"tipo": "texto", "fonte": "arquivo1"},
    {"tipo": "texto", "fonte": "arquivo2"}
]
storage.save(documents, metadata)
```

### 3. Realizando Buscas

```python
resultados = storage.search(
    query=["termo de busca"],
    limit=5,
    filter={"tipo": "texto"},
    score_threshold=0.4
)
```

## Integração com Embeddings

### 1. Configuração Default (OpenAI)

```python
def _create_default_embedding_function(self):
    return OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )
```

### 2. Configuração Personalizada

```python
storage = KnowledgeStorage(
    embedder_config={
        "model_name": "meu_modelo",
        "dimension": 768
    }
)
```

## Considerações de Performance

### 1. Gestão de Memória
- Persistência otimizada
- Cache inteligente
- Gerenciamento de recursos

### 2. Otimização de Busca
- Índices eficientes
- Filtragem otimizada
- Thresholds adaptativos

### 3. Tratamento de Erros
- Supressão de logs desnecessários
- Mensagens informativas
- Fallbacks apropriados

## Melhores Práticas

### 1. Inicialização
```python
# Configuração recomendada
storage = KnowledgeStorage(
    collection_name="minha_base",
    embedder_config={
        "model_name": "modelo_otimizado",
        "cache_dir": "./cache"
    }
)
```

### 2. Salvamento
```python
# Salvamento com metadados ricos
docs = ["conteudo1", "conteudo2"]
meta = [
    {
        "tipo": "documento",
        "fonte": "sistema",
        "timestamp": "2024-01-01",
        "tags": ["importante", "referencia"]
    },
    # ...
]
storage.save(docs, meta)
```

### 3. Busca
```python
# Busca otimizada
results = storage.search(
    query=["conceito principal", "contexto adicional"],
    limit=3,
    filter={"tipo": "documento", "tags": "importante"},
    score_threshold=0.45
)
```

## Extensibilidade

### 1. Storage Personalizado
```python
class MeuStorage(BaseKnowledgeStorage):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.initialize()

    def search(self, query, limit=3, filter=None, score_threshold=0.35):
        # Implementação personalizada
        pass

    def save(self, documents, metadata):
        # Implementação personalizada
        pass

    def reset(self):
        # Implementação personalizada
        pass
```

### 2. Integração com Outros Bancos
```python
class HybridStorage(KnowledgeStorage):
    def __init__(self, vector_config: Dict[str, Any], sql_config: Dict[str, Any]):
        super().__init__(vector_config)
        self.sql_db = SQLDatabase(sql_config)

    def save(self, documents, metadata):
        # Salva em ambos os bancos
        super().save(documents, metadata)
        self.sql_db.save(documents, metadata)
```

## Conclusão
O sistema de armazenamento do CrewAI oferece uma solução robusta e flexível para persistência e recuperação de conhecimento, com suporte a busca vetorial avançada e integração seamless com diferentes sistemas de embedding. Sua arquitetura modular permite extensão fácil e adaptação a diferentes casos de uso, mantendo performance e confiabilidade.
