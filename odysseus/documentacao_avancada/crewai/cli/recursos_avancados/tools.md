# Gerenciamento de Tools no CrewAI

## Visão Geral

O módulo Tools do CrewAI fornece funcionalidades para criar, publicar e instalar tools personalizadas através da linha de comando (CLI).

## Comandos CLI

### Criação de Tools

```bash
# Criar uma nova tool
$ crewai tool create my-awesome-tool

# Exemplo de output:
Creating custom tool my_awesome_tool...
✓ Tool structure created
✓ Git repository initialized
Created custom tool my_awesome_tool. Run cd my_awesome_tool to start working.
```

### Publicação de Tools

```bash
# Publicar uma tool (pública)
$ crewai tool publish --public

# Publicar uma tool (privada)
$ crewai tool publish --private

# Forçar publicação mesmo com mudanças não sincronizadas
$ crewai tool publish --public --force

# Exemplo de output:
Successfully published my-awesome-tool (1.0.0)
Install it in other projects with crewai tool install my-awesome-tool
```

### Instalação de Tools

```bash
# Instalar uma tool
$ crewai tool install my-awesome-tool

# Exemplo de output:
Successfully installed my-awesome-tool
```

### Autenticação

```bash
# Login no repositório de tools
$ crewai tool login

# Exemplo de output:
Successfully authenticated to the tool repository.
```

## Estrutura de Projeto

Ao criar uma nova tool, a seguinte estrutura é gerada:

```
my_awesome_tool/
├── pyproject.toml
├── README.md
├── src/
│   └── my_awesome_tool/
│       ├── __init__.py
│       └── main.py
└── tests/
    └── __init__.py
```

## Exemplos de Uso

### 1. Criar e Publicar uma Tool

```bash
# Criar nova tool
$ crewai tool create calculator-tool
$ cd calculator_tool

# Desenvolver a tool...

# Publicar
$ crewai tool publish --public
```

### 2. Instalar e Usar uma Tool

```bash
# Instalar tool existente
$ crewai tool install calculator-tool

# A tool estará disponível para uso em seus projetos
```

### 3. Atualizar uma Tool

```bash
# Atualizar código
# Atualizar versão em pyproject.toml
$ crewai tool publish --public
```

## Mensagens de Erro Comuns

```bash
# Erro: Dentro de um projeto existente
Error: Oops! It looks like you're inside a project.
Solução: Mude para um diretório vazio

# Erro: Repositório não sincronizado
Error: Failed to publish tool.
Local changes need to be resolved before publishing.
Solução: Commit, push e pull mudanças

# Erro: Falha na autenticação
Error: Authentication failed.
Solução: Verifique credenciais com crewai login
```

## Configuração

### 1. Arquivo pyproject.toml

```toml
[project]
name = "my-awesome-tool"
version = "1.0.0"
description = "Uma tool incrível"

[project.dependencies]
python = "^3.6"
```

### 2. Variáveis de Ambiente

```bash
# Credenciais do repositório
UV_INDEX_REPO_USERNAME=seu-usuario
UV_INDEX_REPO_PASSWORD=sua-senha
```

## Boas Práticas

### 1. Desenvolvimento
```bash
# Sempre teste localmente antes de publicar
$ python -m pytest tests/
```

### 2. Versionamento
```bash
# Use versionamento semântico
# Atualize version em pyproject.toml
```

### 3. Documentação
```bash
# Mantenha README.md atualizado
# Documente APIs e funcionalidades
```

## Limitações

1. **Publicação**
   - Requer Git instalado
   - Requer autenticação
   - Requer repositório sincronizado

2. **Instalação**
   - Requer permissões adequadas
   - Dependências compatíveis
   - Conexão com repositório

3. **Desenvolvimento**
   - Python 3.6+
   - UV package manager
   - Git

## Troubleshooting

### 1. Problemas de Publicação

```bash
# Verificar estado do Git
$ git status

# Verificar credenciais
$ crewai tool login

# Forçar publicação
$ crewai tool publish --force
```

### 2. Problemas de Instalação

```bash
# Verificar autenticação
$ crewai tool login

# Limpar cache
$ rm -rf ~/.crewai/cache

# Reinstalar
$ crewai tool install my-tool
```

### 3. Logs e Debug

```bash
# Ver logs detalhados
$ crewai tool install my-tool --verbose

# Debug de autenticação
$ crewai tool login --debug
```
