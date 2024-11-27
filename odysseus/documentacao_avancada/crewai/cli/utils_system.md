# Sistema de Utilitários do CrewAI CLI

## Visão Geral

O módulo `utils.py` fornece um conjunto abrangente de funções utilitárias que dão suporte às operações do CrewAI CLI. Estas funções lidam com tarefas como manipulação de arquivos, gerenciamento de configurações, manipulação de ambiente e operações de projeto.

## Grupos de Funcionalidades

### 1. Manipulação de Templates

```python
def copy_template(src, dst, name, class_name, folder_name):
```

**Propósito:**
- Copia e personaliza templates
- Substitui placeholders
- Cria novos arquivos de projeto

**Operações:**
1. Leitura do template fonte
2. Substituição de variáveis
   - `{{name}}` → nome do projeto
   - `{{crew_name}}` → nome da classe
   - `{{folder_name}}` → nome do diretório
3. Escrita do arquivo personalizado

### 2. Gerenciamento TOML

```python
def read_toml(file_path: str = "pyproject.toml")
def parse_toml(content)
def simple_toml_parser(content)
```

**Funcionalidades:**
1. **Leitura de TOML**
   - Suporte a Python 3.11+
   - Parser simplificado para versões anteriores
   - Manipulação de configurações

2. **Atributos de Projeto**
   ```python
   def get_project_name()
   def get_project_version()
   def get_project_description()
   ```

### 3. Gerenciamento de Ambiente

```python
def fetch_and_json_env_file(env_file_path: str = ".env")
def load_env_vars(folder_path)
def update_env_vars(env_vars, provider, model)
def write_env_file(folder_path, env_vars)
```

**Capacidades:**
1. **Leitura de Variáveis**
   - Carregamento de arquivo .env
   - Parsing de configurações
   - Validação de formato

2. **Atualização de Ambiente**
   - Integração com provedores
   - Configuração de modelos
   - Persistência de mudanças

### 4. Operações de Sistema de Arquivos

```python
def tree_copy(source, destination)
def tree_find_and_replace(directory, find, replace)
```

**Funcionalidades:**
1. **Cópia de Diretórios**
   - Cópia recursiva
   - Preservação de estrutura
   - Manipulação de arquivos

2. **Substituição em Massa**
   - Busca recursiva
   - Substituição em conteúdo
   - Renomeação de arquivos

### 5. Autenticação e Versão

```python
def get_auth_token()
def get_crewai_version()
```

**Recursos:**
1. **Gerenciamento de Token**
   - Acesso seguro
   - Validação de credenciais
   - Integração com TokenManager

2. **Controle de Versão**
   - Versão do CrewAI
   - Compatibilidade
   - Metadados do pacote

## Uso Prático

### 1. Criação de Projeto

```python
# Copiando template
copy_template(
    "template/crew.py",
    "project/my_crew.py",
    "MyCrew",
    "MyCrewClass",
    "my_project"
)

# Configurando ambiente
env_vars = load_env_vars(project_path)
update_env_vars(env_vars, "openai", "gpt-4")
write_env_file(project_path, env_vars)
```

### 2. Leitura de Configurações

```python
# Lendo configurações do projeto
project_name = get_project_name()
project_version = get_project_version()
project_description = get_project_description()

# Lendo variáveis de ambiente
env_vars = fetch_and_json_env_file()
```

### 3. Operações em Diretórios

```python
# Copiando estrutura de diretórios
tree_copy("template_dir", "new_project")

# Substituindo strings em arquivos
tree_find_and_replace("project_dir", "old_name", "new_name")
```

## Integração com o Sistema

### 1. CLI Principal
- Suporte a comandos
- Manipulação de argumentos
- Feedback ao usuário

### 2. Sistema de Templates
- Geração de código
- Personalização de projetos
- Estruturação de diretórios

### 3. Configuração de Ambiente
- Variáveis de ambiente
- Credenciais de API
- Configurações de projeto

## Considerações Técnicas

### 1. Compatibilidade
- Suporte multi-versão Python
- Adaptação de funcionalidades
- Tratamento de diferenças

### 2. Segurança
- Manipulação segura de tokens
- Proteção de credenciais
- Validação de entrada

### 3. Performance
- Operações otimizadas
- Manipulação eficiente de arquivos
- Caching quando apropriado

## Tratamento de Erros

### 1. Arquivos
```python
try:
    with open(file_path, "r") as f:
        # Operações de arquivo
except FileNotFoundError:
    # Tratamento específico
except Exception as e:
    # Tratamento genérico
```

### 2. Configurações
- Validação de formato TOML
- Verificação de atributos
- Mensagens de erro claras

### 3. Ambiente
- Validação de variáveis
- Verificação de permissões
- Recuperação de falhas

## Manutenção e Extensão

### 1. Adição de Funcionalidades
1. Identificar necessidade
2. Implementar função
3. Documentar uso
4. Testar integração

### 2. Atualização de Recursos
1. Manter compatibilidade
2. Atualizar documentação
3. Validar mudanças

### 3. Depuração
1. Logs detalhados
2. Mensagens claras
3. Rastreamento de erros

## Conclusão

O sistema de utilitários do CrewAI CLI é:
- **Versátil**: Ampla gama de funcionalidades
- **Robusto**: Tratamento completo de erros
- **Extensível**: Fácil adição de recursos
- **Integrado**: Parte central do CLI

Este sistema forma a base para:
1. Operações do CLI
2. Gerenciamento de projetos
3. Configuração de ambiente
4. Experiência do desenvolvedor
