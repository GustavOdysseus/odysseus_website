# Ferramenta de Rastreamento de Website Firecrawl - Documentação

## Descrição
A Ferramenta de Rastreamento de Website Firecrawl é uma poderosa ferramenta de rastreamento web que utiliza a biblioteca Firecrawl para rastrear e extrair conteúdo de websites. Ela fornece opções flexíveis de configuração tanto para o comportamento de rastreamento quanto para o processamento de páginas.

## Principais Recursos

### Rastreamento Web
- Extração de conteúdo de website
- Opções configuráveis de rastreamento
- Opções de processamento de página
- Integração com API
- Tratamento de erros

### Opções de Configuração
1. **Opções do Rastreador**
   - Comportamento personalizado de rastreamento
   - Configurações de travessia
   - Limitação de taxa
   - Controle de profundidade

2. **Opções de Página**
   - Configurações de extração de conteúdo
   - Seleção de elementos
   - Processamento de dados
   - Formatação de saída

## Componentes do Sistema

### 1. Esquema de Entrada

#### FirecrawlCrawlWebsiteToolSchema
- Parâmetros:
  - `url`: URL do website alvo (obrigatório)
  - `crawler_options`: Configuração de rastreamento (opcional)
  - `page_options`: Configurações de processamento de página (opcional)

### 2. Processamento
- Validação de URL
- Inicialização da API
- Configuração do rastreador
- Processamento de página
- Extração de conteúdo
- Tratamento de erros

## Exemplo de Uso

```python
# Inicializar com chave de API
ferramenta = FirecrawlCrawlWebsiteTool(api_key="sua-chave-api")

# Rastreamento básico
resultado = ferramenta.run(url="https://exemplo.com")

# Rastreamento avançado com opções
resultado = ferramenta.run(
    url="https://exemplo.com",
    crawler_options={
        "maxDepth": 2,
        "maxPages": 10
    },
    page_options={
        "waitForSelector": ".content",
        "removeSelectors": [".ads", ".nav"]
    }
)
```

## Características Técnicas
- Integração com Firecrawl
- Autenticação de API
- Manipulação de requisições
- Processamento de respostas
- Gerenciamento de erros
- Flexibilidade de configuração

## Requisitos
- Chave de API Firecrawl
- Pacote firecrawl-py
- Conectividade com internet
- URLs válidas
- Permissões apropriadas

## Recursos Especiais
- Rastreamento configurável
- Processamento personalizado de página
- Operação baseada em API
- Opções flexíveis
- Relatório de erros

## Limitações e Considerações
- Limites de taxa da API
- Restrições de website
- Políticas de robôs
- Dependências de rede
- Uso de recursos

## Notas
- Verificar chave de API
- Respeitar robots.txt
- Monitorar limites de taxa
- Considerar políticas do site
- Gerenciar recursos
- Validar saída
- Tratar erros de rede
- Documentar configurações
- Manter logs de rastreamento
