# Ferramenta Serper.dev - Documentação

## Descrição
A Ferramenta Serper.dev é uma interface que permite realizar buscas na internet utilizando a API Serper.dev, fornecendo resultados do Google de forma estruturada e programática. Esta ferramenta é ideal para automação de buscas e coleta de dados web.

## Funcionalidades Principais

### Busca na Internet
- Acesso programático aos resultados do Google
- Personalização de parâmetros de busca
- Formatação estruturada dos resultados
- Opção de salvamento dos resultados em arquivo
- Cache inteligente de resultados
- Filtragem avançada
- Exportação personalizada

### Parâmetros de Configuração
- `search_url`: URL base da API (padrão: "https://google.serper.dev/search")
- `country`: Código do país para resultados localizados
- `location`: Localização específica para resultados
- `locale`: Configuração de idioma
- `n_results`: Número de resultados (padrão: 10)
- `save_file`: Flag para salvar resultados em arquivo
- `timeout`: Tempo limite para requisições
- `retry_attempts`: Número de tentativas em caso de falha

## Componentes do Sistema

### 1. Schema de Entrada (SerperDevToolSchema)
- Parâmetros Obrigatórios:
  - `search_query`: String de busca
- Parâmetros Opcionais:
  - `filter_type`: Tipo de filtro para resultados
  - `date_range`: Intervalo de datas
  - `domain_filter`: Filtro por domínio
  - `language`: Idioma preferencial

### 2. Formatação dos Resultados
Para cada resultado, inclui:
- Título formatado
- URL completa
- Snippet otimizado
- Metadados relevantes
- Data de indexação
- Ranking de relevância
- Informações estruturadas
- Tags de categorização

## Exemplo de Uso

```python
# Inicialização básica
ferramenta = SerperDevTool()

# Busca simples
resultado = ferramenta.run(search_query="inteligência artificial")

# Busca avançada
resultado = ferramenta.run(
    search_query="restaurantes",
    country="BR",
    location="São Paulo",
    n_results=5,
    save_file=True,
    filter_type="recent",
    date_range="last_week",
    domain_filter=["*.com.br"],
    language="pt-BR"
)
```

## Requisitos
- Chave de API do Serper.dev (`SERPER_API_KEY`)
- Variável de ambiente configurada
- Conexão com internet estável
- Biblioteca requests instalada
- Python 3.7+
- Memória suficiente
- Espaço em disco
- SSL atualizado

## Recursos Especiais
- Suporte a buscas internacionais
- Personalização de localização
- Salvamento automático de resultados
- Formatação estruturada
- Cache inteligente
- Retry automático
- Logging detalhado
- Exportação flexível
- Filtragem avançada
- Análise de relevância

## Sistema de Cache
- Cache local de resultados
- Tempo de expiração configurável
- Atualização automática
- Otimização de requisições
- Economia de recursos

## Parâmetros de Localização
1. **País (gl)**
   - Código do país
   - Exemplos: "BR", "US", "UK"
   - Afeta ranking de resultados
   - Personalização regional

2. **Localização**
   - Cidade ou região
   - Resultados locais
   - Geolocalização
   - Preferências regionais

3. **Idioma (hl)**
   - Configuração de idioma
   - Interface localizada
   - Resultados traduzidos
   - Contexto linguístico

## Limitações e Considerações
- Limites de taxa da API
- Cotas de uso
- Latência de rede
- Custos de API
- Cache necessário
- Timeout padrão
- Validação de dados
- Tratamento de erros

## Notas de Implementação
- Verificar chave API
- Monitorar uso
- Implementar retry
- Gerenciar cache
- Validar entrada
- Tratar erros
- Otimizar requisições
- Documentar uso
- Manter logs
- Backup de dados
- Atualizar índices
- Monitorar performance
- Implementar timeouts
- Validar resultados
- Gerenciar memória
- Otimizar recursos
- Manter segurança
- Documentar mudanças
- Testar integração
- Validar saída
