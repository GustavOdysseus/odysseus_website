# Ferramenta de Raspagem de Website Firecrawl - Documentação

## Descrição
A Ferramenta de Raspagem de Website Firecrawl é uma ferramenta especializada de raspagem web que utiliza a biblioteca Firecrawl para extrair conteúdo de páginas web. Ela oferece extensas opções de configuração para raspagem de página, extração de dados e gerenciamento de timeout.

## Principais Recursos

### Raspagem Web
- Extração de conteúdo de página única
- Opções configuráveis de página
- Configurações de extração de dados
- Gerenciamento de timeout
- Integração com API

### Opções de Configuração
1. **Opções de Página**
   - Configurações de carregamento de página
   - Seleção de elementos
   - Condições de espera
   - Opções de navegação

2. **Opções de Extrator**
   - Regras de extração de dados
   - Filtragem de conteúdo
   - Formatação de saída
   - Direcionamento de elementos

## Componentes do Sistema

### 1. Esquema de Entrada

#### FirecrawlScrapeWebsiteToolSchema
- Parâmetros:
  - `url`: URL do website alvo (obrigatório)
  - `page_options`: Configuração de raspagem de página (opcional)
  - `extractor_options`: Configurações de extração de dados (opcional)
  - `timeout`: Timeout da operação em milissegundos (opcional, padrão: 30000)

### 2. Processamento
- Validação de URL
- Inicialização da API
- Configuração de página
- Extração de dados
- Tratamento de timeout
- Formatação de resposta

## Exemplo de Uso

```python
# Inicializar com chave de API
ferramenta = FirecrawlScrapeWebsiteTool(api_key="sua-chave-api")

# Raspagem básica
resultado = ferramenta.run(url="https://exemplo.com")

# Raspagem avançada com opções
resultado = ferramenta.run(
    url="https://exemplo.com",
    page_options={
        "waitForSelector": ".content",
        "removeSelectors": [".ads"]
    },
    extractor_options={
        "includeSelectors": [".main-content"],
        "excludeSelectors": [".sidebar"]
    },
    timeout=45000
)
```

## Características Técnicas
- Integração com Firecrawl
- Autenticação de API
- Manipulação de requisições
- Processamento de respostas
- Gerenciamento de timeout
- Tratamento de erros

## Requisitos
- Chave de API Firecrawl
- Pacote firecrawl-py
- Conectividade com internet
- URLs válidas
- Permissões apropriadas

## Recursos Especiais
- Raspagem configurável
- Regras personalizadas de extração
- Controle de timeout
- Direcionamento de elementos
- Relatório de erros

## Limitações e Considerações
- Limites de taxa da API
- Restrições de website
- Políticas de robôs
- Dependências de rede
- Uso de recursos
- Restrições de timeout

## Notas
- Verificar chave de API
- Respeitar robots.txt
- Monitorar limites de taxa
- Ajustar timeouts conforme necessário
- Validar seletores
- Tratar erros de rede
- Testar configurações
- Documentar extrações
- Manter logs de raspagem
