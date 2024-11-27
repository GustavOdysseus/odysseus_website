# API Plus do CrewAI

## Visão Geral

O módulo `plus_api.py` implementa a interface de comunicação com a API CrewAI+, fornecendo métodos para gerenciamento de tools, crews e deployments na plataforma CrewAI+.

## Funcionalidade Principal

```python
class PlusAPI:
    """
    This class exposes methods for working with the CrewAI+ API.
    """
    TOOLS_RESOURCE = "/crewai_plus/api/v1/tools"
    CREWS_RESOURCE = "/crewai_plus/api/v1/crews"
```

## Componentes do Sistema

### 1. Inicialização
```python
def __init__(self, api_key: str) -> None:
    self.api_key = api_key
    self.headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": f"CrewAI-CLI/{get_crewai_version()}",
        "X-Crewai-Version": get_crewai_version(),
    }
```
- Autenticação via API Key
- Headers padronizados
- Versionamento automático

### 2. Requisições HTTP
```python
def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
    url = urljoin(self.base_url, endpoint)
    session = requests.Session()
    session.trust_env = False
    return session.request(method, url, headers=self.headers, **kwargs)
```
- Sessão dedicada
- Trust env desabilitado
- Headers consistentes

### 3. Gerenciamento de Tools
```python
def publish_tool(self, handle: str, is_public: bool, version: str, description: Optional[str], encoded_file: str):
```
- Publicação de tools
- Controle de visibilidade
- Versionamento

## Endpoints Principais

### 1. Tools
- **Login**
  ```python
  def login_to_tool_repository(self)
  ```
  - Autenticação no repositório
  - Acesso a tools privadas

- **Publicação**
  ```python
  def publish_tool(self, handle, is_public, version, description, encoded_file)
  ```
  - Upload de tools
  - Metadata configurável
  - Controle de acesso

### 2. Crews
- **Deploy**
  ```python
  def deploy_by_name(self, project_name: str)
  def deploy_by_uuid(self, uuid: str)
  ```
  - Deploy por nome
  - Deploy por UUID
  - Resposta assíncrona

- **Status**
  ```python
  def crew_status_by_name(self, project_name: str)
  def crew_status_by_uuid(self, uuid: str)
  ```
  - Monitoramento
  - Estado atual
  - Detalhes de execução

- **Logs**
  ```python
  def crew_by_name(self, project_name: str, log_type: str = "deployment")
  def crew_by_uuid(self, uuid: str, log_type: str = "deployment")
  ```
  - Logs de deployment
  - Tipos customizáveis
  - Histórico completo

### 3. Gerenciamento
- **Listagem**
  ```python
  def list_crews(self)
  ```
  - Crews disponíveis
  - Metadata completa
  - Estado atual

- **Criação**
  ```python
  def create_crew(self, payload)
  ```
  - Nova crew
  - Configuração flexível
  - Validação automática

- **Deleção**
  ```python
  def delete_crew_by_name(self, project_name: str)
  def delete_crew_by_uuid(self, uuid: str)
  ```
  - Remoção por nome
  - Remoção por UUID
  - Limpeza completa

## Fluxos de Trabalho

### 1. Publicação de Tool
1. Login no repositório
2. Preparação do arquivo
3. Publicação com metadata
4. Validação de status

### 2. Deploy de Crew
1. Criação da crew
2. Configuração de parâmetros
3. Deploy do ambiente
4. Monitoramento de status

### 3. Gerenciamento de Logs
1. Identificação da crew
2. Seleção do tipo de log
3. Recuperação de histórico
4. Análise de execução

## Integração com Sistema

### 1. Autenticação
- Token Bearer
- Versão do CLI
- Headers customizados

### 2. Sessões HTTP
- Sessões dedicadas
- Configuração segura
- Trust env controlado

### 3. Endpoints
- Versionados
- RESTful
- Documentados

## Melhores Práticas

### 1. Autenticação
- **API Key**
  - Armazenamento seguro
  - Rotação regular
  - Escopo limitado

- **Sessões**
  - Dedicadas
  - Configuradas
  - Limpas

### 2. Requisições
- **Headers**
  - Padronizados
  - Versionados
  - Completos

- **Respostas**
  - Validadas
  - Tipadas
  - Tratadas

## Considerações Técnicas

### 1. Performance
- **Sessões**
  - Reuso
  - Pooling
  - Timeout

### 2. Segurança
- **Autenticação**
  - Bearer token
  - HTTPS
  - Validação

### 3. Manutenibilidade
- **Código**
  - Modular
  - Documentado
  - Testável

## Exemplos de Uso

### 1. Publicação de Tool
```python
api = PlusAPI(api_key)
response = api.publish_tool(
    handle="my-tool",
    is_public=True,
    version="1.0.0",
    description="My awesome tool",
    encoded_file=encoded_content
)
```

### 2. Deploy de Crew
```python
api = PlusAPI(api_key)
response = api.deploy_by_name("my-crew")
status = api.crew_status_by_name("my-crew")
```

