# API Fluente do MLflow

## Introdução

A API fluente do MLflow oferece uma interface mais simples e intuitiva para tracking de experimentos, comparada com a API do cliente. Esta API é implementada no módulo `mlflow.fluent`.

## Principais Funcionalidades

### 1. Gerenciamento de Experimentos

```python
import mlflow

# Criar ou obter um experimento
mlflow.set_experiment("nome_do_experimento")

# Iniciar uma nova execução
with mlflow.start_run() as run:
    # Seu código aqui
    pass
```

### 2. Logging de Parâmetros e Métricas

#### 2.1 Parâmetros
```python
# Registrar parâmetros individuais
mlflow.log_param("learning_rate", 0.01)
mlflow.log_param("batch_size", 32)

# Registrar múltiplos parâmetros
params = {"alpha": 0.5, "l1_ratio": 0.1}
mlflow.log_params(params)
```

#### 2.2 Métricas
```python
# Registrar métricas individuais
mlflow.log_metric("acuracia", 0.95)
mlflow.log_metric("loss", 0.1)

# Registrar métricas com passo (step)
for epoch in range(10):
    mlflow.log_metric("loss", loss_value, step=epoch)
```

### 3. Artefatos

```python
# Salvar um arquivo como artefato
mlflow.log_artifact("modelo.pkl")

# Salvar um diretório inteiro
mlflow.log_artifacts("./resultados")
```

## Exemplo Completo

```python
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Configurar o experimento
mlflow.set_experiment("Classificação")

# Carregar dados
X, y = load_data()
X_train, X_test, y_train, y_test = train_test_split(X, y)

# Iniciar uma execução do MLflow
with mlflow.start_run(run_name="modelo_base"):
    # Definir parâmetros
    params = {
        "solver": "lbfgs",
        "max_iter": 1000
    }
    
    # Criar e treinar o modelo
    model = LogisticRegression(**params)
    model.fit(X_train, y_train)
    
    # Calcular métricas
    score = model.score(X_test, y_test)
    
    # Logging de parâmetros e métricas
    mlflow.log_params(params)
    mlflow.log_metric("acuracia", score)
    
    # Salvar o modelo
    mlflow.sklearn.log_model(model, "modelo")
```

## Boas Práticas

1. **Sempre use contextos `with`**
   ```python
   with mlflow.start_run():
       # seu código aqui
   ```

2. **Organize experimentos logicamente**
   ```python
   mlflow.set_experiment(f"{modelo}_{dataset}_{versao}")
   ```

3. **Documente parâmetros importantes**
   ```python
   mlflow.set_tag("descrição", "Experimento base com LogisticRegression")
   ```

4. **Versione seus dados**
   ```python
   mlflow.log_param("versao_dados", "v1.2.3")
   ```

## Integração com Frameworks Populares

O MLflow oferece integrações nativas com vários frameworks populares:

- **scikit-learn**
  ```python
  mlflow.sklearn.log_model(model, "modelo")
  ```

- **PyTorch**
  ```python
  mlflow.pytorch.log_model(model, "modelo")
  ```

- **TensorFlow/Keras**
  ```python
  mlflow.tensorflow.log_model(model, "modelo")
  ```

## Próximos Passos

1. [Sistema de Armazenamento](./storage.md)
2. [Gerenciamento de Artefatos](./artifacts.md)
3. [Registro de Modelos](../models/README.md)
