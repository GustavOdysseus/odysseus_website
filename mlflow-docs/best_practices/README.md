# Melhores Práticas com MLflow

## Visão Geral

Este guia apresenta as melhores práticas para o uso do MLflow em projetos de machine learning, abrangendo organização de código, experimentação, tracking, registro de modelos e implantação.

## Organização de Projetos

### 1. Estrutura de Diretórios
```
projeto_ml/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── load.py
│   │   └── preprocess.py
│   ├── features/
│   │   ├── __init__.py
│   │   └── build.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train.py
│   │   └── predict.py
│   └── utils/
│       ├── __init__.py
│       └── metrics.py
├── tests/
│   ├── __init__.py
│   ├── test_data.py
│   └── test_models.py
├── notebooks/
│   └── exploratory.ipynb
├── configs/
│   ├── model_config.yaml
│   └── mlflow_config.yaml
├── MLproject
├── conda.yaml
└── README.md
```

### 2. Configuração do MLflow
```yaml
# configs/mlflow_config.yaml
tracking_server:
  uri: "sqlite:///mlflow.db"
  
experiments:
  default: "desenvolvimento"
  production: "producao"
  
artifacts:
  store: "./artifacts"
  
registry:
  uri: "sqlite:///mlflow.db"
  
logging:
  level: "INFO"
```

### 3. Configuração do Modelo
```yaml
# configs/model_config.yaml
model:
  name: "modelo_regressao"
  type: "RandomForestRegressor"
  params:
    n_estimators: 100
    max_depth: 10
    
training:
  test_size: 0.2
  random_state: 42
  
metrics:
  - "rmse"
  - "mae"
  - "r2"
  
validation:
  cv_folds: 5
```

## Experimentação

### 1. Tracking de Experimentos
```python
# src/utils/tracking.py
import mlflow
import yaml
from functools import wraps

def load_config():
    with open("configs/mlflow_config.yaml") as f:
        return yaml.safe_load(f)

def setup_tracking():
    config = load_config()
    mlflow.set_tracking_uri(config["tracking_server"]["uri"])
    mlflow.set_experiment(config["experiments"]["default"])

def track_experiment(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with mlflow.start_run():
            # Logging de parâmetros
            mlflow.log_params(kwargs)
            
            # Executar função
            result = func(*args, **kwargs)
            
            # Logging de métricas
            if isinstance(result, dict):
                mlflow.log_metrics(result)
            
            return result
    return wrapper
```

### 2. Reprodutibilidade
```python
# src/utils/reproducibility.py
import random
import numpy as np
import torch
import mlflow

def set_seed(seed=42):
    """Garantir reprodutibilidade"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    
def log_environment():
    """Registrar informações do ambiente"""
    with mlflow.start_run():
        mlflow.log_param("python_version", sys.version)
        mlflow.log_param("mlflow_version", mlflow.__version__)
        mlflow.log_param("cuda_available", torch.cuda.is_available())
        
        # Versões das dependências
        deps = mlflow.get_system_info()
        mlflow.log_dict(deps, "dependencies.json")
```

### 3. Métricas Customizadas
```python
# src/utils/metrics.py
import mlflow
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

class CustomMetrics(mlflow.metrics.Metric):
    def __init__(self):
        self.values = []
        
    def update(self, y_true, y_pred):
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        
        self.values.append({
            "rmse": rmse,
            "r2": r2
        })
        
    def compute(self):
        metrics = {
            k: np.mean([v[k] for v in self.values])
            for k in self.values[0].keys()
        }
        return metrics
```

## Treinamento de Modelos

### 1. Pipeline de Treinamento
```python
# src/models/train.py
import mlflow
import yaml
from sklearn.model_selection import train_test_split

@track_experiment
def train_model(data, config_path="configs/model_config.yaml"):
    # Carregar configuração
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Preparar dados
    X_train, X_test, y_train, y_test = train_test_split(
        data.drop(target_column, axis=1),
        data[target_column],
        test_size=config["training"]["test_size"],
        random_state=config["training"]["random_state"]
    )
    
    # Treinar modelo
    model = create_model(config["model"])
    model.fit(X_train, y_train)
    
    # Avaliar modelo
    metrics = evaluate_model(model, X_test, y_test)
    
    # Salvar modelo
    mlflow.sklearn.log_model(
        model,
        "model",
        registered_model_name=config["model"]["name"]
    )
    
    return metrics
```

### 2. Validação Cruzada
```python
# src/models/validate.py
import mlflow
from sklearn.model_selection import cross_validate

def cross_val_metrics(model, X, y, config):
    # Executar validação cruzada
    cv_results = cross_validate(
        model,
        X,
        y,
        cv=config["validation"]["cv_folds"],
        scoring=config["metrics"]
    )
    
    # Logging de métricas
    with mlflow.start_run():
        for metric in config["metrics"]:
            mlflow.log_metric(
                f"cv_{metric}_mean",
                cv_results[f"test_{metric}"].mean()
            )
            mlflow.log_metric(
                f"cv_{metric}_std",
                cv_results[f"test_{metric}"].std()
            )
```

## Registro de Modelos

