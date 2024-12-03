# Ferramenta de Busca GitHub - Documentação

## Descrição
A Ferramenta de Busca GitHub é uma solução avançada para realizar buscas semânticas em repositórios do GitHub. Diferentemente da API oficial do GitHub, esta ferramenta oferece capacidades de busca semântica sofisticada no conteúdo dos repositórios, permitindo análises contextuais profundas e descobertas inteligentes.

## Recursos Principais

### Busca Semântica Avançada
- Análise contextual profunda em repositórios
- Processamento multi-conteúdo
- Integração EmbedChain otimizada
- Autenticação segura via token
- Cache inteligente
- Retry automático
- Validação de dados
- Monitoramento em tempo real
- Otimização de requisições
- Rate limiting adaptativo

### Tipos de Conteúdo Suportados
1. **Código (`code`)**
   - Arquivos fonte
   - Documentação
   - Configurações
   - Scripts
   - Templates
   - Testes
   - Bibliotecas
   - Módulos

2. **Repositório (`repo`)**
   - Metadados
   - Descrições
   - Tags
   - Releases
   - Branches
   - Contributors
   - Estatísticas
   - Análises

3. **Pull Requests (`pr`)**
   - Descrições
   - Comentários
   - Reviews
   - Mudanças
   - Discussões
   - Status
   - Labels
   - Histórico

4. **Issues (`issue`)**
   - Títulos
   - Descrições
   - Comentários
   - Labels
   - Milestones
   - Assignees
   - Status
   - Histórico

## Arquitetura do Sistema

### 1. Schemas de Entrada

#### FixedGithubSearchToolSchema
- Parâmetros Obrigatórios:
  - `search_query`: Query de busca
- Parâmetros Opcionais:
  - `max_results`: Limite de resultados
  - `min_relevance`: Relevância mínima
  - `timeout`: Tempo limite
  - `content_types`: Tipos de conteúdo
  - `sort_by`: Ordenação
  - `filter_duplicates`: Filtrar duplicados

#### GithubSearchToolSchema
- Parâmetros Obrigatórios:
  - `search_query`: Query de busca
  - `github_repo`: URL do repositório
- Parâmetros Opcionais:
  - `content_types`: Tipos de conteúdo
  - `max_results`: Limite de resultados
  - `min_relevance`: Relevância mínima
  - `timeout`: Tempo limite
  - `sort_by`: Ordenação
  - `filter_duplicates`: Filtrar duplicados

### 2. Processamento
- Herança RagTool otimizada
- Processamento multi-conteúdo
- Cache inteligente
- Rate limiting
- Retry mechanism
- Validação de dados
- Compressão eficiente
- Logging estruturado
- Monitoramento contínuo
- Indexação otimizada

## Exemplo de Implementação

```python
# Configuração Avançada
ferramenta = GithubSearchTool(
    github_repo="usuario/repositorio",
    gh_token="seu_token_github",
    content_types=["code", "issue", "pr", "repo"],
    max_results=100,
    min_relevance=0.7,
    timeout=300,
    sort_by="relevance",
    filter_duplicates=True,
    cache_enabled=True,
    validate_data=True
)

# Busca Básica
resultado = ferramenta.run(
    search_query="implementação de feature específica"
)

# Busca Avançada
resultado = ferramenta.run(
    search_query="análise de performance em microserviços",
    github_repo="organização/outro-repo",
    content_types=["pr", "issue", "code"],
    max_results=50,
    min_relevance=0.8,
    sort_by="date",
    filter_duplicates=True,
    timeout=60
)
```

## Requisitos Técnicos
- Token GitHub válido
- EmbedChain Framework
- Python 3.7+
- Requests
- PyGithub
- Memória adequada
- CPU suficiente
- Conexão estável
- Dependências base
- Recursos adequados
- SO compatível

## Recursos Especiais
- Busca semântica avançada
- Multi-repositório
- Análise contextual
- Cache adaptativo
- Rate limiting inteligente
- Retry automático
- Validação robusta
- Compressão otimizada
- Backup automático
- Monitoramento real-time
- Alertas de falha
- Exportação personalizada
- Filtragem avançada
- Análise estatística

## Limitações e Considerações
- Limites da API GitHub
- Uso de recursos
- Tempo de resposta
- Tamanho dos dados
- Rate limiting
- Timeouts
- Falhas de rede
- Autenticação
- Permissões
- Performance
- Concorrência
- Validação
- Compatibilidade

## Notas de Implementação
- Validar token
- Configurar rate limiting
- Implementar cache
- Gerenciar recursos
- Otimizar buscas
- Implementar retry
- Tratar erros
- Monitorar uso
- Implementar logging
- Backup de dados
- Validar respostas
- Gerenciar timeouts
- Otimizar requisições
- Comprimir dados
- Monitorar API
- Validar permissões
- Documentar operações
- Manter logs
- Testar integrações
- Validar resultados
- Implementar alertas
- Documentar mudanças
- Testes automatizados
- Otimização contínua
