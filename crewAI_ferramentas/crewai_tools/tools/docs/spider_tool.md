# Ferramenta Spider - Documentação

## Descrição
A Ferramenta Spider é uma ferramenta especializada para web scraping e crawling que converte conteúdo web em dados prontos para LLM. Oferece dois modos principais de operação: extração de página única e crawling completo de website, com extensas opções de configuração.

## Funcionalidades Principais

### Modos de Operação
1. **Modo Scrape**
   - Extração de página única
   - Processamento de conteúdo
   - Conversão para Markdown
   - Extração seletiva
   - Manipulação de metadados

2. **Modo Crawl**
   - Crawling completo do site
   - Controle de profundidade
   - Seguimento de links
   - Agregação de conteúdo
   - Saída estruturada

## Componentes do Sistema

### 1. Schema de Entrada

#### SpiderToolSchema
- Parâmetros:
  - `url`: URL do website alvo (obrigatório)
  - `mode`: Modo de operação ("scrape" ou "crawl")
  - `params`: Opções de configuração
    - `limit`: Máximo de páginas para crawling
    - `depth`: Profundidade máxima de crawling
    - `metadata`: Flag para incluir metadados
    - `query_selector`: Seletor CSS para conteúdo

### 2. Processamento
- Validação de URL
- Seleção de modo
- Manipulação de parâmetros
- Extração de conteúdo
- Conversão de formato

## Exemplo de Uso

```python
# Inicializar ferramenta
ferramenta = SpiderTool(api_key="sua-chave-api")

# Extração de página única
resultado = ferramenta.run(
    url="https://exemplo.com",
    mode="scrape",
    params={
        "metadata": True,
        "query_selector": "article"
    }
)

# Crawling completo do site
resultado = ferramenta.run(
    url="https://exemplo.com",
    mode="crawl",
    params={
        "limit": 10,
        "depth": 2,
        "metadata": True
    }
)
```

## Características Técnicas
- Integração com cliente Spider
- Conversão para Markdown
- Seleção por CSS
- Controle de profundidade
- Manipulação de metadados
- Processamento assíncrono
- Cache inteligente
- Otimização de recursos

## Requisitos
- Biblioteca cliente Spider
- Chave de API
- Conectividade com internet
- URLs válidas
- Recursos do sistema
- Python 3.7+
- Memória adequada
- Espaço em disco

## Recursos Especiais
- Modos duplos de operação
- Controle de profundidade
- Extração de metadados
- Direcionamento por CSS
- Conversão de formato
- Cache de resultados
- Filtragem de conteúdo
- Exportação personalizada
- Processamento paralelo
- Validação automática

## Limitações e Considerações
- Limites de taxa da API
- Restrições de websites
- Uso de recursos
- Dependências de rede
- Tamanho do conteúdo
- Tempo de processamento
- Políticas de robots.txt
- Limites de memória
- Latência de rede
- Custos de API

## Notas de Implementação
- Verificar chave de API
- Monitorar uso de recursos
- Implementar timeouts
- Gerenciar memória cache
- Respeitar limites de taxa
- Testar seletores CSS
- Tratar erros graciosamente
- Monitorar performance
- Implementar cache eficiente
- Considerar segurança
- Testar conectividade
- Lidar com sites grandes
- Validar entrada de dados
- Processar conteúdo
- Respeitar robots.txt
- Implementar retry
- Otimizar consultas
- Documentar resultados
- Manter logs detalhados
- Backup de dados importantes
