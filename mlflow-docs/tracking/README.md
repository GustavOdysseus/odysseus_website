# Sistema de Tracking do MLflow

## Visão Geral do Sistema de Tracking

O Sistema de Tracking do MLflow é o componente central para registro e monitoramento de experimentos de machine learning. Ele permite registrar parâmetros, métricas, artefatos e modelos de forma organizada e reproduzível.

## Componentes Principais

### 1. Cliente Principal (MlflowClient)

**Localização do Código:** [`/mlflow/tracking/client.py`](../mlflow/mlflow/tracking/client.py)

#### 1.1 Classe MlflowClient

A classe `MlflowClient` é a interface principal para interação com o MLflow. Ela fornece métodos para:
- Gerenciamento de experimentos
- Registro de execuções (runs)
- Controle de modelos
- Gerenciamento de artefatos

```python
class MlflowClient:
    def __init__(self, tracking_uri: Optional[str] = None, registry_uri: Optional[str] = None):
        """
        Argumentos:
            tracking_uri: Endereço do servidor de tracking
            registry_uri: Endereço do servidor de registro de modelos
        """
```

#### 1.2 Principais Métodos

##### Gerenciamento de Execuções (Runs)

1. **get_run** (Linha 181)
```python
def get_run(self, run_id: str) -> Run:
    """
    Recupera informações detalhadas de uma execução específica.
    
    Argumentos:
        run_id: Identificador único da execução
        
    Retorna:
        Objeto Run contendo metadados, parâmetros, tags e métricas
    """
```

2. **get_parent_run** (Linha 227)
```python
def get_parent_run(self, run_id: str) -> Optional[Run]:
    """
    Recupera a execução pai de uma execução aninhada.
    
    Argumentos:
        run_id: Identificador da execução filha
        
    Retorna:
        Objeto Run da execução pai, ou None se não existir
    """
```

### 2. Sistema de Armazenamento

O MLflow oferece diferentes backends para armazenamento de dados:
- FileStore: Armazenamento local em arquivo
- SQLAlchemy: Suporte a diversos bancos de dados
- REST: Comunicação com servidor remoto

## Exemplos Práticos

### Exemplo 1: Tracking Básico
```python
from mlflow import MlflowClient

# Inicializa o cliente
client = MlflowClient()

# Cria uma nova execução
run = client.create_run(experiment_id="0")

# Registra parâmetros e métricas
client.log_param(run.info.run_id, "param1", "valor1")
client.log_metric(run.info.run_id, "metrica1", 0.95)

# Finaliza a execução
client.set_terminated(run.info.run_id)
```

## Próximas Seções

1. [API Fluente](./fluent.md)
2. [Sistema de Armazenamento](./storage.md)
3. [Gerenciamento de Artefatos](./artifacts.md)
