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

O CrewAI Plus API fornece uma interface de linha de comando para interagir com os serviços avançados do CrewAI, incluindo gerenciamento de tools, crews e deployments.

## Comandos Principais

### 1. Gerenciamento de Tools

#### Login no Repositório de Tools
```bash
crewai plus tools login

# Exemplo de output:
Successfully logged in to the tool repository
API Key: ********-****-****-****-************
```

#### Publicar uma Tool
```bash
crewai plus tools publish my-tool --version 1.0.0 --public

# Opções:
#   --version    Versão da tool
#   --public     Se a tool deve ser pública
#   --description    Descrição da tool
```

#### Obter Informações de uma Tool
```bash
crewai plus tools get my-tool

# Exemplo de output:
Tool: my-tool
Version: 1.0.0
Public: Yes
Description: Uma tool incrível
```

### 2. Gerenciamento de Crews

#### Listar Crews
```bash
crewai plus crews list

# Exemplo de output:
Available Crews:
1. my-project (uuid: abc123)
2. another-project (uuid: def456)
```

#### Deploy de um Crew
```bash
# Por nome do projeto
crewai plus crews deploy --name my-project

# Por UUID
crewai plus crews deploy --uuid abc123
```

#### Status do Crew
```bash
# Verificar status por nome
crewai plus crews status --name my-project

# Verificar status por UUID
crewai plus crews status --uuid abc123

# Exemplo de output:
Status: Running
Uptime: 2h 30m
Last Update: 2024-01-20 14:30:00
```

#### Logs do Crew
```bash
# Ver logs por nome
crewai plus crews logs --name my-project

# Ver logs por UUID
crewai plus crews logs --uuid abc123

# Opções de tipo de log:
#   --type deployment    Logs de deployment (padrão)
#   --type execution     Logs de execução
```

#### Criar um Novo Crew
```bash
crewai plus crews create --name my-new-project --config config.yaml

# Opções:
#   --name      Nome do projeto
#   --config    Arquivo de configuração
```

#### Deletar um Crew
```bash
# Deletar por nome
crewai plus crews delete --name my-project

# Deletar por UUID
crewai plus crews delete --uuid abc123
```

## Configuração

### 1. Variáveis de Ambiente
```bash
# Configurar API Key
export CREWAI_API_KEY=sua-api-key

# Configurar URL Base (opcional)
export CREWAI_BASE_URL=https://custom.crewai.com
```

### 2. Arquivo de Configuração
```yaml
# ~/.crewai/config.yaml
api_key: sua-api-key
base_url: https://app.crewai.com
```

## Troubleshooting

### 1. Erros Comuns

#### Autenticação Falhou
```bash
Error: Authentication failed
Solução: Verifique sua API key e ambiente
```

#### Deploy Falhou
```bash
Error: Deployment failed
Solução: Verifique logs e configuração
```

### 2. Soluções
- Verificar API key
- Confirmar conectividade
- Validar configuração
- Checar logs detalhados

## Melhores Práticas

### 1. Segurança
- Nunca compartilhe sua API key
- Use variáveis de ambiente
- Mantenha logs seguros

### 2. Operação
- Monitore deployments
- Verifique status regularmente
- Mantenha logs organizados

### 3. Manutenção
- Atualize tools regularmente
- Faça backup de configurações
- Monitore uso de recursos

## Notas Adicionais

### 1. Dependências
- Python 3.6+
- Requests
- Click
- URLLib

### 2. Recursos
- Documentação oficial
- Fórum da comunidade
- Suporte técnico

### 3. Limitações
- Rate limits
- Quotas de uso
- Restrições de recursos
