# Assets do Flow CrewAI

## Visão Geral

O diretório `assets` contém recursos essenciais para a visualização do Flow CrewAI, incluindo templates HTML e recursos visuais. Estes assets são fundamentais para criar visualizações profissionais e consistentes dos fluxos.

## Estrutura do Diretório

```
assets/
├── crewai_flow_visual_template.html  (2.4 KB)
└── crewai_logo.svg                   (26.7 KB)
```

## Template Visual (crewai_flow_visual_template.html)

### Estrutura Base
```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>{{ title }}</title>
    <!-- Dependencies -->
    <!-- Styles -->
  </head>
  <body>
    <!-- Content -->
  </body>
</html>
```

### Dependências Externas

#### 1. Vis Network
```html
<script
  src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js"
  integrity="sha512-LnvoEWDFrqGHlHmDD2101OrLcbsfkrzoSpvtSQtxK3RMnRV0eOkhhBN2dXHKRrUU8p2DGRTk35n4O8nWSVe1mQ=="
  crossorigin="anonymous"
  referrerpolicy="no-referrer"
></script>
```

#### 2. Vis Network CSS
```html
<link
  rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/dist/vis-network.min.css"
  integrity="sha512-WgxfT5LWjfszlPHXRmBWHkV2eceiWTOBvrKCNbdgDYTHrT2AeLCGbF4sZlZw3UMN3WtL0tGUoIAKsu8mllg/XA=="
  crossorigin="anonymous"
  referrerpolicy="no-referrer"
/>
```

### Estilos CSS Incorporados

#### 1. Layout Base
```css
body {
  font-family: verdana;
  margin: 0;
  padding: 0;
}

.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
```

#### 2. Área da Rede
```css
#mynetwork {
  flex-grow: 1;
  width: 100%;
  height: 750px;
  background-color: #ffffff;
}
```

#### 3. Legenda
```css
.legend-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  background-color: #f8f9fa;
  position: fixed;
  bottom: 0;
  width: 100%;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.legend-color-box {
  width: 20px;
  height: 20px;
  margin-right: 5px;
}
```

#### 4. Elementos da Legenda
```css
.legend-dashed {
  border-bottom: 2px dashed #666666;
  width: 20px;
  height: 0;
  margin-right: 5px;
}

.legend-solid {
  border-bottom: 2px solid #666666;
  width: 20px;
  height: 0;
  margin-right: 5px;
}
```

#### 5. Logo
```css
.logo {
  height: 50px;
  margin-right: 20px;
}
```

### Placeholders

1. `{{ title }}`: Título da visualização
2. `{{ logo_svg_base64 }}`: Logo em formato base64
3. `<!-- LEGEND_ITEMS_PLACEHOLDER -->`: Itens da legenda
4. `{{ network_content }}`: Conteúdo da rede

## Logo (crewai_logo.svg)

- Formato: SVG
- Tamanho: 26.7 KB
- Uso: Identidade visual do CrewAI
- Incorporação: Convertido para base64 no template

## Uso dos Assets

### 1. Carregamento do Template
```python
def load_template():
    template_path = os.path.join(
        current_dir, 
        "assets", 
        "crewai_flow_visual_template.html"
    )
    return template_path
```

### 2. Carregamento do Logo
```python
def load_logo():
    logo_path = os.path.join(
        current_dir,
        "assets",
        "crewai_logo.svg"
    )
    return logo_path
```

### 3. Geração do HTML Final
```python
def generate_html(template_path, logo_path):
    handler = HTMLTemplateHandler(template_path, logo_path)
    return handler.generate_final_html(
        network_body,
        legend_items_html
    )
```

## Melhores Práticas

### 1. Gerenciamento de Assets
- Mantenha os assets no diretório apropriado
- Use caminhos relativos
- Valide integridade dos arquivos

### 2. Template HTML
- Mantenha o código limpo e organizado
- Use comentários descritivos
- Siga padrões de HTML5

### 3. Estilos CSS
- Organize por componente
- Use nomes de classe descritivos
- Mantenha consistência visual

### 4. Performance
- Otimize tamanho dos assets
- Use CDNs para dependências
- Minimize requisições HTTP

## Extensibilidade

### 1. Temas Customizados
```css
/* custom-theme.css */
:root {
  --primary-color: #YOUR_COLOR;
  --secondary-color: #YOUR_COLOR;
  --background-color: #YOUR_COLOR;
}
```

### 2. Templates Alternativos
```html
<!-- custom-template.html -->
<!DOCTYPE html>
<html>
  <head>
    <!-- Custom head content -->
  </head>
  <body>
    <!-- Custom layout -->
  </body>
</html>
```

## Conclusão

Os assets do Flow CrewAI fornecem uma base sólida para a visualização de fluxos, com um template HTML bem estruturado e recursos visuais profissionais. A organização modular e as opções de customização permitem adaptar a visualização para diferentes necessidades, mantendo a consistência e qualidade.
