# Ferramenta de Busca CSV - Documentação

## Descrição
A Ferramenta de Busca CSV é uma solução avançada para realizar buscas semânticas em arquivos CSV (Comma-Separated Values). Utiliza processamento semântico sofisticado e análise contextual para encontrar informações relevantes em dados tabulares, oferecendo recursos avançados de busca e otimização.

## Principais Recursos

### Busca Semântica em CSVs
- Processamento tabular avançado
- Busca contextual inteligente
- Suporte multi-arquivo
- Integração EmbedChain
- Análise semântica profunda
- Cache adaptativo
- Retry automático
- Validação de dados
- Monitoramento em tempo real
- Otimização de performance

### Modos de Operação
1. **Modo Fixo**
   - CSV pré-configurado
   - Busca otimizada
   - Contexto persistente
   - Cache inteligente
   - Validação contínua
   - Monitoramento de mudanças
   - Backup automático
   - Performance otimizada
   - Indexação avançada

2. **Modo Dinâmico**
   - CSV flexível
   - Seleção adaptativa
   - Contexto dinâmico
   - Validação automática
   - Detecção de alterações
   - Cache dinâmico
   - Retry inteligente
   - Monitoramento contínuo
   - Otimização em tempo real

## Componentes do Sistema

### 1. Esquemas de Entrada

#### FixedCSVSearchToolSchema
- Parâmetros Obrigatórios:
  - `search_query`: Query de busca
- Parâmetros Opcionais:
  - `max_results`: Limite de resultados
  - `min_relevance`: Relevância mínima
  - `include_headers`: Incluir cabeçalhos
  - `sort_by`: Ordenação
  - `filter_duplicates`: Filtrar duplicados
  - `timeout`: Tempo limite
  - `encoding`: Codificação do arquivo

#### CSVSearchToolSchema
- Parâmetros Obrigatórios:
  - `search_query`: Query de busca
  - `csv`: Caminho do arquivo
- Parâmetros Opcionais:
  - `max_results`: Limite de resultados
  - `min_relevance`: Relevância mínima
  - `include_headers`: Incluir cabeçalhos
  - `sort_by`: Ordenação
  - `filter_duplicates`: Filtrar duplicados
  - `timeout`: Tempo limite
  - `encoding`: Codificação do arquivo
  - `delimiter`: Delimitador
  - `quotechar`: Caractere de citação

### 2. Processamento
- Herança RagTool otimizada
- Processamento tabular avançado
- Análise linha a linha
- Suporte multi-formato
- Cache de resultados
- Validação de dados
- Otimização de recursos
- Compressão de dados
- Logging estruturado
- Indexação eficiente

## Exemplo de Uso

```python
# Inicialização com configuração avançada
ferramenta = CSVSearchTool(
    csv="dados/vendas_2023.csv",
    max_results=100,
    min_relevance=0.7,
    include_headers=True,
    sort_by="relevance",
    filter_duplicates=True,
    timeout=300,
    encoding="utf-8",
    delimiter=",",
    quotechar='"',
    cache_enabled=True,
    validate_data=True
)

# Busca com configuração padrão
resultado = ferramenta.run(
    search_query="total de vendas por região no primeiro trimestre"
)

# Busca avançada com opções completas
resultado = ferramenta.run(
    search_query="análise comparativa de vendas por produto",
    csv="dados/analise_vendas.csv",
    max_results=50,
    min_relevance=0.8,
    include_headers=True,
    sort_by="date",
    filter_duplicates=True,
    encoding="latin-1",
    delimiter=";",
    quotechar="'",
    timeout=60
)
```

## Características Técnicas
- Processamento CSV otimizado
- Suporte multi-delimitador
- Tratamento avançado de headers
- Cache inteligente
- Sistema de indexação
- Compressão de dados
- Logging detalhado
- Retry mechanism
- Monitoramento de performance
- Otimização de recursos
- Validação de conteúdo
- Análise semântica

## Requisitos
- EmbedChain Framework
- Python 3.7+
- Pandas
- NumPy
- Memória suficiente
- Espaço em disco
- CPU adequada
- Dependências base
- Recursos adequados
- SO compatível

## Recursos Especiais
- Busca semântica avançada
- Processamento multi-arquivo
- Análise contextual
- Indexação otimizada
- Cache adaptativo
- Retry automático
- Validação de dados
- Compressão eficiente
- Backup automático
- Monitoramento real-time
- Alertas de falha
- Exportação personalizada
- Filtragem avançada
- Análise estatística

## Limitações e Considerações
- Tamanho do arquivo
- Uso de memória
- Tempo de processamento
- Estrutura dos dados
- Qualidade do CSV
- Timeouts
- Falhas de leitura
- Corrupção de dados
- Limites do sistema
- Performance
- Concorrência
- Validação de conteúdo
- Compatibilidade

## Notas de Implementação
- Validar arquivos
- Configurar processamento
- Implementar timeouts
- Gerenciar recursos
- Otimizar busca
- Implementar cache
- Tratar erros
- Monitorar performance
- Implementar logging
- Backup de dados
- Validar conteúdo
- Gerenciar timeouts
- Implementar retry
- Otimizar recursos
- Comprimir dados
- Monitorar uso
- Validar estrutura
- Documentar operações
- Manter logs
- Testar performance
- Validar integridade
- Implementar alertas
- Documentar mudanças
- Testes automatizados
- Otimização contínua
