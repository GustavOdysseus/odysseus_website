# Ferramenta de Busca em Diretório - Documentação

## Descrição
A Ferramenta de Busca em Diretório é uma solução avançada para realizar buscas semânticas em conteúdo de diretórios. Baseada na RagTool, oferece capacidades sofisticadas de busca através de arquivos usando processamento de linguagem natural, com suporte completo para travessia recursiva e indexação otimizada.

## Principais Recursos

### Busca em Diretório
- Busca semântica avançada
- Travessia recursiva otimizada
- Análise inteligente de conteúdo
- Indexação em tempo real
- Integração EmbedChain
- Processamento de linguagem natural
- Cache adaptativo
- Retry automático
- Validação de conteúdo
- Monitoramento em tempo real

### Modos de Operação
1. **Modo de Diretório Fixo**
   - Diretório pré-configurado
   - Contexto persistente
   - Interface otimizada
   - Cache inteligente
   - Validação contínua
   - Monitoramento de mudanças
   - Backup automático
   - Performance otimizada

2. **Modo de Diretório Dinâmico**
   - Diretório flexível
   - Seleção adaptativa
   - Contexto dinâmico
   - Validação automática
   - Detecção de alterações
   - Cache dinâmico
   - Retry inteligente
   - Monitoramento contínuo

## Componentes do Sistema

### 1. Esquemas de Entrada

#### FixedDirectorySearchToolSchema
- Parâmetros Obrigatórios:
  - `search_query`: Query de busca
- Parâmetros Opcionais:
  - `max_results`: Limite de resultados
  - `min_relevance`: Relevância mínima
  - `file_types`: Tipos de arquivo
  - `exclude_dirs`: Diretórios excluídos
  - `include_hidden`: Incluir ocultos
  - `depth_limit`: Limite de profundidade
  - `timeout`: Tempo limite

#### DirectorySearchToolSchema
- Parâmetros Obrigatórios:
  - `search_query`: Query de busca
  - `directory`: Caminho do diretório
- Parâmetros Opcionais:
  - `max_results`: Limite de resultados
  - `min_relevance`: Relevância mínima
  - `file_types`: Tipos de arquivo
  - `exclude_dirs`: Diretórios excluídos
  - `include_hidden`: Incluir ocultos
  - `depth_limit`: Limite de profundidade
  - `timeout`: Tempo limite

### 2. Processamento
- Carregamento otimizado
- Análise semântica avançada
- Processamento de queries
- Ranking inteligente
- Indexação em tempo real
- Cache de resultados
- Validação de dados
- Otimização de recursos
- Compressão de dados
- Logging estruturado

## Exemplo de Uso

```python
# Inicialização com configuração avançada
ferramenta = DirectorySearchTool(
    directory="/caminho/para/diretorio",
    max_results=100,
    min_relevance=0.7,
    file_types=[".txt", ".md", ".py"],
    exclude_dirs=["node_modules", ".git"],
    include_hidden=False,
    depth_limit=5,
    timeout=300
)

# Busca com configuração padrão
resultado = ferramenta.run(
    search_query="documentação sobre APIs REST"
)

# Busca com configuração dinâmica
resultado = ferramenta.run(
    search_query="implementação de autenticação",
    directory="/outro/diretorio",
    max_results=50,
    min_relevance=0.8,
    file_types=[".py", ".js"],
    depth_limit=3
)
```

## Características Técnicas
- Integração DirectoryLoader avançada
- Travessia recursiva otimizada
- Embeddings sofisticados
- Análise semântica profunda
- Processamento de queries NLP
- Sistema de cache
- Compressão de dados
- Logging detalhado
- Retry mechanism
- Monitoramento de performance
- Otimização de recursos
- Validação de conteúdo

## Requisitos
- EmbedChain Framework
- Python 3.7+
- Acesso ao filesystem
- Memória suficiente
- Espaço em disco
- Permissões adequadas
- Dependências base
- Recursos adequados
- SO compatível
- CPU multicore

## Recursos Especiais
- Compreensão semântica avançada
- Busca recursiva otimizada
- Ranking contextual
- Queries em linguagem natural
- Gerenciamento de contexto
- Cache adaptativo
- Retry automático
- Validação de conteúdo
- Compressão de dados
- Backup automático
- Monitoramento real-time
- Alertas de falha
- Exportação personalizada
- Filtragem avançada

## Limitações e Considerações
- Consumo de memória
- Tempo de indexação
- Compatibilidade de formatos
- Precisão das buscas
- Requisitos de sistema
- Timeouts
- Falhas de busca
- Corrupção de índice
- Limites do sistema
- Performance
- Concorrência
- Validação de conteúdo
- Compatibilidade

## Notas de Implementação
- Validar ambiente
- Configurar indexação
- Implementar timeouts
- Gerenciar recursos
- Otimizar busca
- Implementar cache
- Tratar erros
- Monitorar performance
- Implementar logging
- Backup de índices
- Validar conteúdo
- Gerenciar timeouts
- Implementar retry
- Otimizar recursos
- Comprimir dados
- Monitorar uso
- Validar resultados
- Documentar operações
- Manter logs
- Testar performance
- Validar integridade
- Implementar alertas
- Documentar mudanças
- Testes automatizados
- Otimização contínua
