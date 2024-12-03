# Configurações do Flow CrewAI

## Visão Geral

O módulo `config.py` define as configurações visuais e de estilo para o sistema de visualização do Flow CrewAI. Ele estabelece um conjunto consistente de cores, estilos e propriedades visuais que são usados em toda a visualização.

## Paleta de Cores

### Cores Base
```python
DARK_GRAY = "#333333"    # Cinza escuro para elementos principais
CREWAI_ORANGE = "#FF5A50" # Laranja CrewAI para destaques
GRAY = "#666666"         # Cinza para elementos secundários
WHITE = "#FFFFFF"        # Branco para fundos e texto
BLACK = "#000000"        # Preto para contraste máximo
```

### Mapa de Cores (COLORS)
```python
COLORS = {
    "bg": WHITE,                 # Fundo da visualização
    "start": CREWAI_ORANGE,      # Nós de início
    "method": DARK_GRAY,         # Nós de método
    "router": DARK_GRAY,         # Nós de roteamento
    "router_border": CREWAI_ORANGE, # Borda dos roteadores
    "edge": GRAY,                # Arestas padrão
    "router_edge": CREWAI_ORANGE,# Arestas de roteamento
    "text": WHITE,               # Texto padrão
}
```

## Estilos de Nós (NODE_STYLES)

### 1. Nós de Início
```python
"start": {
    "color": CREWAI_ORANGE,
    "shape": "box",
    "font": {
        "color": WHITE
    },
    "margin": {
        "top": 10,
        "bottom": 8,
        "left": 10,
        "right": 10
    }
}
```
#### Características
- Cor distintiva (laranja CrewAI)
- Forma retangular
- Texto branco para contraste
- Margens equilibradas

### 2. Nós de Método
```python
"method": {
    "color": DARK_GRAY,
    "shape": "box",
    "font": {
        "color": WHITE
    },
    "margin": {
        "top": 10,
        "bottom": 8,
        "left": 10,
        "right": 10
    }
}
```
#### Características
- Cor neutra (cinza escuro)
- Forma retangular
- Texto branco para contraste
- Margens consistentes

### 3. Nós de Roteamento
```python
"router": {
    "color": {
        "background": DARK_GRAY,
        "border": CREWAI_ORANGE,
        "highlight": {
            "border": CREWAI_ORANGE,
            "background": DARK_GRAY
        }
    },
    "shape": "box",
    "font": {
        "color": WHITE
    },
    "borderWidth": 3,
    "borderWidthSelected": 4,
    "shapeProperties": {
        "borderDashes": [5, 5]
    },
    "margin": {
        "top": 10,
        "bottom": 8,
        "left": 10,
        "right": 10
    }
}
```
#### Características
- Fundo cinza escuro
- Borda laranja tracejada
- Destaque na seleção
- Espessura de borda aumentada
- Padrão de traços na borda

### 4. Nós de Crew
```python
"crew": {
    "color": {
        "background": WHITE,
        "border": CREWAI_ORANGE
    },
    "shape": "box",
    "font": {
        "color": BLACK
    },
    "borderWidth": 3,
    "borderWidthSelected": 4,
    "shapeProperties": {
        "borderDashes": False
    },
    "margin": {
        "top": 10,
        "bottom": 8,
        "left": 10,
        "right": 10
    }
}
```
#### Características
- Fundo branco
- Borda laranja sólida
- Texto preto
- Espessura de borda aumentada
- Sem traços na borda

## Uso das Configurações

### 1. Aplicação em Visualizações
```python
from crewai.flow.config import COLORS, NODE_STYLES

def create_visualization():
    net = Network(
        bgcolor=COLORS["bg"]
    )
    
    # Aplicando estilos aos nós
    net.add_node(
        "start_node",
        **NODE_STYLES["start"]
    )
```

### 2. Customização
```python
# Customizando cores
custom_colors = COLORS.copy()
custom_colors["start"] = "#YOUR_COLOR"

# Customizando estilos
custom_styles = NODE_STYLES.copy()
custom_styles["start"]["shape"] = "circle"
```

## Melhores Práticas

### 1. Consistência Visual
- Mantenha a paleta de cores consistente
- Use as cores base para novos elementos
- Respeite a hierarquia visual

### 2. Acessibilidade
- Mantenha contraste adequado
- Use cores distintas para diferentes tipos
- Considere daltonismo

### 3. Extensibilidade
- Crie novas cores derivadas das bases
- Mantenha padrões de estilo
- Documente alterações

## Extensibilidade

### 1. Novas Cores
```python
# Adicionando novas cores
LIGHT_ORANGE = "#FFB3AE"  # Versão clara do CREWAI_ORANGE
DARK_ORANGE = "#CC4840"   # Versão escura do CREWAI_ORANGE

# Expandindo o mapa de cores
COLORS.update({
    "highlight": LIGHT_ORANGE,
    "shadow": DARK_ORANGE
})
```

### 2. Novos Estilos de Nó
```python
# Adicionando novo estilo de nó
NODE_STYLES["special"] = {
    "color": {
        "background": LIGHT_ORANGE,
        "border": DARK_ORANGE
    },
    "shape": "box",
    "font": {"color": BLACK},
    "borderWidth": 2
}
```

## Conclusão

O sistema de configuração do Flow CrewAI fornece uma base sólida e flexível para a estilização e personalização das visualizações. Sua estrutura organizada e modular permite fácil manutenção e extensão, mantendo a consistência visual em toda a aplicação.
