# Gerenciador de Templates HTML do Flow CrewAI

## Visão Geral

O módulo `html_template_handler.py` é responsável por gerenciar e manipular templates HTML para a visualização do Flow CrewAI. Ele fornece uma interface limpa e flexível para gerar visualizações HTML interativas, incluindo suporte para logos, legendas e conteúdo dinâmico.

## Classe Principal: HTMLTemplateHandler

```python
class HTMLTemplateHandler:
    def __init__(self, template_path, logo_path):
        """
        Inicializa o gerenciador de templates.
        
        Args:
            template_path: Caminho para o arquivo de template HTML
            logo_path: Caminho para o arquivo de logo
        """
```

### Métodos Principais

#### 1. Leitura de Template
```python
def read_template(self):
    """
    Lê o arquivo de template HTML.
    
    Returns:
        str: Conteúdo do template HTML
    """
```

#### 2. Codificação de Logo
```python
def encode_logo(self):
    """
    Codifica o arquivo de logo em base64.
    
    Returns:
        str: Logo codificada em base64
    """
```

#### 3. Extração de Conteúdo
```python
def extract_body_content(self, html):
    """
    Extrai o conteúdo do corpo do HTML.
    
    Args:
        html: String HTML completa
        
    Returns:
        str: Conteúdo do corpo do HTML
    """
```

#### 4. Geração de Legendas
```python
def generate_legend_items_html(self, legend_items):
    """
    Gera o HTML para os itens da legenda.
    
    Args:
        legend_items: Lista de itens da legenda
        
    Returns:
        str: HTML formatado da legenda
    """
```

#### 5. Geração HTML Final
```python
def generate_final_html(self, network_body, legend_items_html, title="Flow Plot"):
    """
    Gera o HTML final combinando todos os elementos.
    
    Args:
        network_body: Conteúdo HTML da rede
        legend_items_html: HTML da legenda
        title: Título da visualização
        
    Returns:
        str: HTML final completo
    """
```

## Tipos de Elementos HTML

### 1. Elementos com Borda
```html
<div class="legend-item">
    <div class="legend-color-box" 
         style="background-color: {color}; 
                border: 2px dashed {border};">
    </div>
    <div>{label}</div>
</div>
```

### 2. Elementos com Linha
```html
<div class="legend-item">
    <div class="legend-{style}" 
         style="border-bottom: 2px {style} {color};">
    </div>
    <div>{label}</div>
</div>
```

### 3. Elementos Simples
```html
<div class="legend-item">
    <div class="legend-color-box" 
         style="background-color: {color};">
    </div>
    <div>{label}</div>
</div>
```

## Estrutura do Template

### Placeholders
1. `{{ title }}`: Título da visualização
2. `{{ network_content }}`: Conteúdo da rede
3. `{{ logo_svg_base64 }}`: Logo codificada
4. `<!-- LEGEND_ITEMS_PLACEHOLDER -->`: Itens da legenda

### Exemplo de Template Base
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        /* Estilos CSS */
    </style>
</head>
<body>
    <div class="header">
        <img src="data:image/svg+xml;base64,{{ logo_svg_base64 }}" />
        <h1>{{ title }}</h1>
    </div>
    <div class="network-container">
        {{ network_content }}
    </div>
    <div class="legend">
        <!-- LEGEND_ITEMS_PLACEHOLDER -->
    </div>
</body>
</html>
```

## Casos de Uso

### 1. Visualização Básica
```python
handler = HTMLTemplateHandler("template.html", "logo.svg")
network_html = generate_network_html()  # Função hipotética
legend_items = get_legend_items()       # Função hipotética
final_html = handler.generate_final_html(
    network_html,
    handler.generate_legend_items_html(legend_items)
)
```

### 2. Visualização Customizada
```python
handler = HTMLTemplateHandler("custom_template.html", "custom_logo.svg")
network_html = generate_custom_network()  # Função hipotética
legend_items = get_custom_legend_items() # Função hipotética
final_html = handler.generate_final_html(
    network_html,
    handler.generate_legend_items_html(legend_items),
    title="Custom Flow Visualization"
)
```

## Melhores Práticas

### 1. Manipulação de Templates
- Use encoding UTF-8
- Valide placeholders
- Mantenha templates limpos

### 2. Manipulação de Logos
- Use SVG para melhor qualidade
- Otimize tamanhos de arquivo
- Valide formatos suportados

### 3. Geração HTML
- Escape caracteres especiais
- Valide HTML gerado
- Mantenha consistência de estilo

## Extensibilidade

### 1. Templates Customizados
```python
class CustomTemplateHandler(HTMLTemplateHandler):
    def custom_placeholder(self, content):
        return f"<!-- CUSTOM_{content} -->"
        
    def add_custom_section(self, html, section):
        return html.replace(
            self.custom_placeholder("SECTION"),
            section
        )
```

### 2. Estilos Adicionais
```python
def add_custom_styles(self, html, styles):
    style_tag = f"<style>{styles}</style>"
    return html.replace("</head>", f"{style_tag}</head>")
```

## CSS Recomendado

```css
.header {
    display: flex;
    align-items: center;
    padding: 20px;
}

.header img {
    height: 40px;
    margin-right: 20px;
}

.network-container {
    height: 600px;
    border: 1px solid #ddd;
    margin: 20px;
}

.legend {
    position: absolute;
    top: 20px;
    right: 20px;
    background: white;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
}
```

## Conclusão

O HTMLTemplateHandler é uma ferramenta robusta e flexível para gerar visualizações HTML do Flow CrewAI. Sua arquitetura modular e suporte a customização permitem criar visualizações profissionais e interativas, mantendo o código organizado e manutenível.
