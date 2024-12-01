# PDFKnowledgeSource - Documentação

## Visão Geral
`PDFKnowledgeSource` é uma implementação especializada de `BaseFileKnowledgeSource` projetada para processar e armazenar conteúdo de arquivos PDF como fonte de conhecimento no CrewAI. A classe utiliza a biblioteca `pdfplumber` para extração eficiente de texto de PDFs.

## Estrutura da Classe

```python
class PDFKnowledgeSource(BaseFileKnowledgeSource):
    """Fonte de conhecimento para conteúdo de arquivos PDF usando embeddings."""
```

### Herança
- Estende: `BaseFileKnowledgeSource`
- Herda: Funcionalidades de manipulação de arquivos
- Implementa: Processamento específico para PDF

## Dependências

### 1. Principais
```python
from typing import List, Dict
from pathlib import Path
import pdfplumber  # Importação dinâmica
```

### 2. Gerenciamento de Dependências
```python
def _import_pdfplumber(self):
    """Importação dinâmica do pdfplumber."""
    try:
        import pdfplumber
        return pdfplumber
    except ImportError:
        raise ImportError(
            "pdfplumber is not installed. Please install it with: pip install pdfplumber"
        )
```

## Métodos Principais

### 1. load_content
```python
def load_content(self) -> Dict[Path, str]:
    """Carrega e pré-processa conteúdo do arquivo PDF."""
    super().load_content()  # Validação dos caminhos
    pdfplumber = self._import_pdfplumber()

    paths = [self.file_path] if isinstance(self.file_path, Path) else self.file_path
    content = {}

    for path in paths:
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        content[path] = text
    return content
```

#### Pipeline de Processamento
1. Validação do arquivo
2. Importação do pdfplumber
3. Normalização do caminho
4. Extração de texto por página
5. Concatenação do conteúdo

### 2. add
```python
def add(self) -> None:
    """
    Adiciona conteúdo PDF à fonte de conhecimento, divide em chunks,
    computa embeddings e salva.
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
from crewai.knowledge.source import PDFKnowledgeSource

source = PDFKnowledgeSource(
    file_path=Path("documento.pdf"),
    chunk_size=1000,
    chunk_overlap=100
)
source.add()
```

### 2. Com Metadados
```python
source = PDFKnowledgeSource(
    file_path=Path("relatorio.pdf"),
    metadata={
        "tipo": "relatorio",
        "departamento": "financeiro",
        "ano": "2024"
    }
)
source.add()
```

### 3. Storage Personalizado
```python
from crewai.knowledge.storage import KnowledgeStorage

storage = KnowledgeStorage(
    persistence_dir="./pdf_knowledge"
)

source = PDFKnowledgeSource(
    file_path=Path("documento.pdf"),
    storage=storage,
    collection_name="documentos_2024"
)
source.add()
```

## Configurações Avançadas

### 1. Processamento de PDF Complexo
```python
class EnhancedPDFSource(PDFKnowledgeSource):
    def load_content(self) -> Dict[Path, str]:
        pdfplumber = self._import_pdfplumber()
        paths = [self.file_path] if isinstance(self.file_path, Path) else self.file_path
        content = {}

        for path in paths:
            text = ""
            with pdfplumber.open(path) as pdf:
                # Extrai metadados do PDF
                metadata = pdf.metadata
                text += f"Título: {metadata.get('Title', 'N/A')}\n"
                text += f"Autor: {metadata.get('Author', 'N/A')}\n"
                text += f"Criado em: {metadata.get('CreationDate', 'N/A')}\n\n"

                # Processa cada página
                for page in pdf.pages:
                    # Extrai texto
                    page_text = page.extract_text()
                    if page_text:
                        text += f"Página {page.page_number}:\n{page_text}\n"

                    # Extrai tabelas
                    tables = page.extract_tables()
                    if tables:
                        text += f"\nTabelas na página {page.page_number}:\n"
                        for table in tables:
                            for row in table:
                                text += " | ".join(str(cell) for cell in row) + "\n"
                            text += "\n"

            content[path] = text
        return content
```

