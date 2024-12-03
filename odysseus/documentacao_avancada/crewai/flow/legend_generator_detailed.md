# Gerador de Legendas do Flow CrewAI

## Visão Geral

O módulo `legend_generator.py` é responsável por criar legendas interativas e visualmente informativas para as visualizações do Flow CrewAI. Ele fornece uma maneira consistente e personalizável de representar diferentes tipos de nós e conexões no fluxo.

## Componentes Principais

### 1. Itens de Legenda (get_legend_items)

```python
def get_legend_items(colors):
    """
    Gera os itens da legenda com suas respectivas cores e estilos.
    
    Args:
        colors: Dicionário com as cores do tema
        
    Returns:
        List[Dict]: Lista de itens da legenda
    """
```

#### Tipos de Itens
1. Start Method
   - Cor sólida
   - Representa pontos de início
   - Estilo visual distinto

2. Method
   - Cor padrão
   - Representa métodos regulares
   - Sem bordas especiais

3. Crew Method
   - Cor de fundo personalizada
   - Borda especial
   - Estilo sólido

4. Router
   - Cor específica para roteadores
   - Borda tracejada
   - Estilo visual único

5. Trigger
   - Cor para conexões
   - Estilo de linha sólida
   - Representa gatilhos simples

6. AND Trigger
   - Cor para conexões
   - Linha tracejada
   - Representa condições AND

7. Router Trigger
   - Cor específica para rotas
   - Linha tracejada
   - Representa conexões de roteamento

### 2. Geração de HTML (generate_legend_items_html)

```python
def generate_legend_items_html(legend_items):
    """
    Gera o HTML para os itens da legenda.
    
    Args:
        legend_items: Lista de itens da legenda
        
    Returns:
        str: HTML formatado da legenda
    """
```

#### Tipos de Elementos HTML

1. Elementos com Borda
```html
<div class="legend-item">
    <div class="legend-color-box" 
         style="background-color: {color}; 
                border: 2px {style} {border}; 
                border-radius: 5px;">
    </div>
    <div>{label}</div>
</div>
```

2. Elementos com Linha
```html
<div class="legend-item">
    <div class="legend-{style}" 
         style="border-bottom: 2px {style} {color}; 
                border-radius: 5px;">
    </div>
    <div>{label}</div>
</div>
```

3. Elementos Simples
```html
<div class="legend-item">
    <div class="legend-color-box" 
         style="background-color: {color}; 
                border-radius: 5px;">
    </div>
    <div>{label}</div>
</div>
```

## Esquema de Cores Padrão

```python
default_colors = {
    "start": "#4CAF50",      # Verde
    "method": "#2196F3",     # Azul
    "bg": "#FFFFFF",         # Branco
    "router": "#FF5722",     # Laranja
    "router_border": "#D84315", # Laranja Escuro
    "edge": "#2B7CE9",       # Azul Claro
    "router_edge": "#FF9800" # Laranja Claro
}
```

## Casos de Uso

### 1. Legenda Padrão
```python
def create_default_legend():
    colors = default_colors
    items = get_legend_items(colors)
    return generate_legend_items_html(items)
```

### 2. Legenda Customizada
```python
def create_custom_legend(custom_colors):
    items = get_legend_items(custom_colors)
    return generate_legend_items_html(items)
```

## Melhores Práticas

### 1. Cores
- Use cores contrastantes
- Mantenha consistência visual
- Considere acessibilidade

### 2. Estilos
- Mantenha padrões consistentes
- Use bordas para diferenciação
- Aplique estilos de linha apropriados

### 3. Layout
- Organize itens logicamente
- Mantenha espaçamento adequado
- Agrupe itens relacionados

## Extensibilidade

### 1. Cores Customizadas
```python
custom_colors = {
    "start": "#YOUR_COLOR",
    "method": "#YOUR_COLOR",
    "bg": "#YOUR_COLOR",
    "router": "#YOUR_COLOR",
    "router_border": "#YOUR_COLOR",
    "edge": "#YOUR_COLOR",
    "router_edge": "#YOUR_COLOR"
}
```

### 2. Itens Adicionais
```python
def add_custom_legend_item(items, label, color, style=None):
    items.append({
        "label": label,
        "color": color,
        "dashed": style == "dashed"
    })
    return items
```

## CSS Recomendado

```css
.legend-item {
    display: flex;
    align-items: center;
    margin: 5px 0;
}

.legend-color-box {
    width: 20px;
    height: 20px;
    margin-right: 10px;
}

.legend-solid,
.legend-dashed {
    width: 30px;
    height: 0;
    margin-right: 10px;
}

.legend-item div {
    font-size: 14px;
    color: #333;
}
```

## Conclusão

O sistema de geração de legendas do CrewAI Flow é uma ferramenta essencial para criar visualizações compreensíveis e profissionais. Sua flexibilidade permite adaptação a diferentes necessidades de visualização, mantendo consistência e clareza na representação dos elementos do fluxo.