### 3. Monitoramento
```python
api = PlusAPI(api_key)
logs = api.crew_by_name("my-crew", log_type="deployment")
```

## Troubleshooting

### 1. Erros Comuns
- **Autenticação**
  ```
  Error: Invalid API key
  Solução: Verificar API key
  ```

- **Deploy**
  ```
  Error: Crew not found
  Solução: Verificar nome/UUID
  ```

### 2. Soluções
- Validar credenciais
- Verificar payload
- Checar logs

### 3. Prevenção
- Validação prévia
- Monitoramento
- Logs detalhados

## Conclusão

A API Plus do CrewAI é:
- **Robusta**: Endpoints completos
- **Segura**: Autenticação forte
- **Flexível**: Operações diversas
- **Confiável**: Tratamento de erros

Este sistema é essencial para:
1. Gerenciamento de tools
2. Deploy de crews
3. Monitoramento de execução
4. Controle de ambiente

## Notas Adicionais

### 1. Dependências
- Requests
- URLLib
- Environment

### 2. Configuração
- API Key
- Base URL
- Versão CLI

### 3. Extensibilidade
- Novos endpoints
- Tipos de log
- Payloads customizados

# CrewAI Plus API

## Visão Geral

O CrewAI Plus API fornece acesso aos serviços avançados do CrewAI através da linha de comando (CLI).

## Comandos CLI

### Configuração Inicial

```bash
# Configurar a API key
$ export CREWAI_API_KEY="sua-api-key"

# Configurar URL base (opcional)
$ export CREWAI_BASE_URL="https://custom.crewai.com"
```

### Comandos de Tools

```bash
# Fazer login no repositório de tools
$ crewai tool login

# Publicar uma tool
$ crewai tool publish --name my-tool --version 1.0.0 --description "Minha tool incrível"

# Obter informações de uma tool
$ crewai tool get my-tool
```

### Comandos de Crews

```bash
# Listar todos os crews
$ crewai crew list

# Criar um novo crew
$ crewai crew create --name my-project --file crew_config.yaml

# Deploy de um crew
$ crewai crew deploy --name my-project
$ crewai crew deploy --uuid abc-123-def-456

# Verificar status de um crew
$ crewai crew status --name my-project
$ crewai crew status --uuid abc-123-def-456

# Ver logs de um crew
$ crewai crew logs --name my-project --type deployment
$ crewai crew logs --uuid abc-123-def-456 --type execution

# Deletar um crew
$ crewai crew delete --name my-project
$ crewai crew delete --uuid abc-123-def-456
```

## Opções Comuns

```bash
# Opções globais disponíveis para todos os comandos
--help          # Mostra ajuda sobre o comando
--verbose       # Aumenta o nível de detalhes do output
--quiet         # Reduz o nível de detalhes do output
--format json   # Output em formato JSON
```

## Exemplos de Uso

### 1. Workflow Básico de Tools

```bash
# Login e publicação de uma tool
$ export CREWAI_API_KEY="minha-api-key"
$ crewai tool login
$ crewai tool publish --name calculator --version 1.0.0 --description "Calculadora avançada"
```

### 2. Workflow Básico de Crews

```bash
# Criar e fazer deploy de um crew
$ crewai crew create --name math-crew --file math_crew.yaml
$ crewai crew deploy --name math-crew
$ crewai crew status --name math-crew
$ crewai crew logs --name math-crew --type deployment
```

## Mensagens de Erro Comuns

```bash
# Erro de autenticação
Error: Authentication failed. Please check your API key.

# Erro de deploy
Error: Deployment failed. See logs for details.
$ crewai crew logs --name my-project --type deployment

# Erro de configuração
Error: Invalid configuration file. Please check your YAML syntax.
```

## Arquivos de Configuração

### crew_config.yaml
```yaml
name: my-project
version: 1.0.0
description: "Descrição do projeto"
tools:
  - calculator
  - converter
```

## Boas Práticas

1. **Segurança**
   ```bash
   # Use variáveis de ambiente para a API key
   $ export CREWAI_API_KEY="sua-api-key"
   
   # Nunca inclua a API key em scripts ou repositórios
   ```

2. **Monitoramento**
   ```bash
   # Verifique status regularmente
   $ crewai crew status --name my-project
   
   # Monitore logs para problemas
   $ crewai crew logs --name my-project --type execution
   ```

3. **Manutenção**
   ```bash
   # Atualize tools regularmente
   $ crewai tool publish --name my-tool --version 1.0.1
   
   # Mantenha backups de configurações
   $ cp crew_config.yaml crew_config.backup.yaml
   ```

## Limitações

1. **Rate Limits**
   - Máximo de 100 requisições por minuto
   - Máximo de 1000 requisições por hora

2. **Tamanho de Arquivos**
   - Tools: máximo 10MB
   - Logs: máximo 100MB

3. **Tempo de Execução**
   - Deploy: máximo 5 minutos
   - Execução: máximo 1 hora
