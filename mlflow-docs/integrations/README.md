# Integração do MLflow com Outras Ferramentas

## Visão Geral

Este guia aborda as principais integrações do MLflow com outras ferramentas e frameworks populares de machine learning e MLOps.

## Frameworks de Deep Learning

### 1. PyTorch
```python
# src/integrations/pytorch_integration.py
import mlflow.pytorch
import torch
import torch.nn as nn
from typing import Dict, Any

class PyTorchIntegration:
    def __init__(self, model: nn.Module, config: Dict[str, Any]):
        self.model = model
        self.config = config
        
    def log_model(self, artifacts: Dict[str, Any] = None):
        with mlflow.start_run():
            # Log de hiperparâmetros
            mlflow.log_params(self.config)
            
            # Log do modelo
            mlflow.pytorch.log_model(
                self.model,
                "model",
                extra_files=artifacts
            )
            
    def load_model(self, run_id: str) -> nn.Module:
        # Carregar modelo
        model_uri = f"runs:/{run_id}/model"
        return mlflow.pytorch.load_model(model_uri)
```

### 2. TensorFlow/Keras
```python
# src/integrations/tensorflow_integration.py
import mlflow.tensorflow
import tensorflow as tf
from typing import Dict, Any

class TensorFlowIntegration:
    def __init__(self, model: tf.keras.Model, config: Dict[str, Any]):
        self.model = model
        self.config = config
        
    def log_model(self, custom_objects: Dict = None):
        with mlflow.start_run():
            # Log de hiperparâmetros
            mlflow.log_params(self.config)
            
            # Log do modelo
            mlflow.tensorflow.log_model(
                self.model,
                "model",
                custom_objects=custom_objects
            )
            
    def load_model(self, run_id: str) -> tf.keras.Model:
        # Carregar modelo
        model_uri = f"runs:/{run_id}/model"
        return mlflow.tensorflow.load_model(model_uri)
```

## Frameworks de Machine Learning

### 1. Scikit-learn
```python
# src/integrations/sklearn_integration.py
import mlflow.sklearn
from sklearn.base import BaseEstimator
from typing import Dict, Any

class SklearnIntegration:
    def __init__(self, model: BaseEstimator, config: Dict[str, Any]):
        self.model = model
        self.config = config
        
    def log_pipeline(self):
        with mlflow.start_run():
            # Log de hiperparâmetros
            mlflow.log_params(self.config)
            
            # Log do pipeline
            mlflow.sklearn.log_model(
                self.model,
                "model"
            )
            
    def load_pipeline(self, run_id: str) -> BaseEstimator:
        # Carregar pipeline
        model_uri = f"runs:/{run_id}/model"
        return mlflow.sklearn.load_model(model_uri)
```

### 2. XGBoost
```python
# src/integrations/xgboost_integration.py
import mlflow.xgboost
import xgboost as xgb
from typing import Dict, Any

class XGBoostIntegration:
    def __init__(self, model: xgb.Booster, config: Dict[str, Any]):
        self.model = model
        self.config = config
        
    def log_model(self):
        with mlflow.start_run():
            # Log de hiperparâmetros
            mlflow.log_params(self.config)
            
            # Log do modelo
            mlflow.xgboost.log_model(
                self.model,
                "model"
            )
            
    def load_model(self, run_id: str) -> xgb.Booster:
        # Carregar modelo
        model_uri = f"runs:/{run_id}/model"
        return mlflow.xgboost.load_model(model_uri)
```

## Ferramentas de Orquestração

### 1. Airflow
```python
# src/integrations/airflow_integration.py
from airflow import DAG
from airflow.operators.python import PythonOperator
import mlflow
from datetime import datetime
from typing import Dict, Any

class AirflowIntegration:
    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        
    def create_training_dag(
        self,
        dag_id: str,
        schedule: str,
        default_args: Dict[str, Any]
    ) -> DAG:
        dag = DAG(
            dag_id,
            schedule_interval=schedule,
            default_args=default_args,
            start_date=datetime(2024, 1, 1)
        )
        
        def _train_model(**context):
            mlflow.set_experiment(self.experiment_name)
            with mlflow.start_run():
                # Lógica de treinamento
                pass
                
        train_task = PythonOperator(
            task_id="train_model",
            python_callable=_train_model,
            dag=dag
        )
        
        return dag
```

