# Sistema de Armazenamento do MLflow

## Visão Geral

O MLflow oferece um sistema flexível de armazenamento que suporta diferentes backends para armazenar metadados de experimentos, parâmetros, métricas e artefatos.

## Tipos de Armazenamento

### 1. Armazenamento Local (FileStore)

O armazenamento local é o padrão quando nenhuma URI específica é fornecida.

```python
# URI para armazenamento local
mlflow.set_tracking_uri("file:./mlruns")
```

#### Estrutura de Diretórios
```
mlruns/
├── 0/                          # ID do Experimento
│   ├── meta.yaml              # Metadados do experimento
│   ├── [run-id]/              # ID da execução
│   │   ├── metrics/           # Métricas em formato .json
│   │   ├── params/            # Parâmetros em arquivos de texto
│   │   ├── artifacts/         # Artefatos salvos
│   │   └── meta.yaml          # Metadados da execução
└── meta.yaml                  # Metadados globais
```

### 2. Banco de Dados (SQLAlchemy)

O MLflow suporta vários bancos de dados através do SQLAlchemy.

```python
# PostgreSQL
mlflow.set_tracking_uri("postgresql://user:password@localhost:5432/mlflow")

# MySQL
mlflow.set_tracking_uri("mysql://user:password@localhost:3306/mlflow")

# SQLite
mlflow.set_tracking_uri("sqlite:///mlflow.db")
```

### 3. Servidor MLflow Tracking

Para ambientes de produção, é recomendado usar um servidor MLflow dedicado.

```python
# Conectar a um servidor MLflow
mlflow.set_tracking_uri("http://localhost:5000")
```

## Configuração do Backend

### 1. Configuração via Código

```python
import mlflow

# Configurar URI de tracking
mlflow.set_tracking_uri("sqlite:///mlflow.db")

# Configurar URI de registro de modelos
mlflow.set_registry_uri("postgresql://user:password@localhost:5432/mlflow")
```

### 2. Configuração via Variáveis de Ambiente

```bash
# URI do servidor de tracking
export MLFLOW_TRACKING_URI="http://localhost:5000"

# URI do registro de modelos
export MLFLOW_REGISTRY_URI="postgresql://user:password@localhost:5432/mlflow"
```

## Armazenamento de Artefatos

### 1. Sistema de Arquivos Local

```python
# Configurar armazenamento local
mlflow.set_tracking_uri("file:./mlruns")
```

### 2. Amazon S3

```python
# Configurar S3
mlflow.set_tracking_uri("s3://bucket-name/path/to/mlruns")
```

### 3. Azure Blob Storage

```python
# Configurar Azure Blob
mlflow.set_tracking_uri("wasbs://container@account.blob.core.windows.net/path/to/mlruns")
```

## Boas Práticas

1. **Backup Regular**
   - Mantenha backups regulares do banco de dados
   - Use sistemas de armazenamento redundante para artefatos

2. **Monitoramento**
   - Monitore o uso de espaço em disco
   - Configure alertas para falhas de armazenamento

3. **Limpeza**
   ```python
   # Deletar execuções antigas
   from mlflow.tracking import MlflowClient
   
   client = MlflowClient()
   client.delete_run("run_id")
   ```

4. **Segurança**
   - Use credenciais seguras para bancos de dados
   - Configure autenticação para o servidor MLflow
   - Implemente controle de acesso baseado em funções (RBAC)

## Exemplo de Configuração Completa

```python
import mlflow
import os

# Configurar credenciais (preferencialmente via variáveis de ambiente)
os.environ["AWS_ACCESS_KEY_ID"] = "seu_access_key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "seu_secret_key"

# Configurar URIs
mlflow.set_tracking_uri("postgresql://user:password@localhost:5432/mlflow")
mlflow.set_registry_uri("s3://bucket-name/model-registry")

# Iniciar experimento
mlflow.set_experiment("meu_experimento")

# Usar o MLflow normalmente
with mlflow.start_run():
    mlflow.log_param("param1", "valor1")
    mlflow.log_metric("metrica1", 0.95)
    
    # Artefatos serão armazenados no S3
    mlflow.log_artifact("modelo.pkl")
```

## Próximos Passos

1. [Gerenciamento de Artefatos](./artifacts.md)
2. [Registro de Modelos](../models/README.md)
3. [Implantação](../deployment/README.md)
