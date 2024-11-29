# Visualizador de Flow CrewAI

## Visão Geral

O módulo `flow_visualizer.py` é o componente central de visualização do Flow CrewAI. Ele utiliza a biblioteca pyvis para criar visualizações de rede interativas e profissionais dos fluxos do CrewAI.

## Classe Principal: FlowPlot

```python
class FlowPlot:
    def __init__(self, flow):
        """
        Inicializa o visualizador de flow.
        
        Args:
            flow: Instância do flow a ser visualizado
        """
        self.flow = flow
        self.colors = COLORS
        self.node_styles = NODE_STYLES
```

### Métodos Principais

#### 1. Plotagem Principal
```python
def plot(self, filename):
    """
    Gera e salva a visualização do flow.
    
    Args:
        filename: Nome do arquivo de saída (sem extensão)
    """
```

#### Características da Rede
- Direcionada (directed=True)
- Altura fixa (750px)
- Largura responsiva (100%)
- Cor de fundo configurável
- Layout customizado
- Física desabilitada para melhor controle

#### 2. Geração HTML
```python
def _generate_final_html(self, network_html):
    """
    Gera o HTML final com todos os componentes.
    
    Args:
        network_html: HTML gerado pela rede
        
    Returns:
        str: HTML final completo
    """
```

#### 3. Limpeza
```python
def _cleanup_pyvis_lib(self):
    """
    Limpa arquivos temporários gerados pela pyvis.
    """
```

## Configuração da Rede

### 1. Opções Básicas
```python
net = Network(
    directed=True,
    height="750px",
    width="100%",
    bgcolor=colors["bg"],
    layout=None
)
```

### 2. Opções Avançadas
```javascript
var options = {
    "nodes": {
        "font": {
            "multi": "html"
        }
    },
    "physics": {
        "enabled": false
    }
}
```

## Pipeline de Visualização

### 1. Cálculo de Níveis
```python
node_levels = calculate_node_levels(flow)
```
- Determina a hierarquia dos nós
- Organiza nós em camadas
- Otimiza layout vertical

### 2. Cálculo de Posições
```python
node_positions = compute_positions(flow, node_levels)
```
- Posicionamento automático
- Distribuição otimizada
- Prevenção de sobreposição

### 3. Adição de Nós
```python
add_nodes_to_network(net, flow, node_positions, node_styles)
```
- Criação de nós
- Aplicação de estilos
- Posicionamento preciso

### 4. Adição de Arestas
```python
add_edges(net, flow, node_positions, colors)
```
- Conexões entre nós
- Estilos de linha
- Direcionamento

## Integração de Componentes

### 1. Template Handler
```python
html_handler = HTMLTemplateHandler(template_path, logo_path)
network_body = html_handler.extract_body_content(network_html)
```

### 2. Geração de Legendas
```python
legend_items = get_legend_items(colors)
legend_items_html = generate_legend_items_html(legend_items)
```

### 3. HTML Final
```python
final_html_content = html_handler.generate_final_html(
    network_body, 
    legend_items_html
)
```

## Função de Conveniência

```python
def plot_flow(flow, filename="flow_plot"):
    """
    Função de alto nível para plotar flows.
    
    Args:
        flow: Flow a ser visualizado
        filename: Nome do arquivo de saída
    """
    visualizer = FlowPlot(flow)
    visualizer.plot(filename)
```

## Configurações Padrão

### 1. Cores (COLORS)
```python
COLORS = {
    "bg": "#FFFFFF",
    "edge": "#2B7CE9",
    "router_edge": "#FF9800",
    "start": "#4CAF50",
    "router": "#FF5722",
    "method": "#2196F3"
}
```

### 2. Estilos de Nós (NODE_STYLES)
```python
NODE_STYLES = {
    "start": {
        "color": COLORS["start"],
        "borderWidth": 2,
        "borderColor": "#388E3C"
    },
    "router": {
        "color": COLORS["router"],
        "borderWidth": 2,
        "borderColor": "#D84315"
    },
    "method": {
        "color": COLORS["method"],
        "borderWidth": 2,
        "borderColor": "#1976D2"
    }
}
```

## Casos de Uso

### 1. Visualização Básica
```python
from crewai.flow import Flow, plot_flow

flow = Flow()
# Configuração do flow...
plot_flow(flow)
```

### 2. Visualização Customizada
```python
visualizer = FlowPlot(flow)
visualizer.colors = custom_colors
visualizer.node_styles = custom_styles
visualizer.plot("custom_flow")
```

## Melhores Práticas

### 1. Performance
- Desative física para flows grandes
- Otimize posicionamento de nós
- Limpe recursos temporários

### 2. Visual
- Use cores contrastantes
- Mantenha hierarquia clara
- Evite sobreposições

### 3. Interatividade
- Mantenha navegação suave
- Forneça informações claras
- Permita zoom e pan

## Extensibilidade

### 1. Estilos Customizados
```python
custom_colors = {
    "bg": "#YOUR_COLOR",
    "edge": "#YOUR_COLOR",
    # ...
}

custom_styles = {
    "start": {
        "color": "#YOUR_COLOR",
        "shape": "circle"
    },
    # ...
}
```

### 2. Layout Customizado
```python
def custom_layout_algorithm(flow, node_levels):
    positions = {}
    # Implementação personalizada...
    return positions
```

## Conclusão

O FlowPlot é uma ferramenta poderosa e flexível para visualizar flows do CrewAI. Sua arquitetura modular e opções de customização permitem criar visualizações profissionais e interativas, facilitando a compreensão e análise de flows complexos.
