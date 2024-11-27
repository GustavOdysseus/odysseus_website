# Templates do CrewAI CLI

## Visão Geral

O sistema de templates do CrewAI CLI fornece estruturas pré-definidas para diferentes tipos de projetos, facilitando a criação de crews, flows, pipelines e tools.

## Tipos de Templates

### 1. Template de Crew

Estrutura básica para criação de crews:

```
crew/
├── .gitignore
├── README.md
├── __init__.py
├── config/
│   └── ...
├── crew.py
├── main.py
├── pyproject.toml
└── tools/
    └── ...
```

#### Uso via CLI
```bash
# Criar novo crew
$ crewai crew create my-crew

# Exemplo de output:
Creating new crew my-crew...
✓ Template structure created
✓ Configuration initialized
Created new crew my-crew. Run cd my-crew to start working.
```

### 2. Template de Tool

Estrutura para desenvolvimento de tools personalizadas:

```
tool/
├── .gitignore
├── README.md
├── pyproject.toml
└── src/
    └── {{tool_name}}/
        ├── __init__.py
        └── main.py
```

#### Uso via CLI
```bash
# Criar nova tool
$ crewai tool create my-tool

# Exemplo de output:
Creating custom tool my-tool...
✓ Tool structure created
✓ Git repository initialized
Created custom tool my-tool. Run cd my-tool to start working.
```

### 3. Template de Flow

Estrutura para criação de flows:

```
flow/
├── .gitignore
├── README.md
├── __init__.py
├── crews/
│   └── ...
├── main.py
├── pyproject.toml
└── tools/
    └── ...
```

#### Uso via CLI
```bash
# Criar novo flow
$ crewai flow create my-flow

# Exemplo de output:
Creating new flow my-flow...
✓ Flow structure created
✓ Dependencies configured
Created new flow my-flow. Run cd my-flow to start working.
```

### 4. Template de Pipeline

Estrutura para pipelines complexos:

```
pipeline/
├── .gitignore
├── README.md
├── __init__.py
├── config/
│   └── settings.py
├── flows/
│   └── ...
├── main.py
├── pyproject.toml
└── utils/
    └── ...
```

#### Uso via CLI
```bash
# Criar novo pipeline
$ crewai pipeline create my-pipeline

# Exemplo de output:
Creating new pipeline my-pipeline...
✓ Pipeline structure created
✓ Configuration initialized
Created new pipeline my-pipeline. Run cd my-pipeline to start working.
```

## Configuração dos Templates

### 1. pyproject.toml

```toml
# Exemplo para crew
[project]
name = "my-crew"
version = "0.1.0"
description = "Um crew incrível"

[project.dependencies]
crewai = "^1.0.0"
```

### 2. README.md

Cada template inclui um README.md com:
- Descrição do projeto
- Instruções de instalação
- Guia de uso
- Exemplos práticos

### 3. Arquivos de Configuração

```python
# config/settings.py
CREW_NAME = "{{crew_name}}"
VERSION = "{{version}}"
DESCRIPTION = "{{description}}"
```

## Personalização de Templates

### 1. Variáveis de Template

```bash
# Variáveis disponíveis
{{project_name}}    # Nome do projeto
{{version}}        # Versão do projeto
{{description}}    # Descrição do projeto
{{author}}         # Autor do projeto
```

### 2. Hooks de Personalização

```bash
# Pre-create hook
$ crewai template hook pre-create my-hook.sh

# Post-create hook
$ crewai template hook post-create my-hook.sh
```

## Exemplos de Uso

### 1. Criar Crew com Configuração Personalizada

```bash
# Criar crew com configuração
$ crewai crew create my-crew --config custom_config.yaml
```

### 2. Criar Tool com Template Personalizado

```bash
# Usar template personalizado
$ crewai tool create my-tool --template custom_template
```

### 3. Criar Flow com Dependencies

```bash
# Criar flow com dependências específicas
$ crewai flow create my-flow --deps "numpy,pandas"
```

## Boas Práticas

### 1. Estrutura de Projeto
```bash
# Manter estrutura organizada
$ tree my-project
```

### 2. Versionamento
```bash
# Usar .gitignore apropriado
$ cat .gitignore
__pycache__/
*.pyc
.env
```

### 3. Documentação
```bash
# Manter README.md atualizado
$ cat README.md
```

## Troubleshooting

### 1. Problemas Comuns

```bash
# Erro: Template não encontrado
Error: Template 'custom' not found
Solução: Verifique o nome do template

# Erro: Variáveis não definidas
Error: Required variable 'version' not set
Solução: Defina todas as variáveis necessárias
```

### 2. Validação de Template

```bash
# Verificar template
$ crewai template validate my-template

# Exemplo de output:
✓ Structure valid
✓ Variables defined
✓ Dependencies resolved
```

### 3. Debug

```bash
# Modo verbose
$ crewai crew create my-crew --verbose

# Modo debug
$ crewai tool create my-tool --debug
```

## Limitações

1. **Personalização**
   - Templates fixos
   - Variáveis predefinidas
   - Hooks limitados

2. **Compatibilidade**
   - Python 3.6+
   - CrewAI 1.0+
   - Git necessário

3. **Recursos**
   - Sem hot reload
   - Sem templates dinâmicos
   - Sem versionamento de templates
