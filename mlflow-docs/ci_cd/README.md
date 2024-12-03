# Integração Contínua e Entrega Contínua (CI/CD) com MLflow

## Visão Geral

A integração contínua e entrega contínua (CI/CD) são práticas essenciais para garantir a qualidade e confiabilidade de projetos de machine learning. Com MLflow, podemos automatizar o processo de treinamento, validação e implantação de modelos.

## Estrutura do Pipeline

### 1. GitHub Actions
```yaml
# .github/workflows/mlflow-ci.yml
name: MLflow CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Run tests
      run: |
        pytest tests/
        
  train:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Train model
      run: |
        mlflow run . -P data_path=data/train.csv
        
    - name: Register model
      run: |
        python scripts/register_model.py
```

### 2. Script de Registro de Modelo
```python
# scripts/register_model.py
import mlflow
from mlflow.tracking import MlflowClient

def register_best_model():
    client = MlflowClient()
    
    # Buscar melhor modelo baseado em métricas
    runs = mlflow.search_runs(
        experiment_ids=['1'],
        filter_string="metrics.test_score > 0.8",
        order_by=["metrics.test_score DESC"]
    )
    
    if len(runs) > 0:
        best_run = runs.iloc[0]
        
        # Registrar modelo
        model_uri = f"runs:/{best_run.run_id}/model"
        mv = mlflow.register_model(model_uri, "production_model")
        
        # Transicionar para produção
        client.transition_model_version_stage(
            name="production_model",
            version=mv.version,
            stage="Production"
        )

if __name__ == "__main__":
    register_best_model()
```

## Componentes do Pipeline

### 1. Testes Automatizados
```python
# tests/test_pipeline.py
import pytest
import mlflow
from src.pipeline import train_model

def test_model_training():
    # Configurar ambiente de teste
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("test_experiment")
    
    # Treinar modelo
    with mlflow.start_run():
        model = train_model(num_trees=10)
        
        # Verificar métricas
        metrics = mlflow.get_run(
            mlflow.active_run().info.run_id
        ).data.metrics
        
        assert "test_score" in metrics
        assert metrics["test_score"] > 0.7

def test_model_artifacts():
    with mlflow.start_run():
        model = train_model(num_trees=10)
        
        # Verificar artefatos
        artifacts = mlflow.get_artifact_uri()
        assert artifacts is not None
```

### 2. Validação de Modelo
```python
# scripts/validate_model.py
import mlflow
import numpy as np
from sklearn.metrics import classification_report

def validate_production_model():
    client = MlflowClient()
    
    # Carregar modelo em produção
    model = mlflow.pyfunc.load_model(
        model_uri="models:/production_model/Production"
    )
    
    # Carregar dados de validação
    X_val, y_val = load_validation_data()
    
    # Fazer predições
    predictions = model.predict(X_val)
    
    # Gerar relatório
    report = classification_report(y_val, predictions)
    
    # Logging de métricas
    with mlflow.start_run():
        mlflow.log_metrics({
            "validation_accuracy": np.mean(predictions == y_val),
            "validation_f1": f1_score(y_val, predictions)
        })
        
        # Salvar relatório
        with open("validation_report.txt", "w") as f:
            f.write(report)
        mlflow.log_artifact("validation_report.txt")

if __name__ == "__main__":
    validate_production_model()
```

### 3. Monitoramento de Drift
```python
# scripts/monitor_drift.py
import mlflow
import pandas as pd
from scipy.stats import ks_2samp

def detect_data_drift():
    # Carregar dados de referência
    reference_data = pd.read_csv("data/reference.csv")
    
    # Carregar dados atuais
    current_data = pd.read_csv("data/current.csv")
    
    drift_metrics = {}
    
    # Calcular drift para cada feature
    for column in reference_data.columns:
        statistic, p_value = ks_2samp(
            reference_data[column],
            current_data[column]
        )
        
        drift_metrics[f"{column}_drift"] = statistic
        drift_metrics[f"{column}_p_value"] = p_value
    
    # Logging de métricas
    with mlflow.start_run():
        mlflow.log_metrics(drift_metrics)
        
        # Alertar se drift significativo
        if any(v < 0.05 for k, v in drift_metrics.items() if "p_value" in k):
            raise ValueError("Significant data drift detected!")

if __name__ == "__main__":
    detect_data_drift()
```

## Configuração do Ambiente

### 1. Requirements
```txt
# requirements.txt
mlflow>=2.0.0
scikit-learn>=1.0.0
pandas>=1.3.0
pytest>=7.0.0
numpy>=1.20.0
scipy>=1.7.0
```

### 2. Configuração MLflow
```python
# config/mlflow_config.py
import os
import mlflow

def setup_mlflow():
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME"))
    
    # Configurar autenticação
    os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_USER")
    os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_PASSWORD")

```

## Boas Práticas

### 1. Versionamento de Dados
```python
# src/data_version.py
import hashlib
import pandas as pd

def get_data_version(data_path):
    df = pd.read_csv(data_path)
    
    # Calcular hash dos dados
    data_hash = hashlib.md5(
        pd.util.hash_pandas_object(df).values
    ).hexdigest()
    
    return data_hash

def log_data_version():
    with mlflow.start_run():
        data_hash = get_data_version("data/train.csv")
        mlflow.log_param("data_version", data_hash)
```

### 2. Reprodutibilidade
```python
# src/reproducibility.py
import random
import numpy as np
import torch

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    
def log_environment():
    with mlflow.start_run():
        mlflow.log_param("python_version", sys.version)
        mlflow.log_param("sklearn_version", sklearn.__version__)
        mlflow.log_param("cuda_available", torch.cuda.is_available())
```

### 3. Logging Avançado
```python
# src/logging_utils.py
import logging
import mlflow

class MLflowHandler(logging.Handler):
    def emit(self, record):
        with mlflow.start_run():
            mlflow.log_metric(
                f"log_{record.levelname.lower()}",
                1
            )
            
            if record.levelno >= logging.ERROR:
                mlflow.log_artifact("error.log")

def setup_logging():
    logger = logging.getLogger(__name__)
    logger.addHandler(MLflowHandler())
    return logger
```

## Exemplos de Uso

### 1. Pipeline Completo
```bash
# Executar pipeline completo
mlflow run . -P data_path=data/train.csv -P num_trees=100

# Validar modelo
python scripts/validate_model.py

# Monitorar drift
python scripts/monitor_drift.py
```

### 2. CI/CD Manual
```bash
# Executar testes
pytest tests/

# Treinar modelo
mlflow run .

# Registrar modelo
python scripts/register_model.py

# Validar modelo em produção
python scripts/validate_model.py
```

## Próximos Passos

1. [Governança de Modelos](../governance/README.md)
2. [Melhores Práticas](../best_practices/README.md)
3. [Monitoramento](../monitoring/README.md)
