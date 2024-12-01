# Sistema de Fontes de Conhecimento do CrewAI

## Visão Geral
O sistema de fontes de conhecimento do CrewAI é uma arquitetura modular e extensível projetada para ingerir, processar e armazenar conhecimento de diferentes tipos de fontes. O sistema utiliza uma abordagem baseada em chunks e embeddings para processar e armazenar informações de forma eficiente.

## Arquitetura

### Classe Base
```python
class BaseKnowledgeSource(BaseModel, ABC):
    chunk_size: int = 4000
    chunk_overlap: int = 200
    chunks: List[str]
    chunk_embeddings: List[np.ndarray]
    storage: KnowledgeStorage
    metadata: Dict[str, Any]
    collection_name: Optional[str]
```

#### Métodos Principais
1. `load_content() -> Dict[Any, str]`
   - Carrega e pré-processa conteúdo da fonte
   - Método abstrato implementado por subclasses

2. `add() -> None`
   - Processa conteúdo
   - Divide em chunks
   - Computa embeddings
   - Salva no storage

3. `get_embeddings() -> List[np.ndarray]`
   - Retorna lista de embeddings dos chunks

4. `_chunk_text(text: str) -> List[str]`
   - Utilitário para dividir texto em chunks
   - Implementa sobreposição configurável

## Tipos de Fontes

### 1. String Knowledge Source
```python
class StringKnowledgeSource(BaseKnowledgeSource):
    content: str
    collection_name: Optional[str]
```
- Processa texto simples
- Validação de tipo na inicialização
- Chunking automático

### 2. Text File Knowledge Source
- Processa arquivos de texto (.txt)
- Leitura eficiente de arquivos
- Suporte a encoding

### 3. CSV Knowledge Source
- Processa arquivos CSV
- Configuração de delimitadores
- Processamento de colunas

### 4. Excel Knowledge Source
- Suporte a arquivos .xlsx/.xls
- Processamento de múltiplas planilhas
- Configuração de células/ranges

### 5. JSON Knowledge Source
- Processa arquivos JSON
- Suporte a estruturas aninhadas
- Configuração de caminhos

### 6. PDF Knowledge Source
- Extração de texto de PDFs
- Processamento de layouts
- Manutenção de formatação

## Configuração

### 1. Tamanho dos Chunks
```python
source = StringKnowledgeSource(
    content="texto longo...",
    chunk_size=1000,  # Padrão: 4000
    chunk_overlap=100  # Padrão: 200
)
```

### 2. Metadados
```python
metadata = {
    "fonte": "documento_x",
    "autor": "João Silva",
    "data": "2024-01-20"
}
source = StringKnowledgeSource(
    content="...",
    metadata=metadata
)
```

### 3. Storage Personalizado
```python
storage = KnowledgeStorage(
    persistence_dir="./knowledge_db"
)
source = StringKnowledgeSource(
    content="...",
    storage=storage
)
```

## Uso Prático

### 1. Texto Simples
```python
from crewai.knowledge.source import StringKnowledgeSource

source = StringKnowledgeSource(
    content="Texto para processar...",
    chunk_size=1000
)
source.add()
```

### 2. Arquivo CSV
```python
from crewai.knowledge.source import CSVKnowledgeSource

source = CSVKnowledgeSource(
    file_path="dados.csv",
    columns=["texto", "descrição"]
)
source.add()
```

### 3. PDF com Metadados
```python
from crewai.knowledge.source import PDFKnowledgeSource

source = PDFKnowledgeSource(
    file_path="documento.pdf",
    metadata={"tipo": "relatório", "departamento": "vendas"}
)
source.add()
```

## Integração com Storage

### 1. Salvamento de Documentos
```python
def save_documents(self, metadata: Dict[str, Any]):
    """Salva documentos no storage com metadados."""
    self.storage.save(self.chunks, metadata)
```

### 2. Recuperação
```python
# No storage
results = storage.search(
    query="termo de busca",
    collection_name="minha_colecao"
)
```

## Extensibilidade

### 1. Nova Fonte de Conhecimento
```python
class CustomKnowledgeSource(BaseKnowledgeSource):
    def load_content(self) -> Dict[Any, str]:
        # Implementação personalizada
        pass

    def add(self) -> None:
        # Processamento personalizado
        content = self.load_content()
        chunks = self._chunk_text(content)
        self.chunks.extend(chunks)
        self.save_documents(self.metadata)
```

### 2. Processamento Personalizado
```python
class EnhancedTextSource(StringKnowledgeSource):
    def _chunk_text(self, text: str) -> List[str]:
        # Algoritmo personalizado de chunking
        pass

    def add(self) -> None:
        # Pré-processamento adicional
        self.content = self.preprocess(self.content)
        super().add()
```

## Considerações de Performance

### 1. Tamanho dos Chunks
- Menor = Mais preciso, mais storage
- Maior = Menos preciso, menos storage
- Balancear baseado no caso de uso

### 2. Sobreposição
- Mantém contexto entre chunks
- Aumenta uso de storage
- Configurar baseado na coesão necessária

### 3. Processamento em Lote
- Implementar para grandes volumes
- Gerenciar memória eficientemente
- Usar generators quando possível

## Melhores Práticas

### 1. Validação
```python
def load_content(self):
    if not self.content:
        raise ValueError("Conteúdo vazio")
    if len(self.content) < self.chunk_size:
        self.chunk_size = len(self.content)
```

### 2. Metadados
```python
metadata = {
    "source_type": "string",
    "timestamp": datetime.now().isoformat(),
    "version": "1.0"
}
```

### 3. Erro Handling
```python
try:
    source.add()
except Exception as e:
    logger.error(f"Erro ao processar fonte: {e}")
    # Tratamento apropriado
```

## Conclusão
O sistema de fontes de conhecimento do CrewAI oferece uma arquitetura robusta e flexível para processar diferentes tipos de conteúdo. Sua modularidade permite fácil extensão para novos tipos de fontes, enquanto mantém uma interface consistente para integração com o sistema de storage.
