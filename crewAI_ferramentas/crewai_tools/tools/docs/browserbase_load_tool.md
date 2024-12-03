# Ferramenta BrowserbaseLoad - Documentação

## Descrição
A Ferramenta BrowserbaseLoad é uma ferramenta especializada para carregar páginas web usando um navegador headless através do serviço Browserbase. Ela fornece capacidades para buscar conteúdo web com recursos avançados de automação de navegador.

## Principais Recursos

### Carregamento de Páginas Web
- Automação de navegador headless
- Suporte para extração de conteúdo textual
- Gerenciamento de sessão
- Suporte a proxy
- Integração com API Browserbase

### Opções de Configuração
1. **Autenticação da API**
   - Configuração de chave API
   - Gerenciamento de ID do projeto
   - Manipulação de sessão

2. **Opções de Carregamento**
   - Extração de conteúdo textual
   - Suporte a proxy
   - Persistência de sessão
   - Validação de URL

## Componentes do Sistema

### 1. Esquema de Entrada

#### BrowserbaseLoadToolSchema
- Parâmetros:
  - `url`: URL do site para carregar (obrigatório)

### 2. Configuração da Ferramenta
- Configuração da chave API
- Configuração do ID do projeto
- Ativação de extração de conteúdo textual
- Gerenciamento de ID de sessão
- Configuração de proxy

## Exemplo de Uso

```python
# Inicializar com credenciais API
ferramenta = BrowserbaseLoadTool(
    api_key="sua_chave_api",
    project_id="seu_id_projeto",
    text_content=True,
    proxy=True
)

# Carregar uma página web
resultado = ferramenta.run(url="https://exemplo.com")

# Carregar com persistência de sessão
ferramenta = BrowserbaseLoadTool(
    api_key="sua_chave_api",
    project_id="seu_id_projeto",
    session_id="id_sessao_unico"
)
resultado = ferramenta.run(url="https://exemplo.com")
```

## Características Técnicas
- Automação de navegador headless
- Gerenciamento de sessão
- Suporte a proxy
- Extração de conteúdo textual
- Validação de URL

## Requisitos
- Pacote Python Browserbase
- Credenciais API válidas
- Conexão com internet
- Python 3.x

## Recursos Especiais
- Automação de navegador headless
- Persistência de sessão
- Suporte a proxy
- Extração de conteúdo textual
- Validação e processamento de URL

## Limitações e Considerações
- Requer chave API do Browserbase
- Dependente de conectividade com internet
- Limites de taxa podem se aplicar
- Tempo de processamento varia por página
- Disponibilidade de proxy varia

## Notas
- Importante manejar credenciais API com segurança
- Considerar limitação de taxa
- Monitorar custos de uso
- Testar configurações de proxy
- Validar URLs antes do processamento
- Gerenciar sessões cuidadosamente
