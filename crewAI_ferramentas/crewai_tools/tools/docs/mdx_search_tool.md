# Ferramenta de Busca MDX - Documentação

## Descrição
A Ferramenta de Busca MDX é uma solução avançada para realizar buscas semânticas em arquivos MDX (Markdown com JSX). Baseada na arquitetura RagTool e potencializada pelo EmbedChain, oferece capacidades sofisticadas de análise documental, permitindo consultas em linguagem natural e descobertas inteligentes em documentos MDX.

## Recursos Principais

### Busca Semântica Avançada
- Análise contextual profunda
- Processamento MDX otimizado
- Integração EmbedChain avançada
- Cache inteligente
- Retry automático
- Validação de sintaxe
- Monitoramento em tempo real
- Otimização de busca
- Indexação eficiente
- Parsing estruturado

### Funcionalidades MDX
1. **Processamento de Conteúdo**
   - Parsing JSX
   - Extração Markdown
   - Análise de componentes
   - Processamento de frontmatter
   - Extração de metadados
   - Transformação
   - Serialização
   - Normalização

2. **Gerenciamento de Documento**
   - Validação de formato
   - Controle de versão
   - Backup automático
   - Compressão
   - Caching
   - Indexação
   - Parsing
   - Otimização

3. **Análise Avançada**
   - Processamento semântico
   - Análise estrutural
   - Extração de padrões
   - Classificação
   - Categorização
   - Sumarização
   - Clustering
   - Relevância

4. **Segurança**
   - Validação de sintaxe
   - Controle de acesso
   - Logging de operações
   - Backup
   - Sanitização
   - Auditoria
   - Compliance
   - Integridade

## Arquitetura do Sistema

### 1. Schemas de Entrada

#### FixedMDXSearchToolSchema
- Parâmetros Obrigatórios:
  - `search_query`: Query de busca
- Parâmetros Opcionais:
  - `max_results`: Limite de resultados
  - `min_relevance`: Relevância mínima
  - `timeout`: Tempo limite
  - `sort_by`: Ordenação
  - `filter_duplicates`: Filtrar duplicados
  - `include_frontmatter`: Incluir frontmatter
  - `parse_components`: Analisar componentes

#### MDXSearchToolSchema
- Parâmetros Obrigatórios:
  - `search_query`: Query de busca
  - `mdx`: Caminho do arquivo
- Parâmetros Opcionais:
  - `max_results`: Limite de resultados
  - `min_relevance`: Relevância mínima
  - `timeout`: Tempo limite
  - `sort_by`: Ordenação
  - `filter_duplicates`: Filtrar duplicados
  - `include_frontmatter`: Incluir frontmatter
  - `parse_components`: Analisar componentes

### 2. Processamento
- Herança RagTool otimizada
- Processamento MDX avançado
- Cache inteligente
- Retry mechanism
- Validação de sintaxe
- Compressão eficiente
- Logging estruturado
- Monitoramento contínuo
- Indexação otimizada
- Parsing avançado

## Exemplo de Implementação

```python
# Configuração Avançada
ferramenta = MDXSearchTool(
    mdx="/caminho/para/documento.mdx",
    max_results=100,
    min_relevance=0.7,
    timeout=300,
    sort_by="relevance",
    filter_duplicates=True,
    cache_enabled=True,
    validate_syntax=True,
    include_frontmatter=True,
    parse_components=True,
    compression=True
)

# Busca Básica
resultado = ferramenta.run(
    search_query="conceito específico no documento"
)

# Busca Avançada
resultado = ferramenta.run(
    search_query="análise de padrões em componentes",
    mdx="/outro/arquivo.mdx",
    max_results=50,
    min_relevance=0.8,
    sort_by="position",
    filter_duplicates=True,
    timeout=60,
    include_frontmatter=True
)
```

## Requisitos Técnicos
- EmbedChain Framework
- Python 3.7+
- MDX Parser
- remark-mdx
- @mdx-js/mdx
- Memória adequada
- CPU suficiente
- Espaço em disco
- Dependências base
- Recursos adequados
- SO compatível

## Recursos Especiais
- Busca semântica avançada
- MDX otimizado
- Análise contextual
- Cache adaptativo
- Retry automático
- Validação robusta
- Compressão otimizada
- Backup automático
- Monitoramento real-time
- Alertas de falha
- Exportação personalizada
- Filtragem avançada
- Análise estatística
- Parsing estruturado

## Limitações e Considerações
- Tamanho do arquivo
- Estrutura do conteúdo
- Tempo de processamento
- Uso de memória
- Complexidade JSX
- Timeouts
- Falhas de parsing
- Permissões
- Performance
- Concorrência
- Validação
- Compatibilidade

## Notas de Implementação
- Validar MDX
- Configurar parsing
- Implementar cache
- Gerenciar recursos
- Otimizar busca
- Implementar retry
- Tratar erros
- Monitorar uso
- Implementar logging
- Backup de dados
- Validar sintaxe
- Gerenciar timeouts
- Otimizar parsing
- Comprimir dados
- Monitorar operações
- Validar componentes
- Documentar operações
- Manter logs
- Testar performance
- Validar resultados
- Implementar alertas
- Documentar mudanças
- Testes automatizados
- Otimização contínua
