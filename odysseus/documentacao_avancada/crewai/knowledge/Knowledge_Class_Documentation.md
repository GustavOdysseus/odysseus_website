# Knowledge Class Documentation

## Visão Geral
O arquivo `knowledge.py` implementa a classe central `Knowledge` do sistema de gerenciamento de conhecimento do CrewAI. Esta classe é responsável por coordenar fontes de conhecimento, armazenamento e recuperação de informações.

## Implementação Detalhada

### Imports e Configuração
```python
import os
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field

# Imports específicos do CrewAI
from crewai.knowledge.source.base_knowledge_source import BaseKnowledgeSource
from crewai.knowledge.storage.knowledge_storage import KnowledgeStorage
from crewai.utilities.constants import DEFAULT_SCORE_THRESHOLD

# Configuração do ambiente
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # Otimização para fastembed
```

### Classe Knowledge

#### Atributos
```python
class Knowledge(BaseModel):
    sources: List[BaseKnowledgeSource] = Field(default_factory=list)
    model_config = ConfigDict(arbitrary_types_allowed=True)
    storage: KnowledgeStorage = Field(default_factory=KnowledgeStorage)
    embedder_config: Optional[Dict[str, Any]] = None
    collection_name: Optional[str] = None
```

#### Construtor
```python
def __init__(
    self,
    collection_name: str,
    sources: List[BaseKnowledgeSource],
    embedder_config: Optional[Dict[str, Any]] = None,
    storage: Optional[KnowledgeStorage] = None,
    **data,
):
```

##### Parâmetros:
- `collection_name`: Nome da coleção para armazenamento
- `sources`: Lista de fontes de conhecimento
- `embedder_config`: Configurações do embedder (opcional)
- `storage`: Instância de armazenamento personalizada (opcional)

##### Funcionamento:
1. Inicializa a classe base usando Pydantic
2. Configura o armazenamento:
   - Usa o storage fornecido ou
   - Cria novo KnowledgeStorage com configurações específicas
3. Armazena as fontes de conhecimento
4. Inicializa o armazenamento
5. Adiciona cada fonte ao storage

#### Método Query
```python
def query(
    self,
    query: List[str],
    limit: int = 3,
    preference: Optional[str] = None
) -> List[Dict[str, Any]]:
```

##### Parâmetros:
- `query`: Lista de strings para busca
- `limit`: Número máximo de resultados (default: 3)
- `preference`: Filtro de preferência (opcional)

##### Funcionamento:
1. Realiza busca no storage usando:
   - Queries fornecidas
   - Limite especificado
   - Filtro de preferência (se fornecido)
   - Score threshold padrão
2. Retorna resultados mais relevantes

#### Método _add_sources (Privado)
```python
def _add_sources(self):
```

##### Funcionamento:
1. Itera sobre todas as fontes
2. Associa cada fonte ao storage
3. Adiciona a fonte ao sistema

## Uso Prático

### 1. Inicialização Básica
```python
knowledge = Knowledge(
    collection_name="minha_colecao",
    sources=[fonte1, fonte2],
)
```

### 2. Configuração Avançada
```python
knowledge = Knowledge(
    collection_name="colecao_avancada",
    sources=[fonte1, fonte2],
    embedder_config={
        "model_name": "modelo_personalizado",
        "dimension": 768
    },
    storage=meu_storage_personalizado
)
```

### 3. Realizando Queries
```python
# Query simples
resultados = knowledge.query(["termo de busca"])

# Query com múltiplos termos e limite
resultados = knowledge.query(
    ["termo1", "termo2"],
    limit=5
)

# Query com preferência
resultados = knowledge.query(
    ["termo"],
    preference="categoria_especifica"
)
```

## Integração com Outros Componentes

### 1. Fontes de Conhecimento
- Integra com qualquer fonte que implemente `BaseKnowledgeSource`
- Gerencia múltiplas fontes simultaneamente
- Coordena adição e atualização de fontes

### 2. Sistema de Armazenamento
- Integração flexível com `KnowledgeStorage`
- Suporte a configurações personalizadas
- Gerenciamento automático de inicialização

### 3. Sistema de Embeddings
- Configuração flexível através de `embedder_config`
- Suporte a diferentes modelos de embedding
- Otimização de performance

## Considerações de Performance

### 1. Inicialização
- A inicialização é otimizada para carregar fontes eficientemente
- O storage é inicializado apenas uma vez
- As fontes são adicionadas de forma incremental

### 2. Queries
- Utiliza score threshold para garantir qualidade
- Permite limitação de resultados para otimização
- Suporta filtragem eficiente

### 3. Memória
- Gerenciamento eficiente de recursos
- Carregamento sob demanda
- Otimização de cache

## Melhores Práticas

### 1. Configuração
```python
# Configuração recomendada para casos gerais
knowledge = Knowledge(
    collection_name="minha_base",
    sources=minhas_fontes,
    embedder_config={
        "model_name": "BAAI/bge-small-en-v1.5",
        "cache_dir": "./cache"
    }
)
```

### 2. Queries
```python
# Busca otimizada com múltiplos termos
resultados = knowledge.query(
    ["termo principal", "termo contextual"],
    limit=3,
    preference="categoria_relevante"
)
```

### 3. Gerenciamento de Fontes
```python
# Adicionar fontes de forma organizada
fontes = [
    FonteDocumento("docs/"),
    FonteAPI("https://api.exemplo.com"),
    FonteBancoDados("conexao_db")
]
knowledge = Knowledge(collection_name="base", sources=fontes)
```

## Extensibilidade

### 1. Criando Novas Fontes
```python
class MinhaFonte(BaseKnowledgeSource):
    def add(self):
        # Implementação personalizada
        pass
```

### 2. Personalizando Storage
```python
class MeuStorage(KnowledgeStorage):
    def initialize_knowledge_storage(self):
        # Implementação personalizada
        pass
```

## Conclusão
A classe `Knowledge` é o componente central do sistema de conhecimento do CrewAI, oferecendo uma interface robusta e flexível para gerenciamento de conhecimento. Sua implementação permite fácil extensão e personalização, mantendo alta performance e confiabilidade.
