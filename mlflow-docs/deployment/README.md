# Implantação de Modelos MLflow

## Visão Geral

O MLflow oferece várias opções para implantar modelos em produção, desde serviços locais até ambientes em nuvem. Esta documentação cobre os principais métodos de implantação e suas melhores práticas.

## Métodos de Implantação

### 1. MLflow Serving

O modo mais simples de servir um modelo MLflow localmente.

```bash
# Servir modelo local
mlflow models serve -m "models:/meu_modelo/production" -p 5001

# Servir com configurações específicas
mlflow models serve -m "models:/meu_modelo/production" \
    --host 0.0.0.0 \
    --port 5001 \
    --workers 4
```

#### Exemplo de Requisição
```python
import requests
import json

# Dados para previsão
data = {
    "columns": ["feature1", "feature2"],
    "data": [[1.0, 2.0], [3.0, 4.0]]
}

# Fazer requisição
response = requests.post(
    "http://localhost:5001/invocations",
    json=data,
    headers={"Content-Type": "application/json"}
)

predictions = response.json()
```

### 2. Docker Container

Criar e executar um container Docker com o modelo.

```bash
# Gerar Dockerfile
mlflow models generate-docker-context \
    -m "models:/meu_modelo/production" \
    -n "modelo-docker"

# Construir imagem
docker build -t meu_modelo:v1 modelo-docker

# Executar container
docker run -p 5001:8080 meu_modelo:v1
```

### 3. Implantação em Nuvem

#### AWS SageMaker
```python
import mlflow.sagemaker

# Configurar implantação
mlflow.sagemaker.deploy(
    app_name="meu-modelo-prod",
    model_uri="models:/meu_modelo/production",
    region_name="us-east-1",
    mode="create",
    instance_type="ml.m5.xlarge",
    instance_count=1
)
```

#### Azure ML
```python
import mlflow.azureml

# Configurar workspace
workspace = Workspace.from_config()

# Implantar modelo
mlflow.azureml.deploy(
    model_uri="models:/meu_modelo/production",
    workspace=workspace,
    deployment_config="deployment_config.json",
    service_name="meu-modelo-prod"
)
```

## Configurações Avançadas

### 1. Configuração de Ambiente

```python
# conda.yaml
channels:
  - conda-forge
dependencies:
  - python=3.8
  - scikit-learn
  - pandas
  - pip:
    - mlflow>=2.0.0
```

### 2. Configuração de Inferência

```python
# MLproject
name: meu_modelo

conda_env: conda.yaml

entry_points:
  main:
    parameters:
      data_path: path
      model_path: path
    command: "python train.py {data_path} {model_path}"
```

### 3. Configuração de Recursos

```python
# config.json
{
    "compute_target": "aks-cluster",
    "deployment_config": {
        "cpu_cores": 1,
        "memory_gb": 4,
        "enable_gpu": false
    },
    "inference_config": {
        "entry_script": "score.py",
        "runtime": "python",
        "conda_file": "conda.yaml"
    }
}
```

## Exemplo Completo: Pipeline de Implantação

```python
import mlflow
from mlflow.tracking import MlflowClient
import json
import requests

# 1. Configurar cliente
client = MlflowClient()

# 2. Carregar modelo da produção
model_name = "meu_modelo"
model_version = client.get_latest_versions(model_name, stages=["Production"])[0]

# 3. Preparar ambiente de implantação
deployment_config = {
    "name": "modelo-prod",
    "resources": {
        "cpu": "1",
        "memory": "2Gi"
    },
    "scaling": {
        "minReplicas": 1,
        "maxReplicas": 3,
        "targetCPUUtilizationPercentage": 80
    }
}

# 4. Implantar modelo
with open("deployment_config.json", "w") as f:
    json.dump(deployment_config, f)

# 5. Iniciar servidor
import subprocess
subprocess.Popen([
    "mlflow", "models", "serve",
    "-m", f"models:/{model_name}/production",
    "--port", "5001",
    "--workers", "4"
])

# 6. Função de teste
def test_endpoint(data):
    response = requests.post(
        "http://localhost:5001/invocations",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    return response.json()

# 7. Monitoramento básico
def check_health():
    try:
        response = requests.get("http://localhost:5001/health")
        return response.status_code == 200
    except:
        return False
```

## Boas Práticas

### 1. Versionamento
```python
# Sempre use tags específicas para containers
docker build -t meu_modelo:v1.2.3 .

# Mantenha histórico de implantações
client.create_deployment(
    name="modelo-prod",
    version="1.2.3",
    config=deployment_config
)
```

### 2. Monitoramento
```python
import prometheus_client

# Métricas de requisições
REQUEST_TIME = prometheus_client.Summary(
    'request_processing_seconds',
    'Time spent processing request'
)

# Métricas de predições
PREDICTION_HISTOGRAM = prometheus_client.Histogram(
    'prediction_values',
    'Distribution of prediction values'
)
```

### 3. Testes de Carga
```python
import locust

class ModelUser(locust.HttpUser):
    @locust.task
    def predict(self):
        self.client.post(
            "/invocations",
            json={
                "columns": ["feature1"],
                "data": [[1.0]]
            }
        )
```

### 4. Rollback
```python
# Script de rollback
def rollback_deployment(model_name, previous_version):
    client.transition_model_version_stage(
        name=model_name,
        version=previous_version,
        stage="Production"
    )
    
    # Reiniciar servidor
    subprocess.run(["docker", "restart", "modelo-container"])
```

## Próximos Passos

1. [Monitoramento em Produção](../monitoring/README.md)
2. [MLflow Projects](../projects/README.md)
3. [Integração Contínua](../ci_cd/README.md)
