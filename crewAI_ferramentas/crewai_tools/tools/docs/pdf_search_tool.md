# Ferramenta de Busca em PDF - Documentação

## Descrição
A Ferramenta de Busca em PDF é uma solução avançada para realizar buscas semânticas em documentos PDF. Baseada em tecnologia de ponta para processamento de documentos, utiliza algoritmos sofisticados de análise semântica para extrair e localizar informações relevantes em arquivos PDF com alta precisão e eficiência.

## Funcionalidades Principais

### Capacidades de Busca Avançada
- Processamento semântico profundo
- Análise contextual inteligente
- Extração de texto otimizada
- OCR integrado (quando necessário)
- Indexação eficiente
- Cache adaptativo
- Processamento paralelo
- Compressão inteligente
- Validação de conteúdo
- Análise estrutural

### Modos de Operação
1. **Modo de Documento Fixo**
   - Indexação prévia do documento
   - Cache persistente
   - Otimização de performance
   - Busca rápida
   - Análise incremental
   - Monitoramento contínuo
   - Backup automático
   - Validação de integridade

2. **Modo de Documento Dinâmico**
   - Processamento sob demanda
   - Cache temporário
   - Otimização adaptativa
   - Análise em tempo real
   - Validação dinâmica
   - Monitoramento de recursos
   - Backup incremental
   - Limpeza automática

## Arquitetura do Sistema

### 1. Schemas de Entrada

#### FixedPDFSearchToolSchema
- Parâmetros Obrigatórios:
  - `query`: String de busca
- Parâmetros Opcionais:
  - `max_results`: Limite de resultados
  - `min_relevance`: Relevância mínima
  - `timeout`: Tempo limite
  - `include_metadata`: Incluir metadados
  - `extract_images`: Extrair imagens
  - `ocr_enabled`: Habilitar OCR
  - `cache_strategy`: Estratégia de cache
  - `compression_level`: Nível de compressão

#### PDFSearchToolSchema
- Parâmetros Obrigatórios:
  - `query`: String de busca
  - `pdf`: Caminho do arquivo
- Parâmetros Opcionais:
  - `max_results`: Limite de resultados
  - `min_relevance`: Relevância mínima
  - `timeout`: Tempo limite
  - `include_metadata`: Incluir metadados
  - `extract_images`: Extrair imagens
  - `ocr_enabled`: Habilitar OCR
  - `cache_strategy`: Estratégia de cache
  - `compression_level`: Nível de compressão

### 2. Sistema de Processamento
- PDFEmbedchainAdapter otimizado
- Pipeline de processamento modular
- Sistema de cache multinível
- Processamento paralelo
- Compressão adaptativa
- Validação robusta
- Logging estruturado
- Monitoramento em tempo real
- Backup automático
- Recuperação de falhas

## Exemplo de Implementação

```python
# Configuração Avançada
ferramenta = PDFSearchTool(
    pdf="caminho/para/documento.pdf",
    max_results=100,
    min_relevance=0.7,
    timeout=300,
    include_metadata=True,
    extract_images=True,
    ocr_enabled=True,
    cache_strategy="adaptive",
    compression_level="high"
)

# Busca Básica
resultado = ferramenta.run(
    query="conceito específico"
)

# Busca Avançada
resultado = ferramenta.run(
    query="termo complexo",
    pdf="outro/documento.pdf",
    max_results=50,
    min_relevance=0.8,
    include_metadata=True,
    extract_images=True,
    timeout=60
)
```

## Requisitos Técnicos
- EmbedChain Framework
- Python 3.7+
- PyPDF2 ou pdfreader
- Tesseract OCR (opcional)
- PIL/Pillow
- numpy
- pandas
- scipy
- RAM adequada
- CPU multicore
- Armazenamento SSD
- SO compatível

## Recursos Avançados
- Busca semântica profunda
- OCR inteligente
- Extração de metadados
- Processamento paralelo
- Cache multinível
- Compressão adaptativa
- Backup incremental
- Monitoramento real-time
- Análise estatística
- Exportação customizada
- Validação robusta
- Recuperação de falhas
- Logging avançado
- Alertas inteligentes

## Limitações e Considerações
- Tamanho do documento
- Qualidade do PDF
- Recursos computacionais
- Tempo de processamento
- Uso de memória
- Complexidade do texto
- Qualidade do OCR
- Performance de rede
- Espaço em disco
- Concorrência
- Timeouts
- Falhas de processamento

## Notas de Implementação
- Validar formato PDF
- Configurar OCR
- Implementar cache
- Otimizar memória
- Gerenciar recursos
- Implementar retry
- Monitorar performance
- Configurar backup
- Validar resultados
- Implementar logging
- Gerenciar erros
- Otimizar queries
- Comprimir dados
- Validar metadados
- Implementar alertas
- Documentar processos
- Testar escalabilidade
- Medir performance
- Validar integridade
- Monitorar recursos
- Implementar métricas
- Otimizar pipeline
- Manter documentação
- Realizar backups
