# JSONKnowledgeSource - Documentação

## Visão Geral
`JSONKnowledgeSource` é uma implementação especializada de `BaseFileKnowledgeSource` projetada para processar e armazenar conteúdo de arquivos JSON como fonte de conhecimento no CrewAI. A classe utiliza o módulo `json` nativo do Python para manipulação eficiente de dados JSON.

## Estrutura da Classe

```python
class JSONKnowledgeSource(BaseFileKnowledgeSource):
    """Fonte de conhecimento para conteúdo de arquivos JSON usando embeddings."""
```

### Herança
- Estende: `BaseFileKnowledgeSource`
- Herda: Funcionalidades de manipulação de arquivos
- Implementa: Processamento específico para JSON

## Dependências

### Módulos Python
```python
import json
from typing import Any, Dict, List
from pathlib import Path
```

## Métodos Principais

### 1. load_content
```python
def load_content(self) -> Dict[Path, str]:
    """Carrega e pré-processa conteúdo do arquivo JSON."""
    super().load_content()  # Validação do caminho
    paths = [self.file_path] if isinstance(self.file_path, Path) else self.file_path

    content: Dict[Path, str] = {}
    for path in paths:
        with open(path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        content[path] = self._json_to_text(data)
    return content
```

#### Pipeline de Processamento
1. Validação do arquivo
2. Normalização do caminho
3. Leitura do JSON
4. Conversão para texto
5. Retorno do conteúdo formatado

### 2. _json_to_text
```python
def _json_to_text(self, data: Any, level: int = 0) -> str:
    """Converte recursivamente dados JSON para representação textual."""
    text = ""
    indent = "  " * level
    if isinstance(data, dict):
        for key, value in data.items():
            text += f"{indent}{key}: {self._json_to_text(value, level + 1)}\n"
    elif isinstance(data, list):
        for item in data:
            text += f"{indent}- {self._json_to_text(item, level + 1)}\n"
    else:
        text += f"{str(data)}"
    return text
```

#### Características
- Processamento recursivo
- Formatação hierárquica
- Suporte a estruturas aninhadas
- Indentação inteligente

### 3. add
```python
def add(self) -> None:
    """
    Adiciona conteúdo JSON à fonte de conhecimento, divide em chunks,
    computa embeddings e salva.
    """
    content_str = str(self.content) if isinstance(self.content, dict) else self.content
    new_chunks = self._chunk_text(content_str)
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
from pathlib import Path
from crewai.knowledge.source import JSONKnowledgeSource

source = JSONKnowledgeSource(
    file_path=Path("dados.json"),
    chunk_size=1000,
    chunk_overlap=100
)
source.add()
```

### 2. Com Metadados
```python
source = JSONKnowledgeSource(
    file_path=Path("config.json"),
    metadata={
        "tipo": "configuracao",
        "ambiente": "producao",
        "versao": "1.0"
    }
)
source.add()
```

### 3. Storage Personalizado
```python
from crewai.knowledge.storage import KnowledgeStorage

storage = KnowledgeStorage(
    persistence_dir="./json_knowledge"
)

source = JSONKnowledgeSource(
    file_path=Path("dados.json"),
    storage=storage,
    collection_name="configs_2024"
)
source.add()
```

## Configurações Avançadas

### 1. Processamento de JSON Complexo
```python
class EnhancedJSONSource(JSONKnowledgeSource):
    def _json_to_text(self, data: Any, level: int = 0) -> str:
        text = super()._json_to_text(data, level)
        # Adiciona metadados extras
        if isinstance(data, dict):
            text += f"\nTotal de campos: {len(data)}\n"
            text += f"Tipos de dados: {set(type(v).__name__ for v in data.values())}\n"
        return text
```

### 2. Validação de Esquema
```python
from jsonschema import validate

class ValidatedJSONSource(JSONKnowledgeSource):
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"}
        },
        "required": ["id", "data"]
    }

    def load_content(self) -> Dict[Path, str]:
        paths = [self.file_path] if isinstance(self.file_path, Path) else self.file_path
        content: Dict[Path, str] = {}
        
        for path in paths:
            with open(path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                validate(instance=data, schema=self.schema)
                content[path] = self._json_to_text(data)
        return content
```

### 3. Processamento Assíncrono
```python
import asyncio
import aiofiles
import json

class AsyncJSONSource(JSONKnowledgeSource):
    async def async_load_content(self) -> Dict[Path, str]:
        paths = [self.file_path] if isinstance(self.file_path, Path) else self.file_path
        content: Dict[Path, str] = {}
        
        for path in paths:
            async with aiofiles.open(path, mode='r', encoding='utf-8') as f:
                content_str = await f.read()
                data = json.loads(content_str)
                content[path] = self._json_to_text(data)
        return content
```

## Melhores Práticas

### 1. Tratamento de Erros
```python
class RobustJSONSource(JSONKnowledgeSource):
    def load_content(self) -> Dict[Path, str]:
        try:
            return super().load_content()
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON inválido em {self.file_path}: {e}")
        except UnicodeDecodeError as e:
            raise ValueError(f"Encoding inválido em {self.file_path}: {e}")
        except Exception as e:
            if "No such file" in str(e):
                raise FileNotFoundError(f"Arquivo não encontrado: {self.file_path}")
            raise
```

### 2. Logging
```python
import logging

class LoggedJSONSource(JSONKnowledgeSource):
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
class CachedJSONSource(JSONKnowledgeSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_data = None

    def load_content(self) -> Dict[Path, str]:
        if self._cached_data is None:
            self._cached_data = super().load_content()
        return self._cached_data
```

## Considerações de Performance

### 1. Memória
- Processamento eficiente de JSON
- Chunking otimizado
- Cache inteligente

### 2. Processamento
- Conversão eficiente para texto
- Validações rápidas
- Suporte a processamento assíncrono

### 3. Storage
- Integração eficiente com sistema de storage
- Metadados otimizados
- Gerenciamento de chunks

## Boas Práticas de Segurança

### 1. Validação de Entrada
- Verificação de tamanho do arquivo
- Validação de esquema
- Sanitização de dados

### 2. Encoding
- UTF-8 por padrão
- Tratamento de caracteres especiais
- Detecção de encoding

### 3. Limites
- Tamanho máximo de arquivo
- Profundidade máxima de recursão
- Limite de memória

## Conclusão
`JSONKnowledgeSource` oferece uma implementação robusta e flexível para processar arquivos JSON como fonte de conhecimento no CrewAI. Sua integração com o módulo `json` nativo do Python permite manipulação eficiente de dados estruturados, mantendo a simplicidade de uso e extensibilidade do sistema.
