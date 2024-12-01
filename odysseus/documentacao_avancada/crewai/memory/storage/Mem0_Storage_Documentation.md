# Documentação do Mem0Storage

## Visão Geral

O `Mem0Storage` é uma implementação especializada que estende a interface `Storage` para integrar com o serviço Mem0, fornecendo capacidades avançadas de armazenamento e busca de memórias no CrewAI. Esta implementação suporta diferentes tipos de memória e gerenciamento contextual.

## Estrutura do Storage

### Importações e Dependências
```python
import os
from typing import Any, Dict, List
from mem0 import MemoryClient
from crewai.memory.storage.interface import Storage
```

### Tipos de Memória Suportados
- `user`: Memória específica do usuário
- `short_term`: Memória de curto prazo
- `long_term`: Memória de longo prazo
- `entities`: Memória de entidades

## Métodos Principais

### 1. Inicialização

```python
def __init__(self, type, crew=None):
    super().__init__()
    if type not in ["user", "short_term", "long_term", "entities"]:
        raise ValueError("Invalid type for Mem0Storage.")
    
    self.memory_type = type
    self.crew = crew
    self.memory_config = crew.memory_config
    
    user_id = self._get_user_id()
    if type == "user" and not user_id:
        raise ValueError("User ID is required for user memory type")
        
    mem0_api_key = self.memory_config.get("config", {}).get("api_key") or os.getenv("MEM0_API_KEY")
    self.memory = MemoryClient(api_key=mem0_api_key)
```

#### Características:
- Validação de tipo
- Configuração flexível
- Integração com Mem0
- Gestão de API key

### 2. Salvamento

```python
def save(self, value: Any, metadata: Dict[str, Any]) -> None:
```

#### Funcionalidades por Tipo:

1. User Memory
```python
self.memory.add(value, user_id=user_id, metadata={**metadata})
```

2. Short-Term Memory
```python
self.memory.add(
    value,
    agent_id=agent_name,
    metadata={"type": "short_term", **metadata}
)
```

3. Long-Term Memory
```python
self.memory.add(
    value,
    agent_id=agent_name,
    infer=False,
    metadata={"type": "long_term", **metadata}
)
```

4. Entity Memory
```python
self.memory.add(
    value,
    user_id=entity_name,
    metadata={"type": "entity", **metadata}
)
```

### 3. Busca

```python
def search(
    self,
    query: str,
    limit: int = 3,
    score_threshold: float = 0.35,
) -> List[Any]:
```

#### Características:
- Busca contextual
- Filtragem por tipo
- Score threshold
- Limite de resultados

### 4. Utilitários

#### Sanitização de Role
```python
def _sanitize_role(self, role: str) -> str:
    return role.replace("\n", "").replace(" ", "_").replace("/", "_")
```

#### Obtenção de User ID
```python
def _get_user_id(self):
    if self.memory_type == "user":
        if hasattr(self, "memory_config") and self.memory_config is not None:
            return self.memory_config.get("config", {}).get("user_id")
    return None
```

#### Obtenção de Agent Name
```python
def _get_agent_name(self):
    agents = self.crew.agents if self.crew else []
    agents = [self._sanitize_role(agent.role) for agent in agents]
    return "_".join(agents)
```

## Configuração

### 1. API Key
- Prioridade para config
- Fallback para env var
- Validação obrigatória
- Inicialização segura

### 2. Tipos de Memória
- Validação estrita
- Configuração específica
- Metadados apropriados
- Contexto adequado

### 3. User ID
- Obrigatório para user memory
- Configurável via config
- Validação na inicialização
- Gestão flexível

## Melhores Práticas

### 1. Configuração
- Configure API key
- Defina tipo adequado
- Valide user ID
- Gerencie crew

### 2. Salvamento
- Adicione metadados
- Use tipos corretos
- Valide dados
- Gerencie contexto

### 3. Busca
- Configure limites
- Ajuste threshold
- Filtre resultados
- Valide scores

## Considerações de Design

### 1. Estrutura
- Herança de Storage
- Tipos específicos
- Metadados flexíveis
- Configuração robusta

### 2. Operações
- Contexto específico
- Filtragem automática
- Score threshold
- Sanitização

### 3. Segurança
- API key segura
- Validação de inputs
- Sanitização de roles
- Controle de acesso

## Performance

### 1. Otimizações
- Limite de resultados
- Score threshold
- Filtragem eficiente
- Contexto específico

### 2. Monitoramento
- Validação de resultados
- Controle de erros
- Gestão de recursos
- Logging implícito

## Segurança

### 1. Credenciais
- API key segura
- Configuração flexível
- Env var fallback
- Validação obrigatória

### 2. Dados
- Sanitização de roles
- Validação de tipos
- Metadados seguros
- Controle de acesso

## Conclusão

O `Mem0Storage` fornece:

1. Integração robusta com Mem0
2. Tipos específicos de memória
3. Busca contextual avançada
4. Configuração flexível

Esta implementação é crucial para:
- Memória distribuída
- Busca semântica
- Contexto específico
- Integração externa

O sistema equilibra:
- Flexibilidade
- Segurança
- Performance
- Usabilidade

## Notas de Desenvolvimento

### Limitações Atuais
- API key obrigatória
- Tipos fixos
- Dependência externa
- Configuração específica

### Próximos Passos
1. Mais tipos de memória
2. Configuração avançada
3. Cache local
4. Métricas detalhadas

### Exemplos de Uso

```python
# Inicialização
storage = Mem0Storage(
    type="user",
    crew=crew_instance
)

# Salvamento de memória
storage.save(
    value="Informação importante",
    metadata={"contexto": "reunião"}
)

# Busca de memórias
results = storage.search(
    query="informação",
    limit=5,
    score_threshold=0.5
)
```

### Considerações de Uso

1. Configuração
- Configure API key
- Defina tipo correto
- Valide requisitos
- Gerencie crew

2. Operação
- Use tipo adequado
- Adicione metadados
- Configure busca
- Valide resultados

3. Manutenção
- Monitore uso
- Gerencie recursos
- Atualize configurações
- Valide integridade

4. Desenvolvimento
- Teste integração
- Valide tipos
- Documente mudanças
- Gerencie dependências
