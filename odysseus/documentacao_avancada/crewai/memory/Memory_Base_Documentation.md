# Documentação da Classe Base de Memória (memory.py)

## Visão Geral

O arquivo `memory.py` contém a implementação da classe base `Memory` que serve como fundamento para todo o sistema de memória do CrewAI. Esta classe fornece a funcionalidade básica de armazenamento e recuperação de informações, sendo a base para implementações mais especializadas como memória de longo prazo, memória de entidade e memória de usuário.

## Estrutura do Código

```python
from typing import Any, Dict, Optional, List
from crewai.memory.storage.rag_storage import RAGStorage

class Memory:
    def __init__(self, storage: RAGStorage):
        self.storage = storage

    def save(
        self,
        value: Any,
        metadata: Optional[Dict[str, Any]] = None,
        agent: Optional[str] = None,
    ) -> None:
        metadata = metadata or {}
        if agent:
            metadata["agent"] = agent
        self.storage.save(value, metadata)

    def search(
        self,
        query: str,
        limit: int = 3,
        score_threshold: float = 0.35,
    ) -> List[Any]:
        return self.storage.search(
            query=query, 
            limit=limit, 
            score_threshold=score_threshold
        )
```

## Componentes Principais

### 1. Construtor (`__init__`)

```python
def __init__(self, storage: RAGStorage):
    self.storage = storage
```

#### Funcionalidade:
- Inicializa uma nova instância da classe Memory
- Recebe um objeto de armazenamento RAG (Retrieval-Augmented Generation)
- Armazena a referência do storage para uso posterior

#### Parâmetros:
- `storage`: Instância de RAGStorage que será usada para armazenar e recuperar dados

### 2. Método Save

```python
def save(
    self,
    value: Any,
    metadata: Optional[Dict[str, Any]] = None,
    agent: Optional[str] = None,
) -> None
```

#### Funcionalidade:
- Salva um valor na memória com metadados associados
- Suporta marcação automática do agente nos metadados
- Utiliza o storage subjacente para persistência

#### Parâmetros:
- `value`: O valor a ser armazenado (pode ser de qualquer tipo)
- `metadata`: Dicionário opcional de metadados associados ao valor
- `agent`: Identificador opcional do agente que está salvando o valor

#### Comportamento:
1. Inicializa metadados vazios se não fornecidos
2. Adiciona o identificador do agente aos metadados se fornecido
3. Delega o armazenamento real para o objeto storage

### 3. Método Search

```python
def search(
    self,
    query: str,
    limit: int = 3,
    score_threshold: float = 0.35,
) -> List[Any]
```

#### Funcionalidade:
- Realiza busca semântica na memória
- Suporta limitação de resultados
- Implementa filtragem por pontuação de similaridade

#### Parâmetros:
- `query`: String de busca
- `limit`: Número máximo de resultados (padrão: 3)
- `score_threshold`: Pontuação mínima de similaridade (padrão: 0.35)

#### Retorno:
- Lista de itens encontrados que atendem aos critérios de busca

## Integração com RAG Storage

A classe Memory é projetada para trabalhar com o RAGStorage, que fornece:
1. Armazenamento baseado em vetores
2. Busca semântica eficiente
3. Gerenciamento de metadados
4. Filtragem por similaridade

## Casos de Uso

### 1. Armazenamento Básico
```python
memory = Memory(storage=RAGStorage())
memory.save("Informação importante", {"tipo": "nota"})
```

### 2. Armazenamento com Agente
```python
memory.save(
    "Resultado da análise",
    {"tipo": "análise", "prioridade": "alta"},
    agent="analista_1"
)
```

### 3. Busca com Filtros
```python
resultados = memory.search(
    "informação sobre análise",
    limit=5,
    score_threshold=0.5
)
```

## Extensibilidade

A classe Memory serve como base para extensões especializadas:

1. Memória de Longo Prazo
   - Adiciona persistência entre sessões
   - Implementa rastreamento temporal
   - Gerencia qualidade dos dados

2. Memória de Entidade
   - Adiciona classificação de entidades
   - Gerencia relacionamentos
   - Suporta consultas estruturadas

3. Memória de Usuário
   - Foca em interações do usuário
   - Gerencia preferências
   - Mantém histórico personalizado

## Melhores Práticas

### 1. Uso de Metadados
- Sempre inclua metadados relevantes
- Use chaves consistentes
- Documente a estrutura dos metadados

### 2. Busca Eficiente
- Ajuste o score_threshold conforme necessário
- Limite o número de resultados apropriadamente
- Use queries específicas e bem estruturadas

### 3. Gestão de Agentes
- Use identificadores consistentes para agentes
- Documente os agentes em uso
- Mantenha rastreabilidade das operações

## Considerações de Desempenho

1. Armazenamento
   - Monitore o tamanho dos dados armazenados
   - Evite duplicação desnecessária
   - Implemente limpeza periódica

2. Busca
   - Otimize queries frequentes
   - Ajuste parâmetros de busca
   - Monitore tempos de resposta

## Segurança

1. Validação de Dados
   - Valide inputs antes do armazenamento
   - Sanitize dados sensíveis
   - Implemente controle de acesso

2. Proteção de Dados
   - Criptografe dados sensíveis
   - Implemente backup regular
   - Monitore acesso aos dados

## Conclusão

A classe Memory fornece uma base sólida e flexível para o sistema de memória do CrewAI. Sua implementação simples mas extensível permite:

1. Armazenamento flexível de diferentes tipos de dados
2. Busca eficiente com suporte a similaridade
3. Gerenciamento robusto de metadados
4. Integração com diferentes tipos de storage
5. Base para implementações especializadas

Esta implementação equilibra simplicidade e funcionalidade, fornecendo uma base confiável para construir sistemas de memória mais complexos e especializados no CrewAI.
