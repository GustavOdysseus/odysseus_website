# Sistema de Embeddings do CrewAI

## Visão Geral
O sistema de embeddings do CrewAI é uma implementação modular e extensível para geração de embeddings de texto, com suporte a diferentes modelos e otimizações de performance. O sistema é composto por uma interface base abstrata e implementações específicas.

## Arquitetura

### 1. Interface Base (BaseEmbedder)

```python
class BaseEmbedder(ABC):
    @abstractmethod
    def embed_chunks(self, chunks: List[str]) -> np.ndarray: ...
    @abstractmethod
    def embed_texts(self, texts: List[str]) -> np.ndarray: ...
    @abstractmethod
    def embed_text(self, text: str) -> np.ndarray: ...
    @property
    @abstractmethod
    def dimension(self) -> int: ...
```

#### Métodos Abstratos:

1. **embed_chunks**
   - Propósito: Gerar embeddings para múltiplos chunks de texto
   - Input: Lista de strings (chunks)
   - Output: Array numpy de embeddings

2. **embed_texts**
   - Propósito: Gerar embeddings para textos completos
   - Input: Lista de strings (textos)
   - Output: Array numpy de embeddings

3. **embed_text**
   - Propósito: Gerar embedding para um único texto
   - Input: String única
   - Output: Array numpy do embedding

4. **dimension**
   - Propósito: Retornar a dimensionalidade dos embeddings
   - Output: Inteiro representando a dimensão

### 2. Implementação FastEmbed

```python
class FastEmbed(BaseEmbedder):
    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
        cache_dir: Optional[Union[str, Path]] = None,
    ):
```

#### Características:

1. **Inicialização Flexível**
   - Modelo padrão: BAAI/bge-small-en-v1.5
   - Suporte a cache configurável
   - Detecção automática de GPU

2. **Otimizações**
   - Suporte a GPU via fastembed-gpu
   - Sistema de cache para modelos
   - Processamento em batch

3. **Tratamento de Erros**
   - Verificação de disponibilidade do FastEmbed
   - Mensagens de erro informativas
   - Fallbacks apropriados

## Funcionalidades Avançadas

### 1. Suporte a GPU

```python
try:
    from fastembed_gpu import TextEmbedding
    FASTEMBED_AVAILABLE = True
except ImportError:
    try:
        from fastembed import TextEmbedding
        FASTEMBED_AVAILABLE = True
    except ImportError:
        FASTEMBED_AVAILABLE = False
```

- Detecção automática de GPU
- Fallback para CPU quando necessário
- Otimização de performance

### 2. Sistema de Cache

```python
def __init__(
    self,
    model_name: str = "BAAI/bge-small-en-v1.5",
    cache_dir: Optional[Union[str, Path]] = None,
):
    self.model = TextEmbedding(
        model_name=model_name,
        cache_dir=str(cache_dir) if cache_dir else None,
    )
```

- Cache configurável de modelos
- Persistência de embeddings
- Otimização de memória

### 3. Processamento em Batch

```python
def embed_chunks(self, chunks: List[str]) -> List[np.ndarray]:
    embeddings = list(self.model.embed(chunks))
    return embeddings
```

- Processamento eficiente de múltiplos textos
- Otimização de memória
- Performance melhorada

## Uso Prático

### 1. Inicialização Básica

```python
embedder = FastEmbed()
```

### 2. Configuração Avançada

```python
embedder = FastEmbed(
    model_name="modelo_personalizado",
    cache_dir="./cache_embeddings"
)
```

### 3. Geração de Embeddings

```python
# Embedding único
embedding = embedder.embed_text("texto de exemplo")

# Múltiplos embeddings
textos = ["texto1", "texto2", "texto3"]
embeddings = embedder.embed_texts(textos)

# Processamento de chunks
chunks = ["chunk1", "chunk2", "chunk3"]
chunk_embeddings = embedder.embed_chunks(chunks)
```

## Extensibilidade

### 1. Criando Novo Embedder

```python
class MeuEmbedder(BaseEmbedder):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = CarregarMeuModelo(config)

    def embed_chunks(self, chunks: List[str]) -> np.ndarray:
        return self.model.processar_chunks(chunks)

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        return self.model.processar_textos(texts)

    def embed_text(self, text: str) -> np.ndarray:
        return self.model.processar_texto(text)

    @property
    def dimension(self) -> int:
        return self.model.dimensao
```

### 2. Integrando com Outros Modelos

```python
class TransformerEmbedder(BaseEmbedder):
    def __init__(self, model_name: str):
        from transformers import AutoModel, AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
```

## Considerações de Performance

### 1. Uso de Memória
- Processamento em batch para eficiência
- Cache inteligente de modelos
- Limpeza automática de recursos

### 2. Otimização de GPU
- Detecção automática de hardware
- Utilização eficiente de recursos
- Balanceamento de carga

### 3. Escalabilidade
- Processamento paralelo quando possível
- Gerenciamento eficiente de recursos
- Cache distribuído

## Melhores Práticas

### 1. Seleção de Modelo
```python
# Para uso geral
embedder = FastEmbed(model_name="BAAI/bge-small-en-v1.5")

# Para alta precisão
embedder = FastEmbed(model_name="BAAI/bge-large-en-v1.5")

# Para performance
embedder = FastEmbed(model_name="BAAI/bge-small-en-v1.5", cache_dir="./cache")
```

### 2. Processamento em Batch
```python
# Processar em batches para melhor performance
def process_large_dataset(texts: List[str], batch_size: int = 32):
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        embeddings = embedder.embed_texts(batch)
        # Processar embeddings...
```

### 3. Gestão de Recursos
```python
# Configurar cache apropriadamente
import os
cache_dir = os.path.join(os.getcwd(), "embeddings_cache")
embedder = FastEmbed(cache_dir=cache_dir)
```

## Conclusão
O sistema de embeddings do CrewAI oferece uma solução robusta e flexível para geração de embeddings de texto, com suporte a diferentes modelos e otimizações. Sua arquitetura modular permite fácil extensão e personalização, mantendo alta performance e confiabilidade.
