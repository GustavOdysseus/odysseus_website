# Visualizações no Dashboard AgentOps

## Tipos de Visualizações

### 1. Gráficos de Linha
```python
from agentops import Dashboard, Visualization

# Criação de gráfico de linha
viz = Visualization.line_chart(
    metrics=["response_time"],
    timeframe="1h",
    aggregation="avg"
)
```

#### Uso Comum
- Métricas ao longo do tempo
- Tendências de performance
- Custos acumulados
- Uso de recursos

### 2. Gráficos de Barra
```python
# Gráfico de barras
viz = Visualization.bar_chart(
    metrics=["requests_per_agent"],
    groupby="agent_id",
    sort="desc"
)
```

#### Uso Comum
- Comparação entre agentes
- Distribuição de tarefas
- Uso de ferramentas
- Análise de erros

### 3. Heat Maps
```python
# Heat map
viz = Visualization.heat_map(
    metrics=["activity_level"],
    dimensions=["hour", "day"],
    color_scale="viridis"
)
```

#### Uso Comum
- Padrões de atividade
- Distribuição temporal
- Correlações
- Anomalias

### 4. Scatter Plots
```python
# Scatter plot
viz = Visualization.scatter_plot(
    x_metric="response_time",
    y_metric="tokens_used",
    color_by="model"
)
```

#### Uso Comum
- Correlações
- Outliers
- Clusters
- Performance

### 5. Sankey Diagrams
```python
# Diagrama Sankey
viz = Visualization.sankey_diagram(
    flows=["agent_interactions"],
    node_color="group"
)
```

#### Uso Comum
- Fluxo de trabalho
- Interações entre agentes
- Distribuição de recursos
- Caminhos de execução

## Dashboards Personalizados

### 1. Layout
```python
# Configuração de layout
dashboard = Dashboard()
dashboard.create_layout(
    title="Agent Performance",
    rows=2,
    cols=3
)
```

### 2. Widgets
```python
# Adição de widgets
dashboard.add_widget(
    visualization=viz,
    position=(0, 0),
    size=(1, 2)
)
```

### 3. Temas
```python
# Customização de tema
dashboard.set_theme(
    primary_color="#1a73e8",
    background="#f8f9fa",
    font="Roboto"
)
```

## Métricas em Tempo Real

### 1. Atualização Automática
```python
# Configuração de atualização
dashboard.configure_refresh(
    interval=5,  # segundos
    metrics=["active_agents", "costs"]
)
```

### 2. Streaming de Dados
```python
# Stream de métricas
dashboard.stream_metrics(
    callback=handle_updates,
    buffer_size=100
)
```

### 3. Alertas Visuais
```python
# Configuração de alertas visuais
dashboard.set_alerts(
    threshold={"response_time": 1000},
    visual="blink",
    sound=True
)
```

## Exportação e Compartilhamento

### 1. Exportação
```python
# Exportação de dashboard
dashboard.export(
    format="pdf",
    timeframe="1d",
    include_notes=True
)
```

### 2. Compartilhamento
```python
# Compartilhamento de URL
url = dashboard.share(
    access="view",
    expiration="7d"
)
```

### 3. Colaboração
```python
# Configuração de colaboração
dashboard.configure_sharing(
    team="data_science",
    permissions="edit"
)
```

## Análise Avançada

### 1. Filtros Dinâmicos
```python
# Adição de filtros
dashboard.add_filter(
    metric="agent_type",
    type="dropdown",
    default="all"
)
```

### 2. Drill-Down
```python
# Configuração de drill-down
dashboard.enable_drill_down(
    dimensions=["agent", "task", "tool"],
    max_depth=3
)
```

### 3. Análise Comparativa
```python
# Comparação de períodos
dashboard.compare_periods(
    metric="performance",
    periods=["current", "previous"],
    type="overlay"
)
```

## Integração com Notebooks

### 1. Jupyter
```python
# Integração com Jupyter
from agentops.jupyter import DashboardWidget

widget = DashboardWidget(dashboard)
display(widget)
```

### 2. Colab
```python
# Integração com Colab
dashboard.to_colab(
    height=600,
    width=800
)
```

### 3. VSCode
```python
# Integração com VSCode
dashboard.to_vscode(
    update_interval=5
)
```

## Customização Avançada

### 1. CSS Personalizado
```python
# Aplicação de CSS
dashboard.apply_css("""
    .metric-card {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
""")
```

### 2. JavaScript
```python
# Extensão com JavaScript
dashboard.extend_js("""
    function customAnimation() {
        // Código personalizado
    }
""")
```

### 3. Templates
```python
# Uso de templates
dashboard.use_template(
    name="performance_overview",
    customize={
        "colors": ["#1a73e8", "#34a853"],
        "layout": "grid"
    }
)
```
