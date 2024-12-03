# Documentação das Utilidades do Flow CrewAI

## Visão Geral

O módulo `utils.py` fornece um conjunto de funções utilitárias essenciais para o funcionamento do sistema Flow do CrewAI. Estas funções são responsáveis por análise de código, gerenciamento de dependências e estruturação do fluxo de execução.

## Funções Principais

### 1. Análise de Retorno (get_possible_return_constants)

```python
def get_possible_return_constants(function):
    """
    Analisa o código fonte de uma função para identificar valores constantes retornados.
    
    Args:
        function: A função a ser analisada
        
    Returns:
        List[Any]: Lista de valores constantes que podem ser retornados pela função
    """
```

#### Características
- Usa AST (Abstract Syntax Tree) para análise de código
- Identifica valores constantes em declarações return
- Trata erros de indentação e sintaxe
- Suporta Python 3.8+

#### Exemplo de Uso
```python
def my_function():
    if condition:
        return "success"
    return "failure"

constants = get_possible_return_constants(my_function)
# Result: ["success", "failure"]
```

### 2. Cálculo de Níveis (calculate_node_levels)

```python
def calculate_node_levels(flow):
    """
    Calcula os níveis hierárquicos dos nós no fluxo.
    
    Args:
        flow: Instância do fluxo
        
    Returns:
        Dict[str, int]: Mapeamento de nomes de métodos para seus níveis
    """
```

#### Características
- Implementa travessia em largura (BFS)
- Suporta condições OR e AND
- Gerencia roteadores e caminhos
- Mantém consistência de níveis

#### Exemplo de Uso
```python
class MyFlow(Flow):
    @start
    def begin(self):
        pass
        
    @listen("begin")
    def process(self):
        pass

levels = calculate_node_levels(flow_instance)
# Result: {"begin": 0, "process": 1}
```

### 3. Contagem de Arestas (count_outgoing_edges)

```python
def count_outgoing_edges(flow):
    """
    Conta o número de arestas de saída para cada nó no fluxo.
    
    Args:
        flow: Instância do fluxo
        
    Returns:
        Dict[str, int]: Mapeamento de nomes de métodos para contagem de arestas
    """
```

#### Características
- Conta conexões diretas
- Inclui listeners e triggers
- Suporta múltiplos tipos de conexão

### 4. Gerenciamento de Ancestrais (build_ancestor_dict)

```python
def build_ancestor_dict(flow):
    """
    Constrói um dicionário de ancestrais para cada nó no fluxo.
    
    Args:
        flow: Instância do fluxo
        
    Returns:
        Dict[str, Set[str]]: Mapeamento de nós para seus ancestrais
    """
```

#### Características
- Usa DFS para construção
- Mantém conjuntos de ancestrais
- Suporta roteadores
- Evita ciclos

### 5. Verificação de Ancestralidade (is_ancestor)

```python
def is_ancestor(node, ancestor_candidate, ancestors):
    """
    Verifica se um nó é ancestral de outro.
    
    Args:
        node: Nó a ser verificado
        ancestor_candidate: Possível ancestral
        ancestors: Dicionário de ancestrais
        
    Returns:
        bool: True se ancestor_candidate é ancestral de node
    """
```

### 6. Estrutura Pai-Filho (build_parent_children_dict)

```python
def build_parent_children_dict(flow):
    """
    Constrói um dicionário de relações pai-filho no fluxo.
    
    Args:
        flow: Instância do fluxo
        
    Returns:
        Dict[str, List[str]]: Mapeamento de pais para seus filhos
    """
```

#### Características
- Mapeia listeners para triggers
- Gerencia roteadores e caminhos
- Mantém ordem consistente
- Suporta múltiplos filhos

## Casos de Uso Avançados

### 1. Análise de Dependências

```python
class DependencyAnalysis:
    def __init__(self, flow):
        self.levels = calculate_node_levels(flow)
        self.ancestors = build_ancestor_dict(flow)
        self.parent_children = build_parent_children_dict(flow)
        
    def analyze_dependencies(self, node):
        return {
            'level': self.levels.get(node),
            'ancestors': self.ancestors.get(node),
            'children': self.parent_children.get(node)
        }
```

### 2. Validação de Fluxo

```python
def validate_flow(flow):
    levels = calculate_node_levels(flow)
    ancestors = build_ancestor_dict(flow)
    
    # Verifica ciclos
    for node in flow._methods:
        if is_ancestor(node, node, ancestors):
            raise ValueError(f"Ciclo detectado em {node}")
            
    # Verifica níveis consistentes
    for node, level in levels.items():
        for child in build_parent_children_dict(flow).get(node, []):
            if levels[child] <= level:
                raise ValueError(f"Nível inconsistente entre {node} e {child}")
```

## Melhores Práticas

### 1. Análise de Código
- Use `get_possible_return_constants` para análise estática
- Trate erros de parsing adequadamente
- Considere limitações de versão do Python

### 2. Estrutura do Fluxo
- Mantenha hierarquia clara com `calculate_node_levels`
- Evite ciclos usando `is_ancestor`
- Valide dependências com `build_ancestor_dict`

### 3. Performance
- Cache resultados de análises custosas
- Use estruturas de dados eficientes
- Evite recálculos desnecessários

## Extensibilidade

### 1. Análise Customizada
```python
def custom_analysis(flow):
    levels = calculate_node_levels(flow)
    edges = count_outgoing_edges(flow)
    return {
        'complexity': len(levels),
        'connectivity': sum(edges.values()) / len(edges)
    }
```

### 2. Validações Adicionais
```python
def validate_custom_rules(flow):
    parent_children = build_parent_children_dict(flow)
    for parent, children in parent_children.items():
        if len(children) > 5:  # Limite máximo de filhos
            raise ValueError(f"Nó {parent} tem muitos filhos")
```

## Conclusão

O módulo `utils.py` é fundamental para o funcionamento do sistema Flow do CrewAI, fornecendo ferramentas essenciais para análise, estruturação e validação de fluxos. Suas funções são projetadas para serem eficientes, flexíveis e extensíveis, permitindo a construção de fluxos complexos e robustos.