### 2. Kubeflow
```python
# src/integrations/kubeflow_integration.py
import kfp
from kfp import dsl
import mlflow
from typing import Dict, Any

class KubeflowIntegration:
    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        
    @dsl.pipeline(
        name="MLflow Training Pipeline",
        description="Pipeline de treinamento com MLflow"
    )
    def create_training_pipeline(self, config: Dict[str, Any]):
        def train_op():
            mlflow.set_experiment(self.experiment_name)
            with mlflow.start_run():
                # Lógica de treinamento
                pass
                
        train_task = dsl.ContainerOp(
            name="train_model",
            image="mlflow-training:latest",
            command=["python", "-c"],
            arguments=[train_op]
        )
        
        return train_task
```

## Ferramentas de Monitoramento

### 1. Prometheus
```python
# src/integrations/prometheus_integration.py
from prometheus_client import Counter, Gauge, start_http_server
import mlflow
from typing import Dict, Any

class PrometheusIntegration:
    def __init__(self, port: int = 8000):
        self.port = port
        self.metrics = {
            "predictions": Counter(
                "model_predictions_total",
                "Total de predições realizadas"
            ),
            "latency": Gauge(
                "model_latency_seconds",
                "Latência das predições"
            )
        }
        
    def start_server(self):
        start_http_server(self.port)
        
    def log_prediction(self, latency: float):
        self.metrics["predictions"].inc()
        self.metrics["latency"].set(latency)
        
        with mlflow.start_run():
            mlflow.log_metric("prediction_latency", latency)
```

### 2. Grafana
```python
# src/integrations/grafana_integration.py
import mlflow
from grafanalib.core import Dashboard, Graph, Target
from typing import List, Dict, Any

class GrafanaIntegration:
    def __init__(self, dashboard_title: str):
        self.dashboard_title = dashboard_title
        
    def create_dashboard(self, metrics: List[str]) -> Dashboard:
        graphs = []
        
        for metric in metrics:
            target = Target(
                expr=f'mlflow_metric_{metric}',
                legendFormat=metric
            )
            
            graph = Graph(
                title=f"MLflow {metric}",
                targets=[target]
            )
            
            graphs.append(graph)
            
        return Dashboard(
            title=self.dashboard_title,
            rows=graphs
        )
```

## Ferramentas de Dados

### 1. Spark
```python
# src/integrations/spark_integration.py
import mlflow.spark
from pyspark.ml import Pipeline
from pyspark.sql import SparkSession
from typing import Dict, Any

class SparkIntegration:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.spark = SparkSession.builder.getOrCreate()
        
    def log_pipeline(self, pipeline: Pipeline):
        with mlflow.start_run():
            # Log de configurações
            mlflow.log_params(self.config)
            
            # Log do pipeline
            mlflow.spark.log_model(
                pipeline,
                "model"
            )
            
    def load_pipeline(self, run_id: str) -> Pipeline:
        # Carregar pipeline
        model_uri = f"runs:/{run_id}/model"
        return mlflow.spark.load_model(model_uri)
```

### 2. Dask
```python
# src/integrations/dask_integration.py
import mlflow
import dask.dataframe as dd
from typing import Dict, Any

class DaskIntegration:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def process_data(self, data: dd.DataFrame):
        with mlflow.start_run():
            # Log de configurações
            mlflow.log_params(self.config)
            
            # Processar dados
            results = data.compute()
            
            # Log de métricas
            mlflow.log_metric(
                "processed_rows",
                len(results)
            )
            
            return results
```

## Exemplos de Uso

### 1. Integração PyTorch + MLflow
```python
# Criar modelo PyTorch
model = nn.Sequential(
    nn.Linear(10, 5),
    nn.ReLU(),
    nn.Linear(5, 1)
)

# Configurar integração
config = {"lr": 0.01, "epochs": 10}
integration = PyTorchIntegration(model, config)

# Treinar e logar modelo
integration.log_model()

# Carregar modelo
loaded_model = integration.load_model("run_id")
```

### 2. Pipeline Airflow + MLflow
```python
# Configurar integração
integration = AirflowIntegration("experiment_name")

# Criar DAG
default_args = {
    "owner": "mlflow",
    "retries": 1
}

dag = integration.create_training_dag(
    "training_pipeline",
    "@daily",
    default_args
)
```

## Próximos Passos

1. [Manutenção](../maintenance/README.md)
2. [Monitoramento Avançado](../monitoring/advanced.md)
3. [Segurança](../security/README.md)
