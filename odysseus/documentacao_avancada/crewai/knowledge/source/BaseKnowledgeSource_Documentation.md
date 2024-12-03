# BaseKnowledgeSource - Documentação

## Visão Geral
`BaseKnowledgeSource` é a classe base abstrata fundamental para todas as fontes de conhecimento no CrewAI. Esta classe define a interface e comportamentos comuns para processamento, chunking e armazenamento de conhecimento.

## Estrutura da Classe

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

### Atributos

1. `chunk_size`
   - Tipo: `int`
   - Padrão: 4000
   - Propósito: Define o tamanho de cada chunk de texto
   - Impacto: Afeta granularidade e precisão da recuperação

2. `chunk_overlap`
   - Tipo: `int`
   - Padrão: 200
   - Propósito: Define sobreposição entre chunks consecutivos
   - Uso: Mantém contexto entre chunks

3. `chunks`
   - Tipo: `List[str]`
   - Inicialização: Lista vazia
   - Propósito: Armazena chunks de texto processados
   - Gestão: Atualizado durante processamento

4. `chunk_embeddings`
   - Tipo: `List[np.ndarray]`
   - Inicialização: Lista vazia
   - Propósito: Armazena embeddings dos chunks
   - Formato: Arrays numpy multidimensionais

5. `storage`
   - Tipo: `KnowledgeStorage`
   - Padrão: Nova instância
   - Propósito: Gerencia persistência dos dados
   - Configuração: Customizável via injeção

6. `metadata`
   - Tipo: `Dict[str, Any]`
   - Inicialização: Dicionário vazio
   - Propósito: Informações adicionais sobre o conhecimento
   - Flexibilidade: Aceita qualquer tipo de valor

7. `collection_name`
   - Tipo: `Optional[str]`
   - Padrão: None
   - Propósito: Identifica coleção no storage
   - Uso: Organização e recuperação

## Métodos Abstratos

### 1. load_content
```python
@abstractmethod
def load_content(self) -> Dict[Any, str]:
    """Carrega e pré-processa conteúdo da fonte."""
    pass
```
- Deve ser implementado por subclasses
- Responsável por carregar dados brutos
- Retorna mapeamento de identificadores para conteúdo
- Pode incluir pré-processamento específico

### 2. add
```python
@abstractmethod
def add(self) -> None:
    """Processa conteúdo, divide em chunks, computa embeddings e salva."""
    pass
```
- Deve ser implementado por subclasses
- Orquestra o pipeline de processamento
- Gerencia fluxo de dados
- Integra com storage

## Métodos Utilitários

### 1. get_embeddings
```python
def get_embeddings(self) -> List[np.ndarray]:
    """Retorna lista de embeddings dos chunks."""
    return self.chunk_embeddings
```
- Acesso aos embeddings computados
- Uso em recuperação e busca
- Formato: Lista de arrays numpy

### 2. _chunk_text
```python
def _chunk_text(self, text: str) -> List[str]:
    """Método utilitário para dividir texto em chunks."""
    return [
        text[i : i + self.chunk_size]
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap)
    ]
```
- Implementação base de chunking
- Usa chunk_size e chunk_overlap
- Mantém consistência entre chunks
- Pode ser sobrescrito para lógicas específicas

### 3. save_documents
```python
def save_documents(self, metadata: Dict[str, Any]):
    """Salva documentos no storage."""
    self.storage.save(self.chunks, metadata)
```
- Interface com sistema de storage
- Gerencia persistência
- Associa metadados aos chunks
- Chamado após processamento

## Implementação de Subclasse

### 1. Exemplo Básico
```python
class SimpleKnowledgeSource(BaseKnowledgeSource):
    content: str

    def load_content(self) -> Dict[Any, str]:
        return {"content": self.content}

    def add(self) -> None:
        content_dict = self.load_content()
        for key, text in content_dict.items():
            chunks = self._chunk_text(text)
            self.chunks.extend(chunks)
        self.save_documents(self.metadata)
```

### 2. Exemplo com Processamento
```python
class ProcessingKnowledgeSource(BaseKnowledgeSource):
    def preprocess(self, text: str) -> str:
        # Lógica de pré-processamento
        return processed_text

    def load_content(self) -> Dict[Any, str]:
        raw_content = self._load_raw()
        return {
            "processed": self.preprocess(raw_content)
        }

    def add(self) -> None:
        content = self.load_content()
        for text in content.values():
            self.chunks.extend(self._chunk_text(text))
        self.save_documents(self.metadata)
```

## Configuração e Uso

### 1. Configuração Básica
```python
source = SimpleKnowledgeSource(
    chunk_size=1000,
    chunk_overlap=100,
    metadata={"tipo": "texto"}
)
```

### 2. Storage Customizado
```python
storage = KnowledgeStorage(
    persistence_dir="./knowledge_db",
    collection="documentos"
)
source = SimpleKnowledgeSource(
    storage=storage,
    collection_name="colecao_1"
)
```

### 3. Pipeline Completo
```python
source = ProcessingKnowledgeSource(
    chunk_size=2000,
    chunk_overlap=150,
    metadata={
        "fonte": "arquivo",
        "processamento": "avançado"
    }
)
source.add()  # Executa pipeline completo
```

## Melhores Práticas

### 1. Gerenciamento de Memória
```python
class EfficientSource(BaseKnowledgeSource):
    def add(self) -> None:
        for chunk in self._generate_chunks():
            self.process_chunk(chunk)
            self.save_chunk(chunk)
```

### 2. Validação
```python
class ValidatedSource(BaseKnowledgeSource):
    def load_content(self) -> Dict[Any, str]:
        content = self._load()
        self._validate_content(content)
        return content

    def _validate_content(self, content):
        if not content:
            raise ValueError("Conteúdo vazio")
```

### 3. Logging
```python
class LoggedSource(BaseKnowledgeSource):
    def add(self) -> None:
        logger.info("Iniciando processamento")
        try:
            super().add()
            logger.info("Processamento concluído")
        except Exception as e:
            logger.error(f"Erro: {e}")
            raise
```

## Extensibilidade

### 1. Chunking Personalizado
```python
class CustomChunkingSource(BaseKnowledgeSource):
    def _chunk_text(self, text: str) -> List[str]:
        # Implementação personalizada de chunking
        return custom_chunks
```

### 2. Pipeline Estendido
```python
class ExtendedSource(BaseKnowledgeSource):
    def add(self) -> None:
        content = self.load_content()
        processed = self.preprocess(content)
        enhanced = self.enhance(processed)
        chunks = self._chunk_text(enhanced)
        self.chunks.extend(chunks)
        self.save_documents(self.metadata)
```

## Conclusão
`BaseKnowledgeSource` fornece uma fundação robusta e flexível para o sistema de conhecimento do CrewAI. Sua arquitetura permite fácil extensão e customização, enquanto mantém consistência no processamento e armazenamento de conhecimento.
