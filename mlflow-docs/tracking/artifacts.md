# Gerenciamento de Artefatos no MLflow

## Visão Geral

Artefatos no MLflow são arquivos associados a execuções (runs) que podem incluir modelos, datasets, visualizações, arquivos de configuração e muito mais. O MLflow oferece uma API flexível para gerenciar esses artefatos.

## Tipos de Artefatos

### 1. Modelos
```python
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression

# Treinar e salvar um modelo
model = LogisticRegression()
model.fit(X_train, y_train)

mlflow.sklearn.log_model(model, "modelo")
```

### 2. Datasets
```python
import pandas as pd

# Salvar dataset como artefato
df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
df.to_csv("dados.csv", index=False)
mlflow.log_artifact("dados.csv")
```

### 3. Visualizações
```python
import matplotlib.pyplot as plt

# Criar e salvar um gráfico
plt.plot([1, 2, 3], [4, 5, 6])
plt.savefig("grafico.png")
mlflow.log_artifact("grafico.png")
```

## Métodos de Logging

### 1. Log de Arquivo Único
```python
# Logar um único arquivo
mlflow.log_artifact("caminho/para/arquivo.txt")

# Logar com caminho personalizado
mlflow.log_artifact("local/arquivo.txt", "remoto/pasta")
```

### 2. Log de Diretório
```python
# Logar todos os arquivos em um diretório
mlflow.log_artifacts("pasta_local")

# Logar com caminho personalizado
mlflow.log_artifacts("pasta_local", "pasta_remota")
```

### 3. Log de Objetos Python
```python
# Logar um dicionário como JSON
dict_config = {"param1": 1, "param2": 2}
with open("config.json", "w") as f:
    json.dump(dict_config, f)
mlflow.log_artifact("config.json")
```

## Recuperação de Artefatos

### 1. Via Python API
```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Listar artefatos
artifacts = client.list_artifacts(run_id)

# Download de artefatos
local_path = client.download_artifacts(run_id, "modelo")
```

### 2. Via MLflow UI
```python
# O MLflow UI permite visualizar e baixar artefatos
# Inicie o servidor MLflow UI
mlflow.ui.serve()
```

## Armazenamento de Artefatos

### 1. Sistema de Arquivos Local
```python
# Configuração padrão
mlflow.set_tracking_uri("file:./mlruns")
```

### 2. Armazenamento em Nuvem

#### Amazon S3
```python
# Configurar S3
mlflow.set_tracking_uri("s3://seu-bucket/mlflow-artifacts")
```

#### Azure Blob Storage
```python
# Configurar Azure Blob
mlflow.set_tracking_uri("wasbs://container@account.blob.core.windows.net/artifacts")
```

#### Google Cloud Storage
```python
# Configurar GCS
mlflow.set_tracking_uri("gs://seu-bucket/mlflow-artifacts")
```

## Boas Práticas

### 1. Organização de Artefatos
```python
# Use estrutura de diretórios clara
mlflow.log_artifact("modelo.pkl", "modelos")
mlflow.log_artifact("dados.csv", "dados")
mlflow.log_artifact("config.yaml", "configs")
```

### 2. Versionamento
```python
# Inclua versão nos nomes dos artefatos
mlflow.log_artifact("modelo_v1.pkl", "modelos")
```

### 3. Documentação
```python
# Adicione arquivo README com metadados
with open("README.md", "w") as f:
    f.write("# Modelo de Classificação v1\n")
    f.write("- Data: 2023-10-25\n")
    f.write("- Autor: Equipe ML\n")
mlflow.log_artifact("README.md")
```

## Exemplo Completo

```python
import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Iniciar execução
with mlflow.start_run() as run:
    # 1. Preparar e salvar dados
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    
    # Salvar datasets
    pd.DataFrame(X_train).to_csv("train.csv", index=False)
    pd.DataFrame(X_test).to_csv("test.csv", index=False)
    mlflow.log_artifacts(".", "dados")
    
    # 2. Treinar e salvar modelo
    model = LogisticRegression()
    model.fit(X_train, y_train)
    mlflow.sklearn.log_model(model, "modelo")
    
    # 3. Criar e salvar visualizações
    plt.figure(figsize=(10, 6))
    sns.heatmap(X_train.corr())
    plt.savefig("correlacao.png")
    mlflow.log_artifact("correlacao.png", "visualizacoes")
    
    # 4. Salvar configurações
    config = {
        "split_ratio": 0.2,
        "random_state": 42,
        "model_params": model.get_params()
    }
    with open("config.json", "w") as f:
        json.dump(config, f)
    mlflow.log_artifact("config.json", "configs")
    
    # 5. Adicionar documentação
    with open("README.md", "w") as f:
        f.write(f"# Execução {run.info.run_id}\n")
        f.write("## Conteúdo\n")
        f.write("- dados/: Datasets de treino e teste\n")
        f.write("- modelo/: Modelo treinado\n")
        f.write("- visualizacoes/: Gráficos e análises\n")
        f.write("- configs/: Configurações do experimento\n")
    mlflow.log_artifact("README.md")
```

## Próximos Passos

1. [Registro de Modelos](../models/README.md)
2. [Implantação](../deployment/README.md)
3. [Monitoramento](../monitoring/README.md)
