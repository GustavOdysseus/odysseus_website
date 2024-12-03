# TextFileKnowledgeSource - Documentação

## Visão Geral
`TextFileKnowledgeSource` é uma implementação especializada de `BaseFileKnowledgeSource` projetada para processar e armazenar conteúdo de arquivos de texto como fonte de conhecimento no CrewAI. Esta classe é ideal para trabalhar com arquivos `.txt` e outros formatos de texto plano.

## Estrutura da Classe

```python
class TextFileKnowledgeSource(BaseFileKnowledgeSource):
    """Fonte de conhecimento para conteúdo de arquivos de texto usando embeddings."""
```

### Herança
- Estende: `BaseFileKnowledgeSource`
- Herda: Funcionalidades de manipulação de arquivos
- Implementa: Processamento específico para texto

## Métodos Principais

### 1. load_content
```python
def load_content(self) -> Dict[Path, str]:
    """Carrega e pré-processa conteúdo do arquivo de texto."""
    super().load_content()
    paths = [self.file_path] if isinstance(self.file_path, Path) else self.file_path
    content = {}
    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            content[path] = f.read()
    return content
```

#### Pipeline de Processamento
1. Validação do arquivo
2. Normalização do caminho
3. Leitura do texto com UTF-8
4. Retorno do conteúdo

### 2. add
```python
def add(self) -> None:
    """
    Adiciona conteúdo do arquivo de texto à fonte de conhecimento,
    divide em chunks, computa embeddings e salva.
    """
    for _, text in self.content.items():
        new_chunks = self._chunk_text(text)
        self.chunks.extend(new_chunks)
    self.save_documents(metadata=self.metadata)
```

### 3. _chunk_text
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
from pathlib import Path
from crewai.knowledge.source import TextFileKnowledgeSource

source = TextFileKnowledgeSource(
    file_path=Path("documento.txt"),
    chunk_size=1000,
    chunk_overlap=100
)
source.add()
```

### 2. Com Metadados
```python
source = TextFileKnowledgeSource(
    file_path=Path("dados.txt"),
    metadata={
        "tipo": "texto",
        "departamento": "documentacao",
        "versao": "1.0"
    }
)
source.add()
```

### 3. Múltiplos Arquivos
```python
source = TextFileKnowledgeSource(
    file_path=[
        Path("arquivo1.txt"),
        Path("arquivo2.txt"),
        Path("arquivo3.txt")
    ],
    chunk_size=500,
    chunk_overlap=50
)
source.add()
```

## Configurações Avançadas

### 1. Processamento de Texto Avançado
```python
class EnhancedTextFileSource(TextFileKnowledgeSource):
    def preprocess_text(self, text: str) -> str:
        # Remove linhas vazias extras
        text = "\n".join(line for line in text.splitlines() if line.strip())
        # Normaliza espaços
        text = " ".join(text.split())
        # Remove caracteres especiais
        text = "".join(char for char in text if char.isprintable())
        return text

    def load_content(self) -> Dict[Path, str]:
        content = super().load_content()
        return {path: self.preprocess_text(text) for path, text in content.items()}
```

### 2. Suporte a Diferentes Encodings
```python
class MultiEncodingTextSource(TextFileKnowledgeSource):
    def __init__(self, *args, encoding: str = "utf-8", **kwargs):
        super().__init__(*args, **kwargs)
        self.encoding = encoding

    def load_content(self) -> Dict[Path, str]:
        super().load_content()  # Validação
        paths = [self.file_path] if isinstance(self.file_path, Path) else self.file_path
        content = {}
        
        for path in paths:
            try:
                with path.open("r", encoding=self.encoding) as f:
                    content[path] = f.read()
            except UnicodeDecodeError:
                # Tenta detectar encoding
                import chardet
                with open(path, "rb") as f:
                    raw = f.read()
                    detected = chardet.detect(raw)
                    with path.open("r", encoding=detected["encoding"]) as f2:
                        content[path] = f2.read()
        return content
```

### 3. Chunks Inteligentes
```python
class SmartChunkTextSource(TextFileKnowledgeSource):
    def _chunk_text(self, text: str) -> List[str]:
        # Divide por parágrafos
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= self.chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
```

## Melhores Práticas

### 1. Tratamento de Erros
```python
class RobustTextFileSource(TextFileKnowledgeSource):
    def load_content(self) -> Dict[Path, str]:
        try:
            return super().load_content()
        except UnicodeDecodeError as e:
            raise ValueError(f"Erro de encoding em {self.file_path}: {e}")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Arquivo não encontrado: {e.filename}")
        except PermissionError as e:
            raise PermissionError(f"Sem permissão para ler {e.filename}")
        except Exception as e:
            raise RuntimeError(f"Erro ao processar {self.file_path}: {e}")
```

### 2. Logging
```python
import logging

class LoggedTextFileSource(TextFileKnowledgeSource):
    def load_content(self) -> Dict[Path, str]:
        paths = [self.file_path] if isinstance(self.file_path, Path) else self.file_path
        logging.info(f"Processando {len(paths)} arquivo(s)")
        
        try:
            content = super().load_content()
            for path, text in content.items():
                logging.info(f"Arquivo {path}: {len(text)} caracteres")
            return content
        except Exception as e:
            logging.error(f"Erro no processamento: {e}")
            raise
```

### 3. Cache
```python
class CachedTextFileSource(TextFileKnowledgeSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cache = {}

    def load_content(self) -> Dict[Path, str]:
        paths = [self.file_path] if isinstance(self.file_path, Path) else self.file_path
        content = {}
        
        for path in paths:
            if path in self._cache:
                content[path] = self._cache[path]
            else:
                with path.open("r", encoding="utf-8") as f:
                    text = f.read()
                    self._cache[path] = text
                    content[path] = text
                    
        return content
```

## Considerações de Performance

### 1. Memória
- Leitura eficiente de arquivos
- Chunking otimizado
- Cache inteligente

### 2. Processamento
- Validações rápidas
- Divisão eficiente em chunks
- Detecção de encoding

### 3. Storage
- Integração eficiente com sistema de storage
- Metadados otimizados
- Gerenciamento de chunks

## Boas Práticas de Segurança

### 1. Validação de Entrada
- Verificação de tamanho do arquivo
- Validação de encoding
- Sanitização de texto

### 2. Recursos
- Limite de tamanho de arquivo
- Timeout para processamento
- Limite de chunks

### 3. Sanitização
- Remoção de caracteres perigosos
- Normalização de texto
- Validação de encoding

## Conclusão
`TextFileKnowledgeSource` oferece uma implementação robusta e flexível para processar arquivos de texto como fonte de conhecimento no CrewAI. Sua simplicidade e eficiência a tornam ideal para casos de uso que envolvem processamento de arquivos de texto plano, mantendo a extensibilidade do sistema.
