# DallETool - Documentação

## Descrição
A DallETool é uma ferramenta que integra o modelo DALL-E da OpenAI para geração de imagens a partir de descrições textuais.

## Funcionalidades Principais

### Geração de Imagens
- Utiliza o modelo DALL-E 3 da OpenAI
- Gera imagens com resolução de 1024x1024 pixels
- Qualidade padrão de geração
- Gera uma imagem por requisição

### Parâmetros de Configuração
- `model`: "dall-e-3" (modelo atual da OpenAI)
- `size`: "1024x1024" (tamanho padrão da imagem)
- `quality`: "standard" (qualidade da geração)
- `n`: 1 (número de imagens geradas)

### Entrada Necessária
- `image_description`: String contendo a descrição detalhada da imagem desejada

### Saída
Retorna um JSON contendo:
- URL da imagem gerada
- Descrição revisada da imagem (prompt refinado pelo modelo)

## Exemplo de Uso
```python
dalle_tool = DallETool()
result = dalle_tool.run(image_description="Um gato laranja dormindo em uma almofada azul")
# Retorna JSON com URL da imagem e descrição revisada
```

## Requisitos
- Necessita de uma chave de API válida da OpenAI
- Biblioteca OpenAI instalada
- Acesso à internet para comunicação com a API

## Observações
- A ferramenta requer configuração prévia da chave da API OpenAI
- O tempo de geração pode variar dependendo da complexidade da imagem
- Respeita as políticas de uso e diretrizes da OpenAI
