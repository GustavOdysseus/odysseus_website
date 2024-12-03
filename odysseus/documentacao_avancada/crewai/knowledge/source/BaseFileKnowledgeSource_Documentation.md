# BaseFileKnowledgeSource - Documentação

## Visão Geral
`BaseFileKnowledgeSource` é a classe base para todas as fontes de conhecimento que carregam conteúdo a partir de arquivos no CrewAI. Esta classe estende `BaseKnowledgeSource` e fornece funcionalidades comuns para manipulação de arquivos.

## Estrutura da Classe

```python
class BaseFileKnowledgeSource(BaseKnowledgeSource):
    file_path: Union[Path, List[Path]]
    content: Dict[Path, str]
    storage: KnowledgeStorage
```

### Atributos

1. `file_path`
   - Tipo: `Union[Path, List[Path]]`
   - Obrigatório: Sim
   - Descrição: Caminho ou lista de caminhos para os arquivos fonte
   - Validação: Verifica existência e tipo do arquivo

2. `content`
   - Tipo: `Dict[Path, str]`
   - Inicialização: Automática via `model_post_init`
   - Armazena: Mapeamento de caminhos para conteúdo
   - Acesso: Interno à classe

3. `storage`
   - Tipo: `KnowledgeStorage`
   - Padrão: Nova instância de `KnowledgeStorage`
   - Propósito: Gerenciamento de armazenamento persistente

## Métodos

### 1. model_post_init
```python
def model_post_init(self, _):
    """Método de pós-inicialização para carregar conteúdo."""
    self.content = self.load_content()
```
- Chamado automaticamente após inicialização
- Carrega conteúdo dos arquivos
- Popula o dicionário `content`

### 2. load_content
```python
def load_content(self) -> Dict[Path, str]:
    """Carrega e pré-processa conteúdo do arquivo."""
    paths = [self.file_path] if isinstance(self.file_path, Path) else self.file_path

    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")
    return {}
```
- Método abstrato base
- Deve ser sobrescrito por subclasses
- Realiza validações básicas:
  - Existência do arquivo
  - Tipo do caminho (deve ser arquivo)

### 3. save_documents
```python
def save_documents(self, metadata: Dict[str, Any]):
    """Salva os documentos no storage."""
    chunk_metadatas = [metadata.copy() for _ in self.chunks]
    self.storage.save(self.chunks, chunk_metadatas)
```
- Salva documentos no storage
- Cria metadados para cada chunk
- Utiliza o storage configurado

## Uso

### 1. Implementação Básica
```python
class TextFileKnowledgeSource(BaseFileKnowledgeSource):
    def load_content(self) -> Dict[Path, str]:
        content = {}
        paths = [self.file_path] if isinstance(self.file_path, Path) else self.file_path
        
        for path in paths:
            super().load_content()  # Validação
            with open(path, 'r', encoding='utf-8') as f:
                content[path] = f.read()
        return content
```

### 2. Uso com Arquivo Único
```python
source = TextFileKnowledgeSource(
    file_path=Path("documento.txt"),
    chunk_size=1000
)
source.add()
```

### 3. Uso com Múltiplos Arquivos
```python
source = TextFileKnowledgeSource(
    file_path=[
        Path("doc1.txt"),
        Path("doc2.txt")
    ]
)
source.add()
```

## Validações e Erros

### 1. Arquivo Não Encontrado
```python
try:
    source = TextFileKnowledgeSource(file_path=Path("inexistente.txt"))
except FileNotFoundError as e:
    print(f"Erro: {e}")  # "File not found: inexistente.txt"
```

### 2. Caminho Inválido
```python
try:
    source = TextFileKnowledgeSource(file_path=Path("./diretorio"))
except ValueError as e:
    print(f"Erro: {e}")  # "Path is not a file: ./diretorio"
```

## Metadados e Storage

### 1. Configuração de Metadados
```python
source = TextFileKnowledgeSource(
    file_path=Path("doc.txt"),
    metadata={
        "tipo": "texto",
        "autor": "João Silva",
        "versao": "1.0"
    }
)
```

### 2. Storage Personalizado
```python
storage = KnowledgeStorage(
    persistence_dir="./custom_storage"
)
source = TextFileKnowledgeSource(
    file_path=Path("doc.txt"),
    storage=storage
)
```

## Melhores Práticas

### 1. Validação de Arquivo
```python
def load_content(self) -> Dict[Path, str]:
    super().load_content()  # Sempre chamar validação base
    # Implementação específica
```

### 2. Gerenciamento de Recursos
```python
def load_content(self) -> Dict[Path, str]:
    content = {}
    for path in self._get_paths():
        with path.open('r') as f:  # Uso de context manager
            content[path] = f.read()
    return content
```

### 3. Tratamento de Encoding
```python
def load_content(self) -> Dict[Path, str]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='latin-1') as f:
            content = f.read()
    return {path: content}
```

## Extensibilidade

### 1. Pré-processamento
```python
class EnhancedFileSource(BaseFileKnowledgeSource):
    def preprocess_content(self, content: str) -> str:
        # Lógica de pré-processamento
        return processed_content

    def load_content(self) -> Dict[Path, str]:
        raw_content = super().load_content()
        return {
            path: self.preprocess_content(content)
            for path, content in raw_content.items()
        }
```

### 2. Validação Adicional
```python
class SecureFileSource(BaseFileKnowledgeSource):
    allowed_extensions = {'.txt', '.md'}

    def validate_file(self, path: Path):
        super().load_content()  # Validação base
        if path.suffix not in self.allowed_extensions:
            raise ValueError(f"Extensão não permitida: {path.suffix}")
```

## Considerações de Performance

### 1. Carregamento Lazy
```python
class LazyFileSource(BaseFileKnowledgeSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._loaded = False
        self._content = {}

    @property
    def content(self):
        if not self._loaded:
            self._content = self.load_content()
            self._loaded = True
        return self._content
```

### 2. Processamento em Chunks
```python
def process_large_file(self, path: Path) -> str:
    content = []
    with path.open('r') as f:
        while chunk := f.read(8192):  # 8KB chunks
            content.append(chunk)
    return ''.join(content)
```

## Conclusão
`BaseFileKnowledgeSource` fornece uma base sólida para implementação de fontes de conhecimento baseadas em arquivos no CrewAI. Sua arquitetura flexível permite fácil extensão para diferentes tipos de arquivos enquanto mantém um conjunto consistente de validações e comportamentos base.
