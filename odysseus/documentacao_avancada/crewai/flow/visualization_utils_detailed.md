# Utilitários de Visualização do Flow CrewAI

## Visão Geral

O módulo `visualization_utils.py` fornece um conjunto de ferramentas para criar visualizações interativas e informativas dos fluxos do CrewAI. Ele utiliza análise de código e manipulação de grafos para gerar representações visuais claras e úteis.

## Componentes Principais

### 1. Análise de Chamadas (method_calls_crew)

```python
def method_calls_crew(method):
    """
    Verifica se um método faz chamadas ao .crew().
    
    Args:
        method: Método a ser analisado
        
    Returns:
        bool: True se o método chama .crew()
    """
```

#### Características
- Usa AST para análise de código
- Detecta chamadas de método específicas
- Trata erros de parsing graciosamente
- Suporta diferentes estilos de código

### 2. Adição de Nós (add_nodes_to_network)

```python
def add_nodes_to_network(net, flow, node_positions, node_styles):
    """
    Adiciona nós ao grafo de visualização.
    
    Args:
        net: Objeto de rede para visualização
        flow: Instância do fluxo
        node_positions: Posições dos nós
        node_styles: Estilos visuais dos nós
    """
```

#### Tipos de Nós
1. Start Nodes
   - Representam pontos de início
   - Estilo visual distinto
   - Posicionamento prioritário

2. Router Nodes
   - Representam pontos de decisão
   - Estilo visual específico
   - Conexões especiais

3. Crew Nodes
   - Representam operações com agentes
   - Estilo visual destacado
   - Identificação automática

4. Method Nodes
   - Representam métodos regulares
   - Estilo visual padrão
   - Formatação automática de labels

### 3. Cálculo de Posições (compute_positions)

```python
def compute_positions(flow, node_levels, y_spacing=150, x_spacing=150):
    """
    Calcula posições ótimas para os nós no grafo.
    
    Args:
        flow: Instância do fluxo
        node_levels: Níveis hierárquicos dos nós
        y_spacing: Espaçamento vertical
        x_spacing: Espaçamento horizontal
        
    Returns:
        Dict[str, Tuple[float, float]]: Posições dos nós
    """
```

#### Características
- Centralização automática
- Distribuição hierárquica
- Espaçamento configurável
- Prevenção de sobreposição

### 4. Adição de Arestas (add_edges)

```python
def add_edges(net, flow, node_positions, colors):
    """
    Adiciona arestas ao grafo de visualização.
    
    Args:
        net: Objeto de rede
        flow: Instância do fluxo
        node_positions: Posições dos nós
        colors: Esquema de cores
    """
```

#### Tipos de Arestas
1. Regular Edges
   - Conexões diretas
   - Estilo visual simples
   - Direção clara

2. Router Edges
   - Conexões de roteamento
   - Estilo tracejado
   - Cores distintas

3. AND Condition Edges
   - Conexões de condição AND
   - Estilo especial
   - Identificação visual

#### Características Avançadas
- Curvatura automática
- Prevenção de sobreposição
- Indicadores de direção
- Estilos condicionais

## Recursos de Estilização

### 1. Esquema de Cores
```python
colors = {
    "edge": "#2B7CE9",
    "router_edge": "#FF9800",
    "start_node": "#4CAF50",
    "router_node": "#FF5722",
    "crew_node": "#9C27B0",
    "method_node": "#2196F3"
}
```

### 2. Estilos de Nós
```python
node_styles = {
    "start": {
        "color": "#4CAF50",
        "borderWidth": 2,
        "borderColor": "#388E3C"
    },
    "router": {
        "color": "#FF5722",
        "borderWidth": 2,
        "borderColor": "#D84315"
    },
    "crew": {
        "color": "#9C27B0",
        "borderWidth": 2,
        "borderColor": "#7B1FA2"
    },
    "method": {
        "color": "#2196F3",
        "borderWidth": 2,
        "borderColor": "#1976D2"
    }
}
```

## Casos de Uso

### 1. Visualização Básica
```python
def visualize_simple_flow(flow):
    net = Network()
    node_levels = calculate_node_levels(flow)
    positions = compute_positions(flow, node_levels)
    add_nodes_to_network(net, flow, positions, node_styles)
    add_edges(net, flow, positions, colors)
    return net
```

### 2. Visualização Customizada
```python
def visualize_custom_flow(flow, custom_styles):
    net = Network()
    node_levels = calculate_node_levels(flow)
    positions = compute_positions(
        flow, 
        node_levels, 
        y_spacing=200,  # Mais espaço vertical
        x_spacing=300   # Mais espaço horizontal
    )
    add_nodes_to_network(net, flow, positions, custom_styles)
    add_edges(net, flow, positions, custom_colors)
    return net
```

## Melhores Práticas

### 1. Layout
- Use espaçamento adequado
- Mantenha hierarquia clara
- Evite cruzamentos de arestas

### 2. Estilização
- Mantenha consistência visual
- Use cores com bom contraste
- Forneça indicadores visuais claros

### 3. Performance
- Otimize para grandes fluxos
- Cache posições calculadas
- Minimize recálculos

## Extensibilidade

### 1. Estilos Customizados
```python
custom_styles = {
    "start": {
        "color": "#YOUR_COLOR",
        "shape": "circle",
        "size": 30
    }
}
```

### 2. Layouts Alternativos
```python
def custom_layout_algorithm(flow, node_levels):
    # Implementação personalizada
    positions = {}
    return positions
```

## Conclusão

O sistema de visualização do CrewAI Flow é uma ferramenta poderosa para entender e documentar fluxos complexos. Suas capacidades de personalização e otimização automática o tornam adequado para uma ampla gama de casos de uso, desde desenvolvimento até documentação e debugging.
