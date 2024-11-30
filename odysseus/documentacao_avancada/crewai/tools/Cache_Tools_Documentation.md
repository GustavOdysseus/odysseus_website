# Cache Tools - Documentação Detalhada

## Visão Geral
O módulo `cache_tools` implementa um sistema de cache para o CrewAI, permitindo o armazenamento e recuperação eficiente de resultados de execuções anteriores de ferramentas. Este sistema é fundamental para otimizar o desempenho e reduzir chamadas redundantes.

## Estrutura do Diretório
```
cache_tools/
├── __init__.py
└── cache_tools.py
```

## Componentes Principais

### 1. Classe CacheTools

```python
class CacheTools(BaseModel):
    name: str = "Hit Cache"
    cache_handler: CacheHandler = Field(
        description="Cache Handler for the crew",
        default_factory=CacheHandler,
    )
```

#### Atributos
1. **name** (str)
   - Nome padrão da ferramenta: "Hit Cache"
   - Identificador para uso no sistema

2. **cache_handler** (CacheHandler)
   - Gerenciador de cache
   - Instanciado automaticamente via Pydantic
   - Responsável por operações de cache

### 2. Métodos

#### 2.1 tool()
```python
def tool(self):
    return StructuredTool.from_function(
        func=self.hit_cache,
        name=self.name,
        description="Reads directly from the cache",
    )
```

**Funcionalidade:**
- Cria uma ferramenta estruturada LangChain
- Encapsula a função hit_cache
- Fornece interface padronizada

#### 2.2 hit_cache(key)
```python
def hit_cache(self, key):
    split = key.split("tool:")
    tool = split[1].split("|input:")[0].strip()
    tool_input = split[1].split("|input:")[1].strip()
    return self.cache_handler.read(tool, tool_input)
```

**Funcionalidade:**
- Processa a chave de cache
- Extrai informações da ferramenta
- Recupera dados do cache

## Formato da Chave de Cache
A chave de cache segue o formato:
```
tool:[nome_ferramenta]|input:[entrada_ferramenta]
```

### Exemplo:
```python
key = "tool:data_processor|input:file1.csv"
# Resulta em:
# tool = "data_processor"
# tool_input = "file1.csv"
```

## Integração com LangChain

### 1. StructuredTool
- Utiliza o framework LangChain
- Permite integração com agentes
- Fornece interface estruturada

### 2. Funcionalidades
- Leitura direta do cache
- Integração com outros componentes
- Suporte a ferramentas estruturadas

## Casos de Uso

### 1. Recuperação de Resultados Cached
```python
cache_tools = CacheTools()
tool = cache_tools.tool()
result = tool.run("tool:processor|input:data.csv")
```

### 2. Integração com Agentes
```python
from langchain.agents import Agent

agent = Agent(tools=[cache_tools.tool()])
```

## Melhores Práticas

### 1. Uso do Cache
- Verifique o cache antes de executar operações caras
- Mantenha chaves consistentes
- Limpe o cache periodicamente

### 2. Formatação de Chaves
- Siga o formato padrão
- Use nomes descritivos
- Mantenha consistência

### 3. Gerenciamento de Memória
- Monitore o uso de memória
- Implemente política de expiração
- Gerencie tamanho do cache

## Considerações Técnicas

### 1. Performance
- Cache em memória
- Acesso rápido
- Baixa latência

### 2. Extensibilidade
- Fácil adição de novos handlers
- Suporte a diferentes backends
- Interface consistente

### 3. Integração
- Compatível com LangChain
- Suporte a agentes
- API estruturada

## Exemplos de Implementação

### 1. Uso Básico
```python
from crewai.tools.cache_tools import CacheTools

# Criar instância
cache_tools = CacheTools()

# Criar ferramenta
tool = cache_tools.tool()

# Usar cache
result = tool.run("tool:my_tool|input:my_input")
```

### 2. Integração com Sistema
```python
class MySystem:
    def __init__(self):
        self.cache_tools = CacheTools()
        
    def process_with_cache(self, tool_name, input_data):
        cache_key = f"tool:{tool_name}|input:{input_data}"
        return self.cache_tools.hit_cache(cache_key)
```

## Conclusão
O sistema de cache do CrewAI fornece uma solução eficiente para armazenamento e recuperação de resultados de ferramentas. Sua integração com LangChain e design modular o torna uma parte fundamental da infraestrutura de otimização do framework.
