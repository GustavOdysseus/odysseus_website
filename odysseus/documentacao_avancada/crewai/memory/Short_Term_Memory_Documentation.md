# Documentação do Sistema de Memória de Curto Prazo (ShortTermMemory)

## Visão Geral

O sistema de Memória de Curto Prazo do CrewAI é uma implementação especializada para gerenciar dados transitórios relacionados a tarefas e interações imediatas. Este sistema é projetado para manter informações temporárias e contextuais que são relevantes durante a execução atual de tarefas, permitindo acesso rápido a insights recentes.

## Estrutura do Sistema

### 1. ShortTermMemoryItem

```python
class ShortTermMemoryItem:
    def __init__(
        self,
        data: Any,
        agent: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.data = data
        self.agent = agent
        self.metadata = metadata if metadata is not None else {}
```

#### Atributos:
- `data`: Dados principais a serem armazenados
- `agent`: Identificador do agente (opcional)
- `metadata`: Metadados adicionais (opcional)

### 2. ShortTermMemory

```python
class ShortTermMemory(Memory):
    def __init__(self, crew=None, embedder_config=None, storage=None):
        # Inicialização do sistema de memória
```

#### Características:
- Herda da classe base Memory
- Suporta múltiplos provedores
- Configurável via embedder_config
- Integração com crew

## Componentes Principais

### 1. Inicialização

#### Parâmetros:
- `crew`: Configuração da crew (opcional)
- `embedder_config`: Configuração de embeddings
- `storage`: Sistema de armazenamento

#### Processo de Inicialização:
1. Verifica configurações da crew
2. Determina provedor de memória
3. Configura storage apropriado
4. Inicializa sistema base

### 2. Armazenamento de Memória

```python
def save(
    self,
    value: Any,
    metadata: Optional[Dict[str, Any]] = None,
    agent: Optional[str] = None,
) -> None:
```

#### Funcionalidade:
- Salva dados transitórios
- Gerencia metadados
- Associa agente (opcional)
- Formata dados conforme provedor

#### Formatos de Dados:
1. Provedor mem0:
```
Remember the following insights from Agent run: [dados]
```

2. Provedor Padrão:
- Dados diretos sem formatação especial

### 3. Recuperação de Memória

```python
def search(
    self,
    query: str,
    limit: int = 3,
    score_threshold: float = 0.35,
):
```

#### Funcionalidade:
- Busca por similaridade
- Limita resultados
- Filtra por relevância
- Retorna dados recentes

### 4. Gerenciamento de Estado

```python
def reset(self) -> None:
```

#### Funcionalidade:
- Limpa memória transitória
- Gerencia exceções
- Mantém integridade

## Integração com Storage

### 1. RAG Storage (Padrão)
- Armazenamento vetorial
- Busca semântica
- Embeddings configuráveis
- Reset seguro

### 2. Mem0 Storage (Opcional)
- Provedor externo
- Formato específico
- Instalação adicional
- Capacidades avançadas

## Casos de Uso

### 1. Armazenamento de Insight
```python
memory = ShortTermMemory()
memory.save(
    value="Análise mostra tendência de alta nos últimos 3 dias",
    metadata={"tipo": "análise_mercado"},
    agent="AgentAnalista"
)
```

### 2. Busca Contextual
```python
# Busca insights relevantes
resultados = memory.search(
    query="tendências de mercado",
    limit=3,
    score_threshold=0.35
)
```

### 3. Reset de Contexto
```python
# Limpa memória transitória
memory.reset()
```

## Melhores Práticas

### 1. Gestão de Dados
- Armazene dados relevantes
- Mantenha contexto claro
- Limite volume de dados
- Limpe regularmente

### 2. Otimização de Busca
- Use queries específicas
- Ajuste thresholds
- Limite resultados
- Monitore relevância

### 3. Gestão de Recursos
- Limpe dados obsoletos
- Monitore uso de memória
- Otimize armazenamento
- Gerencie cache

## Considerações de Implementação

### 1. Escolha do Provedor
- Avalie necessidades
- Considere volume
- Planeje crescimento
- Monitore performance

### 2. Configuração
- Ajuste embeddings
- Configure thresholds
- Otimize limites
- Monitore uso

### 3. Manutenção
- Limpe regularmente
- Monitore erros
- Atualize índices
- Gerencie recursos

## Segurança e Privacidade

### 1. Dados Sensíveis
- Evite dados críticos
- Limpe regularmente
- Controle acesso
- Monitore uso

### 2. Gestão de Acesso
- Limite acesso
- Registre operações
- Proteja dados
- Mantenha logs

## Extensibilidade

### 1. Storage Customizado
- Implemente interface
- Mantenha compatibilidade
- Documente mudanças
- Teste integrações

### 2. Funcionalidades
- Adicione filtros
- Expanda busca
- Melhore relevância
- Otimize performance

## Otimização de Performance

### 1. Armazenamento
- Otimize formato
- Comprima dados
- Gerencie cache
- Monitore uso

### 2. Recuperação
- Cache inteligente
- Busca otimizada
- Filtragem eficiente
- Priorização de dados

## Conclusão

O sistema de Memória de Curto Prazo do CrewAI oferece:

1. Gestão eficiente de dados transitórios
2. Busca contextual rápida
3. Flexibilidade de implementação
4. Performance otimizada
5. Integração seamless

Esta implementação é crucial para:
- Contexto imediato
- Insights temporários
- Decisões rápidas
- Interações fluidas

O sistema equilibra:
- Velocidade de acesso
- Relevância contextual
- Eficiência de recursos
- Simplicidade de uso
