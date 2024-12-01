# Documentação do Sistema de Memória do Usuário (UserMemory)

## Visão Geral

O sistema de Memória do Usuário do CrewAI é uma implementação especializada para gerenciar informações relacionadas aos usuários do sistema. Este componente é projetado para manter um registro persistente de dados e preferências do usuário, permitindo uma experiência personalizada e contextualizada.

## Estrutura do Sistema

### 1. UserMemoryItem

```python
class UserMemoryItem:
    def __init__(self, data: Any, user: str, metadata: Optional[Dict[str, Any]] = None):
        self.data = data
        self.user = user
        self.metadata = metadata if metadata is not None else {}
```

#### Atributos:
- `data`: Dados principais do usuário
- `user`: Identificador do usuário
- `metadata`: Metadados adicionais (opcional)

### 2. UserMemory

```python
class UserMemory(Memory):
    def __init__(self, crew=None):
        # Inicialização do sistema de memória
```

#### Características:
- Herda da classe base Memory
- Requer provedor mem0
- Integração com crew
- Armazenamento dedicado

## Componentes Principais

### 1. Inicialização

#### Parâmetros:
- `crew`: Configuração da crew (opcional)

#### Processo de Inicialização:
1. Verifica instalação do mem0
2. Configura storage específico
3. Inicializa sistema base
4. Prepara ambiente

### 2. Armazenamento de Memória

```python
def save(
    self,
    value,
    metadata: Optional[Dict[str, Any]] = None,
    agent: Optional[str] = None,
) -> None:
```

#### Funcionalidade:
- Salva dados do usuário
- Gerencia metadados
- Formata informações
- Mantém contexto

#### Formato de Dados:
```
Remember the details about the user: [dados]
```

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
- Busca contextual
- Limita resultados
- Filtra por relevância
- Retorna histórico

## Integração com Mem0

### 1. Requisitos
- Instalação obrigatória
- Configuração específica
- Tipo "user"
- Integração crew

### 2. Funcionalidades
- Armazenamento persistente
- Busca semântica
- Gestão de contexto
- Personalização

## Casos de Uso

### 1. Armazenamento de Perfil
```python
memory = UserMemory()
memory.save(
    value="Usuário prefere análises técnicas e tem foco em criptomoedas",
    metadata={"preferências": "análise_técnica", "mercado": "crypto"}
)
```

### 2. Busca de Preferências
```python
# Busca preferências do usuário
resultados = memory.search(
    query="preferências de análise",
    limit=3,
    score_threshold=0.35
)
```

### 3. Atualização de Contexto
```python
# Atualiza informações do usuário
memory.save(
    value="Usuário atualizou foco para análise fundamentalista",
    metadata={"update": "preferências"}
)
```

## Melhores Práticas

### 1. Gestão de Dados
- Mantenha dados atualizados
- Estruture informações
- Priorize relevância
- Gerencie contexto

### 2. Personalização
- Capture preferências
- Mantenha histórico
- Adapte respostas
- Evolua perfil

### 3. Privacidade
- Proteja dados
- Limite acesso
- Gerencie consentimento
- Mantenha conformidade

## Considerações de Implementação

### 1. Instalação
- Instale mem0
- Configure ambiente
- Verifique dependências
- Teste integração

### 2. Configuração
- Ajuste thresholds
- Configure limites
- Otimize busca
- Monitore uso

### 3. Manutenção
- Atualize dados
- Limpe obsoletos
- Verifique integridade
- Monitore performance

## Segurança e Privacidade

### 1. Proteção de Dados
- Criptografe sensíveis
- Controle acesso
- Audite uso
- Mantenha logs

### 2. Conformidade
- GDPR/LGPD
- Direitos do usuário
- Políticas de retenção
- Documentação legal

## Extensibilidade

### 1. Personalização
- Expanda metadados
- Adicione campos
- Melhore contexto
- Evolua modelo

### 2. Integração
- APIs externas
- Sistemas legados
- Novas fontes
- Serviços adicionais

## Otimização de Performance

### 1. Armazenamento
- Cache eficiente
- Índices otimizados
- Compressão adequada
- Gestão de recursos

### 2. Recuperação
- Busca rápida
- Relevância precisa
- Priorização inteligente
- Cache contextual

## Conclusão

O sistema de Memória do Usuário do CrewAI oferece:

1. Gestão personalizada de dados
2. Busca contextual eficiente
3. Privacidade robusta
4. Extensibilidade flexível
5. Performance otimizada

Esta implementação é crucial para:
- Personalização de experiência
- Consistência de interação
- Privacidade de dados
- Evolução contínua

O sistema equilibra:
- Personalização
- Privacidade
- Performance
- Usabilidade

## Notas de Desenvolvimento

### Limitações Atuais
- Requer mem0 instalado
- Formato fixo de mensagem
- TODO: Melhorar função save

### Próximos Passos
1. Implementar casos especiais na função save
2. Expandir capacidades de metadados
3. Melhorar formatação de dados
4. Adicionar validações
