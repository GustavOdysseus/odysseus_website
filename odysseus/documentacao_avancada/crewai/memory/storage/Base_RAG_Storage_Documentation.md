# Documentação do BaseRAGStorage

## Visão Geral

O `BaseRAGStorage` é uma classe abstrata base que define a interface e funcionalidades comuns para implementações de armazenamento baseadas em RAG (Retrieval-Augmented Generation) no CrewAI. Esta classe fornece a estrutura fundamental para sistemas de armazenamento que utilizam embeddings e busca semântica.

## Estrutura da Classe

```python
class BaseRAGStorage(ABC):
    app: Any | None = None

    def __init__(
        self,
        type: str,
        allow_reset: bool = True,
        embedder_config: Optional[Any] = None,
        crew: Any = None,
    ):
        # Inicialização dos atributos
```

### Atributos

#### Principais
- `app`: Aplicação/cliente do banco de dados vetorial
- `type`: Tipo do storage
- `allow_reset`: Flag para permitir reset
- `embedder_config`: Configuração do embedder
- `crew`: Referência à crew
- `agents`: String concatenada dos agentes

#### Tipos de Dados
```python
from typing import Any, Dict, List, Optional
```

## Métodos Principais

### 1. Inicialização

```python
def __init__(
    self,
    type: str,
    allow_reset: bool = True,
    embedder_config: Optional[Any] = None,
    crew: Any = None,
):
```

#### Parâmetros:
- `type`: Identificador do tipo de storage
- `allow_reset`: Permite reinicialização
- `embedder_config`: Configuração de embeddings
- `crew`: Instância da crew

### 2. Inicialização de Agentes

```python
def _initialize_agents(self) -> str:
```

#### Funcionalidade:
- Concatena nomes de agentes
- Sanitiza roles
- Retorna string única

### 3. Métodos Abstratos

#### 3.1 Sanitização de Role
```python
@abstractmethod
def _sanitize_role(self, role: str) -> str:
    """Sanitizes agent roles to ensure valid directory names."""
    pass
```

#### 3.2 Salvamento
```python
@abstractmethod
def save(self, value: Any, metadata: Dict[str, Any]) -> None:
    """Save a value with metadata to the storage."""
    pass
```

#### 3.3 Busca
```python
@abstractmethod
def search(
    self,
    query: str,
    limit: int = 3,
    filter: Optional[dict] = None,
    score_threshold: float = 0.35,
) -> List[Any]:
    """Search for entries in the storage."""
    pass
```

#### 3.4 Reset
```python
@abstractmethod
def reset(self) -> None:
    """Reset the storage."""
    pass
```

#### 3.5 Geração de Embedding
```python
@abstractmethod
def _generate_embedding(
    self, text: str, metadata: Optional[Dict[str, Any]] = None
) -> Any:
    """Generate an embedding for the given text and metadata."""
    pass
```

#### 3.6 Inicialização de App
```python
@abstractmethod
def _initialize_app(self):
    """Initialize the vector db."""
    pass
```

### 4. Métodos Opcionais

#### 4.1 Configuração
```python
def setup_config(self, config: Dict[str, Any]):
    """Setup the config of the storage."""
    pass
```

#### 4.2 Inicialização de Cliente
```python
def initialize_client(self):
    """Initialize the client of the storage."""
    pass
```

## Implementação

### 1. Fluxo de Inicialização
1. Recebe parâmetros de configuração
2. Inicializa atributos básicos
3. Configura agentes
4. Prepara ambiente

### 2. Gestão de Agentes
1. Verifica existência da crew
2. Itera sobre agentes
3. Sanitiza roles
4. Concatena identificadores

### 3. Operações de Storage
1. Salva dados com metadados
2. Busca com filtragem
3. Gerencia reset
4. Gera embeddings

## Uso

### 1. Criação de Storage
```python
class CustomRAGStorage(BaseRAGStorage):
    def __init__(self, type: str, **kwargs):
        super().__init__(type, **kwargs)
        self._initialize_app()
```

### 2. Implementação de Métodos
```python
def _sanitize_role(self, role: str) -> str:
    return role.replace(" ", "_").lower()

def save(self, value: Any, metadata: Dict[str, Any]) -> None:
    embedding = self._generate_embedding(value)
    # Implementação específica
```

### 3. Configuração
```python
storage = CustomRAGStorage(
    type="custom_memory",
    allow_reset=True,
    embedder_config={"model": "text-embedding-ada-002"}
)
```

## Melhores Práticas

### 1. Implementação
- Implemente todos os métodos abstratos
- Mantenha consistência de tipos
- Gerencie erros adequadamente
- Documente comportamentos

### 2. Configuração
- Configure embeddings apropriadamente
- Defina limites adequados
- Gerencie recursos
- Monitore performance

### 3. Extensão
- Mantenha interface consistente
- Adicione funcionalidades específicas
- Documente mudanças
- Teste extensivamente

## Considerações de Performance

### 1. Embeddings
- Otimize geração
- Cache quando possível
- Monitore uso de memória
- Gerencie batch size

### 2. Busca
- Configure thresholds
- Otimize filtros
- Limite resultados
- Cache frequentes

### 3. Recursos
- Gerencie conexões
- Monitore uso
- Implemente timeouts
- Limpe recursos

## Segurança

### 1. Sanitização
- Valide inputs
- Sanitize paths
- Proteja metadados
- Controle acesso

### 2. Configuração
- Proteja credenciais
- Valide configs
- Limite acessos
- Audite operações

## Extensibilidade

### 1. Novos Backends
- Implemente interface
- Mantenha compatibilidade
- Documente requisitos
- Teste integração

### 2. Funcionalidades
- Adicione métodos
- Expanda metadados
- Melhore busca
- Otimize performance

## Conclusão

O `BaseRAGStorage` fornece:

1. Interface consistente
2. Flexibilidade de implementação
3. Gestão de recursos
4. Extensibilidade robusta

Esta base é crucial para:
- Implementações RAG
- Busca semântica
- Gestão de memória
- Integração de agentes

O sistema equilibra:
- Abstração
- Performance
- Flexibilidade
- Segurança

## Notas de Desenvolvimento

### Limitações Atuais
- Tipagem genérica (Any)
- Configuração flexível
- Métodos opcionais vazios

### Próximos Passos
1. Tipagem mais específica
2. Validações adicionais
3. Métodos utilitários
4. Documentação expandida
