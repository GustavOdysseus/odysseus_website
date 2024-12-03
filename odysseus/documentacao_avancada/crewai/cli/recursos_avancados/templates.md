# Templates do CrewAI CLI

## Visão Geral

O sistema de templates do CrewAI CLI fornece estruturas pré-definidas para diferentes tipos de projetos:

- Crew: Template básico para criação de crews individuais
- Flow: Template para flows que conectam múltiplos crews
- Pipeline: Template para pipelines de processamento complexos
- Pipeline Router: Template para roteamento entre diferentes pipelines
- Tool: Template para desenvolvimento de tools personalizadas

## Estrutura de Diretórios

```
templates/
├── __init__.py
├── crew/              # Template básico de crew
├── flow/              # Template de flow
├── pipeline/          # Template de pipeline
├── pipeline_router/   # Template de roteamento
└── tool/             # Template de tool
```

## Templates Disponíveis

### 1. Template de Crew (`crew/`)

```
crew/
├── .gitignore
├── README.md
├── __init__.py
├── config/
│   ├── agents.yaml    # Configuração dos agentes
│   └── tasks.yaml     # Configuração das tasks
├── crew.py           # Definição do crew
├── main.py          # Ponto de entrada
├── pyproject.toml   # Dependências e metadados
└── tools/
    └── custom_tool.py # Tools personalizadas
```

### 2. Template de Flow (`flow/`)

```
flow/
├── .gitignore
├── README.md
├── __init__.py
├── crews/           # Múltiplos crews
│   └── poem_crew/   # Exemplo de crew
├── main.py         # Ponto de entrada com Flow
├── pyproject.toml  # Dependências e metadados
└── tools/          # Tools compartilhadas
```

### 3. Template de Pipeline (`pipeline/`)

```
pipeline/
├── .gitignore
├── README.md
├── __init__.py
├── crews/
│   ├── research_crew/      # Crew de pesquisa
│   ├── write_linkedin_crew/ # Crew de LinkedIn
│   └── write_x_crew/       # Crew de X/Twitter
├── main.py                # Ponto de entrada
├── pipelines/
│   └── pipeline.py        # Definição do pipeline
├── pyproject.toml         # Dependências
└── tools/                 # Tools compartilhadas
```

### 4. Template de Pipeline Router (`pipeline_router/`)

```
pipeline_router/
├── .gitignore
├── README.md
├── __init__.py
├── crews/
│   ├── classifier_crew/   # Crew classificador
│   ├── normal_crew/      # Crew normal
│   └── urgent_crew/      # Crew urgente
├── main.py              # Router principal
├── pipelines/
│   ├── pipeline_classifier.py
│   ├── pipeline_normal.py
│   └── pipeline_urgent.py
├── pyproject.toml
└── tools/
```

### 5. Template de Tool (`tool/`)

```
tool/
├── .gitignore
├── README.md
├── pyproject.toml
└── src/
    └── {{tool_name}}/
        ├── __init__.py
        └── tool.py    # Implementação da tool
```

## Variáveis de Template

Os templates utilizam as seguintes variáveis de substituição:

- `{{crew_name}}`: Nome do crew
- `{{folder_name}}`: Nome do diretório
- `{{class_name}}`: Nome da classe principal
- `{{tool_name}}`: Nome da tool
- `{{pipeline_name}}`: Nome do pipeline
- `{{version}}`: Versão do projeto
- `{{description}}`: Descrição do projeto

## Configuração

### pyproject.toml

```toml
[project]
name = "{{project_name}}"
version = "0.1.0"
description = "{{description}}"

[project.dependencies]
crewai = "^1.0.0"
```

### Configuração de Agentes (agents.yaml)

```yaml
researcher:
  role: "Researcher"
  goal: "Research and analyze information"
  backstory: "Expert researcher with deep analytical skills"
```

### Configuração de Tasks (tasks.yaml)

```yaml
research_task:
  description: "Research and analyze the topic"
  expected_output: "Comprehensive research findings"
```

## Exemplos de Uso

### 1. Criar um Crew

```bash
$ crewai crew create my-research-crew
```

### 2. Criar um Flow

```bash
$ crewai flow create my-analysis-flow
```

### 3. Criar um Pipeline

```bash
$ crewai pipeline create my-processing-pipeline
```

### 4. Criar uma Tool

```bash
$ crewai tool create my-custom-tool
```

## Execução

### Crew Individual

```bash
$ cd my-research-crew
$ crewai run
```

### Pipeline

```bash
$ cd my-processing-pipeline
$ crewai run
```

## Limitações

1. **Estrutura**
   - Estrutura fixa dos templates
   - Nomes de arquivos predefinidos
   - Hierarquia de diretórios estabelecida

2. **Configuração**
   - Formato YAML para configuração
   - Variáveis de template predefinidas
   - Dependências específicas do CrewAI

3. **Execução**
   - Python 3.10-3.13 requerido
   - UV package manager necessário
   - Git para versionamento

## Troubleshooting

### Problemas Comuns

```bash
# Erro: Versão do Python incompatível
Error: Python version must be >=3.10, <=3.13
Solução: Use uma versão compatível do Python

# Erro: Dependências faltando
Error: Missing dependencies
Solução: Execute 'crewai install'
```

### Verificação de Ambiente

```bash
# Verificar versão do Python
$ python --version

# Verificar instalação do UV
$ uv --version
