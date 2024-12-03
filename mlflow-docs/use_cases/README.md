# Casos de Uso do MLflow

Este documento apresenta casos de uso práticos do MLflow em diferentes cenários de machine learning.

## 1. Treinamento de Modelos

### 1.1 Treinamento Básico
```python
import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_basic_model():
    # Carregar dados
    data = pd.read_csv("data.csv")
    X = data.drop("target", axis=1)
    y = data["target"]
    
    # Split dados
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2
    )
    
    # Iniciar experimento
    with mlflow.start_run():
        # Treinar modelo
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        
        # Avaliar modelo
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Logging
        mlflow.log_param("n_estimators", model.n_estimators)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "model")
```

### 1.2 Treinamento Distribuído
```python
import mlflow
import ray
from ray import tune
from ray.tune.integration.mlflow import MLflowLoggerCallback

def train_distributed():
    ray.init()
    
    def training_function(config):
        # Configurar modelo
        model = RandomForestClassifier(**config)
        model.fit(X_train, y_train)
        
        # Avaliar
        accuracy = accuracy_score(
            y_test,
            model.predict(X_test)
        )
        
        # Reportar para Ray Tune
        tune.report(accuracy=accuracy)
    
    # Configurar busca
    analysis = tune.run(
        training_function,
        config={
            "n_estimators": tune.grid_search([10, 50, 100]),
            "max_depth": tune.grid_search([None, 10, 20])
        },
        callbacks=[MLflowLoggerCallback()]
    )
```

## 2. Servindo Modelos

### 2.1 API REST
```python
import mlflow.pyfunc
from flask import Flask, request, jsonify

app = Flask(__name__)

# Carregar modelo
model = mlflow.pyfunc.load_model("models:/my_model/Production")

@app.route("/predict", methods=["POST"])
def predict():
    # Receber dados
    data = request.json["data"]
    
    # Fazer predição
    predictions = model.predict(pd.DataFrame(data))
    
    return jsonify({"predictions": predictions.tolist()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### 2.2 Batch Inference
```python
import mlflow
import pandas as pd
from datetime import datetime

def batch_inference():
    # Carregar modelo
    model = mlflow.pyfunc.load_model(
        "models:/my_model/Production"
    )
    
    # Carregar dados
    data = pd.read_csv("batch_data.csv")
    
    # Fazer predições
    with mlflow.start_run():
        predictions = model.predict(data)
        
        # Salvar resultados
        results = pd.DataFrame({
            "id": data["id"],
            "prediction": predictions
        })
        
        # Logging
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results.to_csv(f"predictions_{timestamp}.csv")
        mlflow.log_artifact(f"predictions_{timestamp}.csv")
```

## 3. Monitoramento de Modelos

### 3.1 Performance Monitoring
```python
import mlflow
import pandas as pd
from sklearn.metrics import accuracy_score
import plotly.express as px

def monitor_performance():
    # Carregar modelo e dados
    model = mlflow.pyfunc.load_model(
        "models:/my_model/Production"
    )
    data = pd.read_csv("production_data.csv")
    
    # Calcular métricas
    with mlflow.start_run():
        predictions = model.predict(data.drop("target", axis=1))
        accuracy = accuracy_score(data["target"], predictions)
        
        # Criar visualização
        fig = px.line(
            x=data["date"],
            y=accuracy,
            title="Model Accuracy Over Time"
        )
        
        # Logging
        mlflow.log_metric("production_accuracy", accuracy)
        mlflow.log_figure(fig, "accuracy_plot.html")
```

### 3.2 Drift Detection
```python
import mlflow
import pandas as pd
from scipy.stats import ks_2samp

def detect_drift():
    # Carregar dados
    training_data = pd.read_csv("training_data.csv")
    production_data = pd.read_csv("production_data.csv")
    
    with mlflow.start_run():
        drift_scores = {}
        
        # Calcular drift para cada feature
        for column in training_data.columns:
            statistic, p_value = ks_2samp(
                training_data[column],
                production_data[column]
            )
            
            drift_scores[column] = {
                "statistic": statistic,
                "p_value": p_value
            }
        
        # Logging
        mlflow.log_dict(drift_scores, "drift_scores.json")
