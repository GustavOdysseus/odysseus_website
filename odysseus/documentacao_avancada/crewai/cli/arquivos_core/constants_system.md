# Sistema de Constantes do CrewAI CLI

## Visão Geral

O arquivo `constants.py` define as constantes fundamentais do CrewAI CLI, incluindo configurações de provedores de IA, variáveis de ambiente necessárias e modelos suportados. Este arquivo serve como um ponto central de configuração para toda a integração com diferentes provedores de LLM (Large Language Models).

## Estrutura Principal

### 1. Variáveis de Ambiente (ENV_VARS)

```python
ENV_VARS = {
    "openai": [...],
    "anthropic": [...],
    "gemini": [...],
    "groq": [...],
    "watson": [...],
    "ollama": [...],
    "bedrock": [...],
    "azure": [...],
    "cerebras": [...]
}
```

#### Provedores Suportados

1. **OpenAI**
   - Chave API: `OPENAI_API_KEY`
   - Prompt personalizado para entrada

2. **Anthropic**
   - Chave API: `ANTHROPIC_API_KEY`
   - Integração com Claude

3. **Google (Gemini)**
   - Chave API: `GEMINI_API_KEY`
   - Acesso aos modelos Gemini

4. **Groq**
   - Chave API: `GROQ_API_KEY`
   - Processamento de alta performance

5. **IBM Watson**
   - URL: `WATSONX_URL`
   - Chave API: `WATSONX_APIKEY`
   - ID do Projeto: `WATSONX_PROJECT_ID`

6. **Ollama**
   - Configuração padrão: `http://localhost:11434`
   - Execução local de modelos

7. **AWS Bedrock**
   - Access Key ID: `AWS_ACCESS_KEY_ID`
   - Secret Access Key: `AWS_SECRET_ACCESS_KEY`
   - Region: `AWS_REGION_NAME`

8. **Azure OpenAI**
   - Nome do deployment
   - Chave API: `AZURE_API_KEY`
   - URL Base: `AZURE_API_BASE`
   - Versão API: `AZURE_API_VERSION`

9. **Cerebras**
   - Nome do modelo
   - Chave API: `CEREBRAS_API_KEY`

### 2. Lista de Provedores

```python
PROVIDERS = [
    "openai",
    "anthropic",
    "gemini",
    "groq",
    "ollama",
    "watson",
    "bedrock",
    "azure",
    "cerebras"
]
```

### 3. Modelos Suportados

```python
MODELS = {
    "openai": [
        "gpt-4",
        "gpt-4o",
        "gpt-4o-mini",
        "o1-mini",
        "o1-preview"
    ],
    "anthropic": [
        "claude-3-5-sonnet-20240620",
        "claude-3-sonnet-20240229",
        "claude-3-opus-20240229",
        "claude-3-haiku-20240307"
    ],
    # ... outros provedores
}
```

## Detalhamento dos Modelos

### 1. OpenAI
- GPT-4 e variantes
- Modelos otimizados (o1)
- Diferentes capacidades e tamanhos

### 2. Anthropic
- Claude 3 e variantes
- Diferentes níveis de capacidade
- Modelos especializados

### 3. Gemini
- Modelos 1.5 Flash e Pro
- Gemma 2 em diferentes tamanhos
- Capacidades específicas

### 4. Groq
- LLaMA 3.1 em diferentes tamanhos
- Modelos Gemma otimizados
- Foco em performance

### 5. Watson
- Integração com Meta LLaMA
- Modelos Mistral
- Modelos IBM Granite

### 6. Bedrock
- Ampla variedade de modelos
- Integrações com múltiplos provedores
- Diferentes capacidades e tamanhos

## Uso do Sistema

### 1. Configuração de Provedores
```python
from crewai.cli.constants import ENV_VARS

# Configurar OpenAI
openai_config = ENV_VARS["openai"]
api_key_prompt = openai_config[0]["prompt"]
api_key_name = openai_config[0]["key_name"]
```

### 2. Seleção de Modelos
```python
from crewai.cli.constants import MODELS

# Listar modelos OpenAI disponíveis
openai_models = MODELS["openai"]
```

### 3. Validação de Provedores
```python
from crewai.cli.constants import PROVIDERS

def is_valid_provider(provider):
    return provider in PROVIDERS
```

## Integração com o Sistema

### 1. CLI
- Configuração de provedores
- Validação de entradas
- Gerenciamento de credenciais

### 2. Runtime
- Seleção de modelos
- Configuração de ambiente
- Validação de configurações

### 3. API
- Integração com provedores
- Gerenciamento de modelos
- Configuração de endpoints

## Manutenção e Atualização

### 1. Adição de Novos Provedores
1. Adicionar ao `ENV_VARS`
2. Incluir na lista `PROVIDERS`
3. Definir modelos em `MODELS`

### 2. Atualização de Modelos
1. Atualizar lista de modelos
2. Manter compatibilidade
3. Documentar mudanças

### 3. Gestão de Versões
1. Controle de compatibilidade
2. Migração de configurações
3. Documentação de mudanças

## Considerações Técnicas

### 1. Segurança
- Gerenciamento de credenciais
- Validação de entradas
- Proteção de dados sensíveis

### 2. Performance
- Configurações otimizadas
- Carregamento eficiente
- Uso de recursos

### 3. Manutenibilidade
- Estrutura organizada
- Documentação clara
- Facilidade de atualização

## Conclusão

O sistema de constantes do CrewAI CLI é:
- **Abrangente**: Suporte a múltiplos provedores
- **Flexível**: Fácil adição de novos provedores
- **Organizado**: Estrutura clara e documentada
- **Mantível**: Fácil atualização e extensão

Este sistema forma a base para:
1. Integração com provedores de IA
2. Configuração do ambiente
3. Validação de configurações
4. Experiência consistente do usuário
