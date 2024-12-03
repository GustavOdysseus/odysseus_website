# Ferramenta de Leitura de Diretório - Documentação

## Descrição
A Ferramenta de Leitura de Diretório é uma ferramenta utilitária para listar recursivamente o conteúdo de um diretório. Ela fornece uma maneira simples de explorar estruturas de diretório e obter uma lista de todos os arquivos dentro de um diretório especificado e seus subdiretórios.

## Principais Recursos

### Exploração de Diretório
- Travessia recursiva de diretório
- Listagem de caminhos de arquivo
- Normalização de caminho
- Formato de saída estruturado
- Suporte a subdiretórios

### Modos de Operação
1. **Modo de Diretório Fixo**
   - Diretório especificado na inicialização
   - Esquema simplificado
   - Acesso consistente ao diretório

2. **Modo de Diretório Dinâmico**
   - Diretório especificado por operação
   - Seleção flexível de diretório
   - Seleção de caminho em tempo de execução

## Componentes do Sistema

### 1. Esquemas de Entrada

#### FixedDirectoryReadToolSchema
- Usado quando o diretório é predefinido
- Nenhum parâmetro adicional necessário

#### DirectoryReadToolSchema
- Usado para seleção dinâmica de diretório
- Parâmetros:
  - `directory`: Caminho para o diretório (obrigatório)

### 2. Processamento
- Normalização de caminho
- Travessia recursiva
- Coleta de caminhos de arquivo
- Formatação de saída

## Exemplo de Uso

```python
# Inicializar com diretório fixo
ferramenta = DirectoryReadTool(directory="/caminho/para/diretorio")

# Listar conteúdo do diretório fixo
resultado = ferramenta.run()

# Inicializar para uso dinâmico
ferramenta = DirectoryReadTool()

# Listar conteúdo de diretório específico
resultado = ferramenta.run(directory="/caminho/para/outro/diretorio")
```

## Características Técnicas
- Manipulação de caminhos
- Travessia de diretório
- Coleta de caminhos de arquivo
- Formatação de saída
- Tratamento de erros

## Requisitos
- Acesso ao sistema de arquivos
- Permissões de leitura
- Caminhos de diretório válidos
- Módulo os do Python

## Recursos Especiais
- Travessia recursiva de diretório
- Normalização de caminho
- Saída estruturada
- Seleção flexível de diretório
- Listagem abrangente de arquivos

## Limitações e Considerações
- Diretório deve existir
- Permissões de leitura necessárias
- Desempenho com diretórios grandes
- Uso de memória para muitos arquivos
- Consistência do formato do caminho

## Notas
- Verificar permissões do diretório
- Tratar diretórios grandes com cuidado
- Considerar formatação de caminho
- Monitorar uso de memória
- Validar existência do diretório
- Tratar caracteres especiais em caminhos
