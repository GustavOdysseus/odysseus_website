# Utilitários do Sistema de Conhecimento do CrewAI

## Visão Geral
O módulo de utilitários (`utils`) do sistema de conhecimento do CrewAI fornece funções auxiliares para manipulação e processamento de conhecimento. Embora compacto, este módulo desempenha um papel crucial na formatação e extração de contexto do conhecimento.

## Funcionalidades

### 1. Extração de Contexto de Conhecimento

```python
def extract_knowledge_context(knowledge_snippets: List[Dict[str, Any]]) -> str:
    """Extract knowledge from the task prompt."""
    valid_snippets = [
        result["context"]
        for result in knowledge_snippets
        if result and result.get("context")
    ]
    snippet = "\n".join(valid_snippets)
    return f"Additional Information: {snippet}" if valid_snippets else ""
```

#### Propósito
A função `extract_knowledge_context` é responsável por:
- Extrair informações contextuais de snippets de conhecimento
- Filtrar snippets válidos
- Formatar o conhecimento para uso em prompts

#### Parâmetros
- `knowledge_snippets`: Lista de dicionários contendo snippets de conhecimento
  - Cada snippet deve ter uma chave "context"
  - Suporta snippets nulos ou inválidos

#### Retorno
- String formatada com o contexto extraído
- Prefixado com "Additional Information: "
- String vazia se nenhum snippet válido for encontrado

#### Comportamento
1. Filtragem
   - Remove snippets nulos
   - Verifica existência da chave "context"
   - Ignora snippets inválidos

2. Processamento
   - Extrai apenas o contexto válido
   - Concatena múltiplos contextos
   - Adiciona prefixo informativo

3. Formatação
   - Usa quebras de linha entre snippets
   - Mantém formatação original do contexto
   - Preserva a ordem dos snippets

## Uso Prático

### 1. Extração Simples
```python
snippets = [
    {"context": "Informação importante 1"},
    {"context": "Informação importante 2"}
]
contexto = extract_knowledge_context(snippets)
# Resultado: "Additional Information: Informação importante 1\nInformação importante 2"
```

### 2. Tratamento de Dados Inválidos
```python
snippets = [
    {"context": "Informação válida"},
    None,
    {"outro_campo": "valor"},
    {"context": "Outra informação"}
]
contexto = extract_knowledge_context(snippets)
# Resultado: "Additional Information: Informação válida\nOutra informação"
```

### 3. Integração com Sistema de Conhecimento
```python
# Recuperando conhecimento do storage
resultados = storage.search(query=["termo de busca"], limit=3)

# Extraindo contexto
contexto = extract_knowledge_context(resultados)

# Usando em prompt
prompt = f"""
Base sua resposta no seguinte contexto:
{contexto}

Pergunta: ...
"""
```

## Integração com Outros Componentes

### 1. Sistema de Storage
```python
class KnowledgeStorage:
    def search(self, query: List[str], limit: int = 3) -> List[Dict[str, Any]]:
        resultados = # ... busca no storage
        return extract_knowledge_context(resultados)
```

### 2. Sistema de Agentes
```python
class Agent:
    def process_knowledge(self, knowledge_results):
        context = extract_knowledge_context(knowledge_results)
        self.update_context(context)
```

## Melhores Práticas

### 1. Validação de Entrada
```python
def process_knowledge(snippets):
    if not snippets:
        return ""
    
    # Validar formato
    if not isinstance(snippets, list):
        raise ValueError("Snippets deve ser uma lista")
        
    # Extrair contexto
    return extract_knowledge_context(snippets)
```

### 2. Tratamento de Erros
```python
def safe_extract_context(snippets):
    try:
        return extract_knowledge_context(snippets)
    except Exception as e:
        logger.error(f"Erro ao extrair contexto: {e}")
        return ""
```

### 3. Formatação Consistente
```python
def format_knowledge(snippets):
    context = extract_knowledge_context(snippets)
    if not context:
        return "Nenhuma informação adicional disponível."
    return context
```

## Extensibilidade

### 1. Formatação Personalizada
```python
def custom_extract_knowledge(snippets, prefix="Contexto:", separator=" | "):
    valid_snippets = [
        result["context"]
        for result in snippets
        if result and result.get("context")
    ]
    snippet = separator.join(valid_snippets)
    return f"{prefix} {snippet}" if valid_snippets else ""
```

### 2. Processamento Avançado
```python
def enhanced_knowledge_context(snippets, metadata=True):
    base_context = extract_knowledge_context(snippets)
    if not metadata:
        return base_context
        
    # Adicionar metadados
    meta_info = [
        f"Fonte: {s.get('source', 'Desconhecida')}"
        for s in snippets
        if s and s.get("context")
    ]
    return f"{base_context}\nMetadados:\n" + "\n".join(meta_info)
```

## Considerações de Performance

### 1. Processamento Eficiente
- List comprehension para filtragem
- Concatenação otimizada de strings
- Validação mínima necessária

### 2. Uso de Memória
- Não mantém dados desnecessários
- Processa snippets sequencialmente
- Limpa referências não utilizadas

### 3. Escalabilidade
- Suporta grandes volumes de snippets
- Processamento linear
- Baixo overhead de memória

## Conclusão
O módulo de utilitários, embora simples em sua implementação, fornece funcionalidades essenciais para o processamento e formatação de conhecimento no CrewAI. Sua integração com outros componentes do sistema permite um fluxo eficiente de informações e contribui para a robustez do sistema como um todo.
