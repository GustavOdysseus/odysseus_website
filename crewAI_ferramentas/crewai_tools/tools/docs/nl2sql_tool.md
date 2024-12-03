# Ferramenta NL2SQL - Documentação

## Descrição
A Ferramenta NL2SQL é uma ferramenta especializada para executar consultas SQL e fornecer informações sobre o schema do banco de dados. Ela facilita operações de banco de dados gerenciando conexões, executando consultas e manipulando metadados do schema.

## Principais Recursos

### Operações de Banco de Dados
- Execução de consulta SQL
- Introspecção de schema
- Recuperação de metadados de tabela
- Acesso a informações de coluna
- Gerenciamento de transação

### Capacidades de Operação
1. **Gerenciamento de Schema**
   - Listagem de tabelas
   - Informação de colunas
   - Rastreamento de tipo de dados
   - Validação de schema

2. **Execução de Consulta**
   - Execução SQL
   - Manipulação de transação
   - Formatação de resultado
   - Gerenciamento de erro

## Componentes do Sistema

### 1. Schema de Entrada

#### NL2SQLToolInput
- Parâmetros:
  - `sql_query`: Consulta SQL para executar (obrigatório)
  - `db_uri`: URI do banco de dados (obrigatório)

### 2. Processamento
- Gerenciamento de conexão
- Execução de consulta
- Introspecção de schema
- Formatação de resultado
- Tratamento de erro

## Exemplo de Uso

```python
# Inicializar a ferramenta
ferramenta = NL2SQLTool(
    db_uri="postgresql://usuario:senha@localhost:5432/banco"
)

# Executar consulta SQL
resultado = ferramenta.run(
    sql_query="SELECT * FROM usuarios WHERE idade > 25;"
)

# Acessar informações de schema
tabelas = ferramenta.tables  # Listar tabelas disponíveis
colunas = ferramenta.columns  # Obter informações de coluna
```

## Características Técnicas
- Integração com SQLAlchemy
- Suporte a transação
- Introspecção de schema
- Pool de conexões
- Formatação de resultado

## Requisitos
- Biblioteca SQLAlchemy
- Conexão com banco de dados
- Credenciais válidas
- Acesso à rede
- Permissões de schema

## Recursos Especiais
- Descoberta automática de schema
- Gerenciamento de transação
- Recuperação de erro
- Formatação de resultado
- Pool de conexões
- Cache de schema

## Limitações e Considerações
- Overhead de conexão
- Desempenho de consulta
- Isolamento de transação
- Uso de memória
- Latência de rede
- Mudanças de schema

## Notas
- Verificar credenciais
- Monitorar conexões
- Manipular transações
- Gerenciar recursos
- Considerar pooling
- Testar consultas
- Tratar erros com cuidado
- Monitorar desempenho
- Armazenar schema em cache
- Validar consultas
- Otimizar desempenho
- Documentar schemas
- Manter logs de execução