### 2. Extração de Imagens
```python
import pytesseract
from PIL import Image
import io

class OCRPDFSource(PDFKnowledgeSource):
    def load_content(self) -> Dict[Path, str]:
        pdfplumber = self._import_pdfplumber()
        paths = [self.file_path] if isinstance(self.file_path, Path) else self.file_path
        content = {}

        for path in paths:
            text = ""
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    # Extrai texto normal
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

                    # Processa imagens com OCR
                    for image in page.images:
                        image_bytes = io.BytesIO(image['stream'].get_data())
                        img = Image.open(image_bytes)
                        ocr_text = pytesseract.image_to_string(img)
                        if ocr_text:
                            text += f"\nTexto da Imagem:\n{ocr_text}\n"

            content[path] = text
        return content
```

### 3. Processamento Assíncrono
```python
import asyncio
import aiofiles
from concurrent.futures import ThreadPoolExecutor

class AsyncPDFSource(PDFKnowledgeSource):
    async def async_load_content(self) -> Dict[Path, str]:
        pdfplumber = self._import_pdfplumber()
        paths = [self.file_path] if isinstance(self.file_path, Path) else self.file_path
        content = {}

        async def process_pdf(path):
            with pdfplumber.open(path) as pdf:
                text = ""
                with ThreadPoolExecutor() as pool:
                    # Processa páginas em paralelo
                    futures = [
                        pool.submit(lambda p: p.extract_text(), page)
                        for page in pdf.pages
                    ]
                    for future in futures:
                        page_text = future.result()
                        if page_text:
                            text += page_text + "\n"
                return text

        tasks = [process_pdf(path) for path in paths]
        results = await asyncio.gather(*tasks)
        
        for path, text in zip(paths, results):
            content[path] = text
            
        return content
```

## Melhores Práticas

### 1. Tratamento de Erros
```python
class RobustPDFSource(PDFKnowledgeSource):
    def load_content(self) -> Dict[Path, str]:
        try:
            return super().load_content()
        except Exception as e:
            if "Password required" in str(e):
                raise ValueError(f"PDF protegido por senha: {self.file_path}")
            if "No such file" in str(e):
                raise FileNotFoundError(f"Arquivo não encontrado: {self.file_path}")
            if "PDF file is damaged" in str(e):
                raise ValueError(f"PDF corrompido: {self.file_path}")
            raise
```

### 2. Logging
```python
import logging

class LoggedPDFSource(PDFKnowledgeSource):
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
class CachedPDFSource(PDFKnowledgeSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_content = {}

    def load_content(self) -> Dict[Path, str]:
        paths = [self.file_path] if isinstance(self.file_path, Path) else self.file_path
        
        # Verifica cache para cada arquivo
        missing_paths = [p for p in paths if p not in self._cached_content]
        
        if missing_paths:
            new_content = super().load_content()
            self._cached_content.update(new_content)
            
        return {path: self._cached_content[path] for path in paths}
```

## Considerações de Performance

### 1. Memória
- Processamento página por página
- Cache inteligente
- Limpeza de recursos

### 2. Processamento
- Extração eficiente de texto
- Processamento paralelo de páginas
- OCR sob demanda

### 3. Storage
- Integração eficiente com sistema de storage
- Metadados otimizados
- Gerenciamento de chunks

## Boas Práticas de Segurança

### 1. Validação de Entrada
- Verificação de tamanho do arquivo
- Validação de formato PDF
- Detecção de PDFs maliciosos

### 2. Recursos
- Limite de memória por arquivo
- Timeout para processamento
- Limite de páginas

### 3. Sanitização
- Remoção de scripts
- Validação de caracteres
- Limpeza de metadados sensíveis

## Conclusão
`PDFKnowledgeSource` oferece uma implementação robusta e flexível para processar arquivos PDF como fonte de conhecimento no CrewAI. Sua integração com `pdfplumber` permite extração eficiente de texto e dados estruturados, mantendo a simplicidade de uso e extensibilidade do sistema.
