# StringKnowledgeSource - Documentação

## Visão Geral
`StringKnowledgeSource` é uma implementação especializada de `BaseKnowledgeSource` projetada para processar e armazenar conteúdo textual direto como fonte de conhecimento no CrewAI. Esta classe é ideal para trabalhar com strings em memória, sem necessidade de leitura de arquivos.

## Estrutura da Classe

```python
class StringKnowledgeSource(BaseKnowledgeSource):
    """Fonte de conhecimento para conteúdo textual usando embeddings."""

    content: str = Field(...)
    collection_name: Optional[str] = Field(default=None)
```

### Herança
- Estende: `BaseKnowledgeSource`
- Implementa: Processamento específico para strings

## Atributos

### 1. content
- Tipo: `str`
- Obrigatório: Sim
- Descrição: Conteúdo textual a ser processado

### 2. collection_name
- Tipo: `Optional[str]`
- Obrigatório: Não
- Default: None
- Descrição: Nome da coleção para armazenamento

## Métodos Principais

### 1. model_post_init
```python
def model_post_init(self, _):
    """Método de pós-inicialização para validar conteúdo."""
    self.load_content()
```

#### Características
- Executado após inicialização
- Valida o conteúdo inicial
- Garante integridade dos dados

### 2. load_content
```python
def load_content(self):
    """Valida conteúdo string."""
    if not isinstance(self.content, str):
        raise ValueError("StringKnowledgeSource only accepts string content")
```

#### Características
- Validação de tipo
- Garantia de conteúdo string
- Prevenção de erros

### 3. add
```python
def add(self) -> None:
    """
    Adiciona conteúdo string à fonte de conhecimento, divide em chunks,
    computa embeddings e salva.
    """
    new_chunks = self._chunk_text(self.content)
    self.chunks.extend(new_chunks)
    self.save_documents(metadata=self.metadata)
```

### 4. _chunk_text
```python
def _chunk_text(self, text: str) -> List[str]:
    """Método utilitário para dividir texto em chunks."""
    return [
        text[i : i + self.chunk_size]
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap)
    ]
```

## Uso Prático

### 1. Inicialização Básica
```python
from crewai.knowledge.source import StringKnowledgeSource

texto = """
Este é um exemplo de texto longo que será processado
e dividido em chunks para análise e armazenamento.
"""

source = StringKnowledgeSource(
    content=texto,
    chunk_size=1000,
    chunk_overlap=100
)
source.add()
```

### 2. Com Metadados
```python
source = StringKnowledgeSource(
    content="Conteúdo para processamento",
    metadata={
        "tipo": "texto",
        "origem": "manual",
        "versao": "1.0"
    }
)
source.add()
```

### 3. Com Collection Name
```python
source = StringKnowledgeSource(
    content="Texto para processamento",
    collection_name="textos_processados",
    chunk_size=500,
    chunk_overlap=50
)
source.add()
```

## Configurações Avançadas

### 1. Processamento de Texto Avançado
```python
class EnhancedStringSource(StringKnowledgeSource):
    def preprocess_text(self, text: str) -> str:
        # Remove espaços extras
        text = " ".join(text.split())
        # Normaliza quebras de linha
        text = text.replace("\r\n", "\n")
        # Remove caracteres especiais
        text = "".join(char for char in text if char.isprintable())
        return text

    def add(self) -> None:
        self.content = self.preprocess_text(self.content)
        super().add()
```

### 2. Validação Avançada
```python
class ValidatedStringSource(StringKnowledgeSource):
    max_length: int = 1000000  # 1MB de texto

    def load_content(self):
        super().load_content()
        if len(self.content) > self.max_length:
            raise ValueError(f"Conteúdo excede o tamanho máximo de {self.max_length} caracteres")
        if not self.content.strip():
            raise ValueError("Conteúdo não pode ser vazio ou apenas espaços em branco")
```

### 3. Chunks Inteligentes
```python
class SmartChunkStringSource(StringKnowledgeSource):
    def _chunk_text(self, text: str) -> List[str]:
        # Divide por sentenças
        sentences = text.split(". ")
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk += sentence + ". "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
```

## Melhores Práticas

### 1. Tratamento de Erros
```python
class RobustStringSource(StringKnowledgeSource):
    def add(self) -> None:
        try:
            super().add()
        except Exception as e:
            if "Memory" in str(e):
                raise MemoryError(f"Memória insuficiente para processar texto de {len(self.content)} caracteres")
            if "Encoding" in str(e):
                raise UnicodeError("Erro de encoding no texto")
            raise
```

### 2. Logging
```python
import logging

class LoggedStringSource(StringKnowledgeSource):
    def add(self) -> None:
        logging.info(f"Iniciando processamento de texto com {len(self.content)} caracteres")
        try:
            super().add()
            logging.info(f"Processamento concluído, {len(self.chunks)} chunks gerados")
        except Exception as e:
            logging.error(f"Erro no processamento: {e}")
            raise
```

### 3. Métricas
```python
class MetricStringSource(StringKnowledgeSource):
    def add(self) -> None:
        initial_size = len(self.content)
        start_time = time.time()
        
        super().add()
        
        processing_time = time.time() - start_time
        chunks_generated = len(self.chunks)
        avg_chunk_size = sum(len(chunk) for chunk in self.chunks) / chunks_generated
        
        print(f"Métricas de Processamento:")
        print(f"- Tamanho inicial: {initial_size} caracteres")
        print(f"- Tempo de processamento: {processing_time:.2f}s")
        print(f"- Chunks gerados: {chunks_generated}")
        print(f"- Tamanho médio dos chunks: {avg_chunk_size:.2f} caracteres")
```

## Considerações de Performance

### 1. Memória
- Processamento eficiente de strings
- Chunking otimizado
- Gerenciamento de memória

### 2. Processamento
- Validações rápidas
- Divisão eficiente em chunks
- Operações otimizadas

### 3. Storage
- Integração eficiente com sistema de storage
- Metadados otimizados
- Gerenciamento de chunks

## Boas Práticas de Segurança

### 1. Validação de Entrada
- Verificação de tamanho
- Validação de conteúdo
- Sanitização de texto

### 2. Recursos
- Limite de memória
- Timeout para processamento
- Limite de chunks

### 3. Sanitização
- Remoção de caracteres perigosos
- Normalização de texto
- Validação de encoding

## Conclusão
`StringKnowledgeSource` oferece uma implementação robusta e flexível para processar conteúdo textual como fonte de conhecimento no CrewAI. Sua simplicidade e eficiência a tornam ideal para casos de uso que envolvem processamento direto de strings, mantendo a extensibilidade do sistema.