```

## 4. Otimização de Hiperparâmetros

### 4.1 Grid Search
```python
import mlflow
from sklearn.model_selection import GridSearchCV

def optimize_hyperparameters():
    # Definir grid
    param_grid = {
        "n_estimators": [10, 50, 100],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5, 10]
    }
    
    with mlflow.start_run():
        # Configurar busca
        model = RandomForestClassifier()
        grid_search = GridSearchCV(
            model,
            param_grid,
            cv=5,
            scoring="accuracy"
        )
        
        # Executar busca
        grid_search.fit(X_train, y_train)
        
        # Logging
        mlflow.log_params(grid_search.best_params_)
        mlflow.log_metric(
            "best_cv_score",
            grid_search.best_score_
        )
        mlflow.sklearn.log_model(
            grid_search.best_estimator_,
            "model"
        )
```

### 4.2 Bayesian Optimization
```python
import mlflow
import optuna

def objective(trial):
    # Definir espaço de busca
    params = {
        "n_estimators": trial.suggest_int(
            "n_estimators",
            10,
            100
        ),
        "max_depth": trial.suggest_int(
            "max_depth",
            5,
            30
        )
    }
    
    # Treinar modelo
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    
    # Avaliar
    accuracy = accuracy_score(
        y_test,
        model.predict(X_test)
    )
    
    return accuracy

def optimize_with_optuna():
    with mlflow.start_run():
        study = optuna.create_study(
            direction="maximize"
        )
        study.optimize(objective, n_trials=100)
        
        # Logging
        mlflow.log_params(study.best_params)
        mlflow.log_metric(
            "best_accuracy",
            study.best_value
        )
```

## 5. Pipelines de Produção

### 5.1 Airflow Pipeline
```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

def training_pipeline():
    dag = DAG(
        "ml_training",
        default_args={
            "owner": "data_science",
            "start_date": datetime(2024, 1, 1),
            "retries": 1,
            "retry_delay": timedelta(minutes=5)
        },
        schedule_interval="@daily"
    )
    
    # Preparar dados
    prepare_data = PythonOperator(
        task_id="prepare_data",
        python_callable=prepare_data_fn,
        dag=dag
    )
    
    # Treinar modelo
    train_model = PythonOperator(
        task_id="train_model",
        python_callable=train_model_fn,
        dag=dag
    )
    
    # Avaliar modelo
    evaluate_model = PythonOperator(
        task_id="evaluate_model",
        python_callable=evaluate_model_fn,
        dag=dag
    )
    
    # Definir dependências
    prepare_data >> train_model >> evaluate_model
    
    return dag
```

### 5.2 Kubeflow Pipeline
```python
import kfp
from kfp import dsl

@dsl.pipeline(
    name="Training Pipeline",
    description="End-to-end ML training pipeline"
)
def ml_pipeline():
    # Preparar dados
    prep_op = dsl.ContainerOp(
        name="prepare_data",
        image="data_prep_image",
        command=["python", "prepare.py"],
        file_outputs={"data": "/data.csv"}
    )
    
    # Treinar modelo
    train_op = dsl.ContainerOp(
        name="train_model",
        image="training_image",
        command=["python", "train.py"],
        arguments=["--data", prep_op.outputs["data"]],
        file_outputs={"model": "/model.pkl"}
    )
    
    # Avaliar modelo
    eval_op = dsl.ContainerOp(
        name="evaluate_model",
        image="eval_image",
        command=["python", "evaluate.py"],
        arguments=[
            "--model", train_op.outputs["model"],
            "--data", prep_op.outputs["data"]
        ]
    )
```

## Próximos Passos

1. [Monitoramento Avançado](../monitoring/advanced.md)
2. [Troubleshooting](../troubleshooting/README.md)
3. [Manutenção](../maintenance/README.md)
