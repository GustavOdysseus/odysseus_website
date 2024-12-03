# CSVKnowledgeSource - Documentação

## Visão Geral
`CSVKnowledgeSource` é uma implementação especializada de `BaseFileKnowledgeSource` projetada para processar e armazenar conteúdo de arquivos CSV como fonte de conhecimento no CrewAI. A classe oferece funcionalidades específicas para lidar com a estrutura tabular dos arquivos CSV.

## Estrutura da Classe

```python
class CSVKnowledgeSource(BaseFileKnowledgeSource):
    """Fonte de conhecimento para conteúdo de arquivos CSV usando embeddings."""
```

### Herança
- Estende: `BaseFileKnowledgeSource`
- Herda: Funcionalidades de manipulação de arquivos
- Implementa: Processamento específico para CSV

## Métodos Principais

### 1. load_content
```python
def load_content(self) -> Dict[Path, str]:
    """Carrega e pré-processa conteúdo do arquivo CSV."""
    super().load_content()  # Validação do caminho do arquivo

    file_path = (
        self.file_path[0] if isinstance(self.file_path, list) else self.file_path
    )
    file_path = Path(file_path) if isinstance(file_path, str) else file_path

    with open(file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        content = ""
        for row in reader:
            content += " ".join(row) + "\n"
    return {file_path: content}
```

#### Características
- Validação inicial do arquivo
- Normalização do caminho
- Leitura do CSV
- Concatenação de linhas
- Encoding UTF-8

#### Fluxo de Processamento
1. Validação do caminho
2. Normalização do tipo de caminho
3. Abertura do arquivo
4. Leitura linha a linha
5. Junção de colunas
6. Retorno do conteúdo processado

### 2. add
```python
def add(self) -> None:
    """
    Adiciona conteúdo do CSV à fonte de conhecimento, divide em chunks,
    computa embeddings e salva.
    """
    content_str = (
        str(self.content) if isinstance(self.content, dict) else self.content
    )
    new_chunks = self._chunk_text(content_str)
    self.chunks.extend(new_chunks)
    self.save_documents(metadata=self.metadata)
```

#### Características
- Processamento flexível do conteúdo
- Chunking automático
- Integração com storage
- Suporte a metadados

#### Pipeline de Processamento
1. Conversão do conteúdo
2. Divisão em chunks
3. Armazenamento dos chunks
4. Salvamento com metadados

### 3. _chunk_text
```python
def _chunk_text(self, text: str) -> List[str]:
    """Método utilitário para dividir texto em chunks."""
    return [
        text[i : i + self.chunk_size]
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap)
    ]
```

#### Características
- Implementação padrão de chunking
- Respeita configurações de tamanho
- Mantém sobreposição configurada
- Retorna lista de chunks

## Uso Prático

### 1. Inicialização Básica
```python
from pathlib import Path
from crewai.knowledge.source import CSVKnowledgeSource

source = CSVKnowledgeSource(
    file_path=Path("dados.csv"),
    chunk_size=1000,
    chunk_overlap=100
)
source.add()
```

### 2. Com Metadados
```python
source = CSVKnowledgeSource(
    file_path=Path("dados.csv"),
    metadata={
        "tipo": "csv",
        "origem": "sistema_vendas",
        "data": "2024-01-20"
    }
)
source.add()
```

### 3. Storage Personalizado
```python
from crewai.knowledge.storage import KnowledgeStorage

storage = KnowledgeStorage(
    persistence_dir="./csv_knowledge"
)

source = CSVKnowledgeSource(
    file_path=Path("dados.csv"),
    storage=storage,
    collection_name="vendas_2024"
)
source.add()
```

## Configurações Avançadas

### 1. Processamento de Grandes Arquivos
```python
class LargeCSVKnowledgeSource(CSVKnowledgeSource):
    def load_content(self) -> Dict[Path, str]:
        super().load_content()  # Validação
        content = []
        
        with open(self.file_path, "r", encoding="utf-8") as csvfile:
            for chunk in self._read_in_chunks(csvfile):
                content.append(chunk)
                
        return {self.file_path: "".join(content)}
        
    def _read_in_chunks(self, file, chunk_size=8192):
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data
```

### 2. Processamento Customizado
```python
class EnhancedCSVSource(CSVKnowledgeSource):
    def preprocess_row(self, row: List[str]) -> str:
        # Remove colunas vazias
        row = [col for col in row if col.strip()]
        # Formata dados
        return " | ".join(row)

    def load_content(self) -> Dict[Path, str]:
        super().load_content()
        content = []
        
        with open(self.file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                content.append(self.preprocess_row(row))
                
        return {self.file_path: "\n".join(content)}
```

### 3. Validação Avançada
```python
class ValidatedCSVSource(CSVKnowledgeSource):
    required_columns = ["id", "nome", "valor"]

    def validate_csv(self, file_path: Path):
        with open(file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            
            missing = set(self.required_columns) - set(headers)
            if missing:
                raise ValueError(f"Colunas obrigatórias faltando: {missing}")

    def load_content(self) -> Dict[Path, str]:
        super().load_content()
        self.validate_csv(self.file_path)
        # Continua com processamento normal
```

## Melhores Práticas

### 1. Tratamento de Encoding
```python
def load_content(self) -> Dict[Path, str]:
    try:
        return self._load_with_encoding("utf-8")
    except UnicodeDecodeError:
        return self._load_with_encoding("latin-1")

def _load_with_encoding(self, encoding: str) -> Dict[Path, str]:
    with open(self.file_path, "r", encoding=encoding) as csvfile:
        # Processamento normal
```

### 2. Logging
```python
import logging

class LoggedCSVSource(CSVKnowledgeSource):
    def load_content(self) -> Dict[Path, str]:
        logging.info(f"Iniciando processamento de {self.file_path}")
        try:
            content = super().load_content()
            logging.info("Processamento concluído com sucesso")
            return content
        except Exception as e:
            logging.error(f"Erro no processamento: {e}")
            raise
```

### 3. Cache
```python
class CachedCSVSource(CSVKnowledgeSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_content = None

    def load_content(self) -> Dict[Path, str]:
        if self._cached_content is None:
            self._cached_content = super().load_content()
        return self._cached_content
```

## Conclusão
`CSVKnowledgeSource` oferece uma implementação robusta e flexível para processar arquivos CSV como fonte de conhecimento no CrewAI. Sua arquitetura permite fácil extensão e customização, enquanto mantém a simplicidade de uso para casos básicos.