### 1. Seleção de Modelos
```python
# src/models/selection.py
import mlflow
from mlflow.tracking import MlflowClient

def select_best_model(experiment_id, metric="rmse", ascending=True):
    # Buscar runs
    runs = mlflow.search_runs(
        experiment_ids=[experiment_id],
        order_by=[f"metrics.{metric} {'ASC' if ascending else 'DESC'}"]
    )
    
    if len(runs) == 0:
        raise ValueError("No runs found")
    
    best_run = runs.iloc[0]
    
    # Carregar melhor modelo
    model = mlflow.sklearn.load_model(
        f"runs:/{best_run.run_id}/model"
    )
    
    return model, best_run

def compare_models(experiment_id, baseline_metric):
    client = MlflowClient()
    
    # Buscar todos os modelos
    runs = mlflow.search_runs([experiment_id])
    
    # Comparar com baseline
    improvements = []
    for _, run in runs.iterrows():
        metric_value = run.metrics.get(baseline_metric, 0)
        improvement = {
            "run_id": run.run_id,
            "metric": metric_value,
            "improvement": metric_value - baseline_metric
        }
        improvements.append(improvement)
    
    return pd.DataFrame(improvements)
```

### 2. Transições de Estágio
```python
# src/models/staging.py
import mlflow
from mlflow.tracking import MlflowClient

def promote_model(model_name, version, stage):
    client = MlflowClient()
    
    # Verificar métricas mínimas
    model_version = client.get_model_version(
        name=model_name,
        version=version
    )
    
    run = mlflow.get_run(model_version.run_id)
    metrics = run.data.metrics
    
    if metrics["rmse"] > 0.5:  # Exemplo de threshold
        raise ValueError("Model performance below threshold")
    
    # Promover modelo
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage=stage
    )
    
    # Logging da transição
    with mlflow.start_run():
        mlflow.log_param("promoted_to", stage)
        mlflow.log_param("promoted_at", datetime.now().isoformat())
```

## Implantação

### 1. Preparação para Produção
```python
# src/models/production.py
import mlflow
import json

def prepare_for_production(model_name, version):
    # Carregar modelo
    model = mlflow.pyfunc.load_model(
        f"models:/{model_name}/{version}"
    )
    
    # Gerar schema do modelo
    input_schema = model.metadata.get_input_schema()
    output_schema = model.metadata.get_output_schema()
    
    # Salvar schemas
    schemas = {
        "input_schema": input_schema.to_dict(),
        "output_schema": output_schema.to_dict()
    }
    
    with open("model_schema.json", "w") as f:
        json.dump(schemas, f)
        
    # Logging de artefatos
    with mlflow.start_run():
        mlflow.log_artifact("model_schema.json")
```

### 2. Servindo Modelos
```python
# src/models/serve.py
import mlflow
from flask import Flask, request, jsonify

app = Flask(__name__)

def load_production_model(model_name):
    return mlflow.pyfunc.load_model(
        f"models:/{model_name}/Production"
    )

@app.route("/predict", methods=["POST"])
def predict():
    # Carregar dados
    data = request.json
    
    # Validar input
    if not validate_input(data):
        return jsonify({"error": "Invalid input"}), 400
    
    # Fazer predição
    model = load_production_model("my_model")
    prediction = model.predict(data)
    
    # Logging de predição
    with mlflow.start_run():
        mlflow.log_metric("predictions_made", 1)
    
    return jsonify({"prediction": prediction.tolist()})
```

## Monitoramento

### 1. Logging de Produção
```python
# src/monitoring/logging.py
import mlflow
import logging
from datetime import datetime

class ProductionLogger:
    def __init__(self):
        self.client = MlflowClient()
        
    def log_prediction(self, model_name, input_data, prediction):
        with mlflow.start_run():
            mlflow.log_dict(
                {
                    "timestamp": datetime.now().isoformat(),
                    "input": input_data,
                    "prediction": prediction
                },
                "predictions.json"
            )
    
    def log_error(self, error_msg):
        with mlflow.start_run():
            mlflow.log_param("error", error_msg)
            mlflow.log_metric("errors", 1)
```

### 2. Alertas
```python
# src/monitoring/alerts.py
import mlflow
import numpy as np
from datetime import datetime, timedelta

class ModelAlert:
    def __init__(self, threshold=0.1):
        self.threshold = threshold
        
    def check_drift(self, predictions, baseline):
        drift = np.mean(np.abs(predictions - baseline))
        
        if drift > self.threshold:
            self.send_alert(f"Drift detected: {drift}")
            
    def check_performance(self, metrics):
        if metrics["accuracy"] < 0.8:  # Exemplo
            self.send_alert("Performance degradation detected")
            
    def send_alert(self, message):
        with mlflow.start_run():
            mlflow.log_param("alert", message)
            mlflow.log_param("alert_time", datetime.now().isoformat())
```

## Exemplos de Uso

### 1. Pipeline Completo
```python
# Configurar ambiente
setup_tracking()
set_seed(42)
log_environment()

# Treinar modelo
model_metrics = train_model(data)

# Validar modelo
cross_val_metrics(model, X, y, config)

# Selecionar melhor modelo
best_model, best_run = select_best_model(experiment_id)

# Promover para produção
promote_model("my_model", "1", "Production")
```

### 2. Monitoramento
```python
# Inicializar monitores
logger = ProductionLogger()
alert = ModelAlert()

# Monitorar predições
predictions = model.predict(data)
logger.log_prediction("my_model", data, predictions)

# Verificar drift
alert.check_drift(predictions, baseline)
```

## Próximos Passos

1. [Segurança](../security/README.md)
2. [Escalabilidade](../scalability/README.md)
3. [Integração com Outras Ferramentas](../integrations/README.md)
