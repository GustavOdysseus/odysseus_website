# ExcelKnowledgeSource - Documentação

## Visão Geral
`ExcelKnowledgeSource` é uma implementação especializada de `BaseFileKnowledgeSource` projetada para processar e armazenar conteúdo de arquivos Excel como fonte de conhecimento no CrewAI. A classe utiliza pandas e openpyxl para manipulação eficiente de arquivos Excel.

## Estrutura da Classe

```python
class ExcelKnowledgeSource(BaseFileKnowledgeSource):
    """Fonte de conhecimento para conteúdo de arquivos Excel usando embeddings."""
```

### Herança
- Estende: `BaseFileKnowledgeSource`
- Herda: Funcionalidades de manipulação de arquivos
- Implementa: Processamento específico para Excel

## Dependências

### 1. Principais
```python
import pandas as pd
import openpyxl
```

### 2. Gerenciamento
```python
def _import_dependencies(self):
    """Importação dinâmica de dependências."""
    try:
        import openpyxl  # noqa
        import pandas as pd
        return pd
    except ImportError as e:
        missing_package = str(e).split()[-1]
        raise ImportError(
            f"{missing_package} is not installed. Please install it with: pip install {missing_package}"
        )
```

#### Características
- Importação dinâmica
- Verificação de disponibilidade
- Mensagens de erro informativas
- Sugestão de instalação

## Métodos Principais

### 1. load_content
```python
def load_content(self) -> Dict[Path, str]:
    """Carrega e pré-processa conteúdo do arquivo Excel."""
    super().load_content()  # Validação do caminho
    pd = self._import_dependencies()

    file_path = self.file_path[0] if isinstance(self.file_path, list) else self.file_path
    df = pd.read_excel(file_path)
    content = df.to_csv(index=False)
    return {file_path: content}
```

#### Pipeline de Processamento
1. Validação do arquivo
2. Importação de dependências
3. Normalização do caminho
4. Leitura do Excel com pandas
5. Conversão para CSV
6. Retorno do conteúdo

### 2. add
```python
def add(self) -> None:
    """
    Adiciona conteúdo do Excel à fonte de conhecimento, divide em chunks,
    computa embeddings e salva.
    """
    if isinstance(self.content, dict):
        content_str = "\n".join(str(value) for value in self.content.values())
    else:
        content_str = str(self.content)

    new_chunks = self._chunk_text(content_str)
    self.chunks.extend(new_chunks)
    self.save_documents(metadata=self.metadata)
```

#### Características
- Suporte a múltiplos formatos
- Concatenação de valores
- Chunking automático
- Integração com storage

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
from crewai.knowledge.source import ExcelKnowledgeSource

source = ExcelKnowledgeSource(
    file_path=Path("dados.xlsx"),
    chunk_size=1000,
    chunk_overlap=100
)
source.add()
```

### 2. Com Metadados
```python
source = ExcelKnowledgeSource(
    file_path=Path("planilha.xlsx"),
    metadata={
        "tipo": "excel",
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
    persistence_dir="./excel_knowledge"
)

source = ExcelKnowledgeSource(
    file_path=Path("relatorio.xlsx"),
    storage=storage,
    collection_name="relatorios_2024"
)
source.add()
```

## Configurações Avançadas

### 1. Processamento de Múltiplas Planilhas
```python
class MultiSheetExcelSource(ExcelKnowledgeSource):
    def load_content(self) -> Dict[Path, str]:
        pd = self._import_dependencies()
        file_path = self.file_path[0] if isinstance(self.file_path, list) else self.file_path
        
        # Lê todas as planilhas
        excel_file = pd.ExcelFile(file_path)
        sheets = {}
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            sheets[sheet_name] = df.to_csv(index=False)
            
        return {file_path: "\n\n".join(sheets.values())}
```

### 2. Processamento Customizado
```python
class EnhancedExcelSource(ExcelKnowledgeSource):
    def preprocess_dataframe(self, df: 'pd.DataFrame') -> 'pd.DataFrame':
        # Remove colunas vazias
        df = df.dropna(how='all', axis=1)
        # Remove linhas vazias
        df = df.dropna(how='all', axis=0)
        # Preenche valores nulos
        df = df.fillna('')
        return df

    def load_content(self) -> Dict[Path, str]:
        pd = self._import_dependencies()
        file_path = self.file_path[0] if isinstance(self.file_path, list) else self.file_path
        
        df = pd.read_excel(file_path)
        df = self.preprocess_dataframe(df)
        return {file_path: df.to_csv(index=False)}
```

### 3. Validação Avançada
```python
class ValidatedExcelSource(ExcelKnowledgeSource):
    required_columns = ["id", "nome", "valor"]

    def validate_excel(self, df: 'pd.DataFrame'):
        missing = set(self.required_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Colunas obrigatórias faltando: {missing}")

    def load_content(self) -> Dict[Path, str]:
        pd = self._import_dependencies()
        file_path = self.file_path[0] if isinstance(self.file_path, list) else self.file_path
        
        df = pd.read_excel(file_path)
        self.validate_excel(df)
        return {file_path: df.to_csv(index=False)}
```

## Melhores Práticas

### 1. Tratamento de Erros
```python
class RobustExcelSource(ExcelKnowledgeSource):
    def load_content(self) -> Dict[Path, str]:
        try:
            return super().load_content()
        except Exception as e:
            if "No such file" in str(e):
                raise FileNotFoundError(f"Arquivo não encontrado: {self.file_path}")
            if "Unsupported format" in str(e):
                raise ValueError(f"Formato não suportado: {self.file_path}")
            raise
```

### 2. Logging
```python
import logging

class LoggedExcelSource(ExcelKnowledgeSource):
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
class CachedExcelSource(ExcelKnowledgeSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_df = None

    def load_content(self) -> Dict[Path, str]:
        if self._cached_df is None:
            pd = self._import_dependencies()
            file_path = self.file_path[0] if isinstance(self.file_path, list) else self.file_path
            self._cached_df = pd.read_excel(file_path)
        return {self.file_path: self._cached_df.to_csv(index=False)}
```

## Considerações de Performance

### 1. Memória
- Uso de chunks para processamento
- Limpeza de dados desnecessários
- Cache inteligente de DataFrames

### 2. Processamento
- Conversão eficiente para CSV
- Manipulação otimizada de planilhas
- Validações rápidas

### 3. Storage
- Integração eficiente com sistema de storage
- Metadados otimizados
- Gerenciamento de chunks

## Conclusão
`ExcelKnowledgeSource` oferece uma implementação robusta e flexível para processar arquivos Excel como fonte de conhecimento no CrewAI. Sua integração com pandas e openpyxl permite manipulação eficiente de dados tabulares, enquanto mantém a simplicidade de uso e extensibilidade do sistema.
