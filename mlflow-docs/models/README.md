# Registro de Modelos no MLflow

## Visão Geral

O Registro de Modelos do MLflow é um componente centralizado para gerenciar o ciclo de vida completo dos modelos de machine learning, incluindo versionamento, estágios de transição e linhagem.

## Conceitos Principais

### 1. Modelo Registrado
- Representa uma linha de modelos com o mesmo nome
- Contém metadados e versões do modelo
- Permite transições de estágio (staging, production, archived)

### 2. Versão do Modelo
- Instância específica de um modelo registrado
- Inclui:
  - Código fonte
  - Ambiente
  - Artefatos
  - Métricas
  - Parâmetros

### 3. Estágios do Modelo
- **None**: Estado inicial
- **Staging**: Ambiente de teste
- **Production**: Ambiente de produção
- **Archived**: Modelos descontinuados

## Operações Básicas

### 1. Registrar um Modelo

```python
import mlflow
from sklearn.linear_model import LogisticRegression

# Treinar modelo
model = LogisticRegression()
model.fit(X_train, y_train)

# Registrar modelo
with mlflow.start_run():
    # Log do modelo
    mlflow.sklearn.log_model(
        model,
        "modelo",
        registered_model_name="modelo_classificacao"
    )
```

### 2. Carregar Modelo Registrado

```python
# Carregar versão específica
modelo = mlflow.pyfunc.load_model(
    model_uri=f"models:/modelo_classificacao/1"
)

# Carregar versão em produção
modelo = mlflow.pyfunc.load_model(
    model_uri=f"models:/modelo_classificacao/production"
)
```

### 3. Gerenciar Estágios

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Transição para produção
client.transition_model_version_stage(
    name="modelo_classificacao",
    version=1,
    stage="Production"
)

# Arquivar modelo
client.transition_model_version_stage(
    name="modelo_classificacao",
    version=1,
    stage="Archived"
)
```

## API do Registro de Modelos

### 1. Criar/Atualizar Modelos

```python
# Criar novo modelo registrado
client.create_registered_model("modelo_classificacao")

# Atualizar descrição
client.update_registered_model(
    name="modelo_classificacao",
    description="Modelo de classificação binária"
)
```

### 2. Gerenciar Versões

```python
# Criar nova versão
client.create_model_version(
    name="modelo_classificacao",
    source="runs:/run_id/modelo",
    run_id="run_id"
)

# Atualizar descrição da versão
client.update_model_version(
    name="modelo_classificacao",
    version=1,
    description="Versão inicial do modelo"
)
```

### 3. Buscar Modelos

```python
# Listar todos os modelos registrados
modelos = client.list_registered_models()

# Buscar versões específicas
versoes = client.get_latest_versions("modelo_classificacao", stages=["Production"])
```

## Exemplo Completo

```python
import mlflow
from mlflow.tracking import MlflowClient
from sklearn.linear_model import LogisticRegression
import pandas as pd

# Configurar tracking
mlflow.set_tracking_uri("http://localhost:5000")
client = MlflowClient()

# 1. Criar modelo registrado
try:
    client.create_registered_model("modelo_classificacao")
except:
    print("Modelo já existe")

# 2. Treinar e registrar nova versão
with mlflow.start_run() as run:
    # Treinar modelo
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Avaliar modelo
    score = model.score(X_test, y_test)
    
    # Log de métricas
    mlflow.log_metric("acuracia", score)
    
    # Registrar modelo
    result = mlflow.sklearn.log_model(
        model,
        "modelo",
        registered_model_name="modelo_classificacao"
    )

# 3. Atualizar metadados
client.update_model_version(
    name="modelo_classificacao",
    version=result.version,
    description=f"Modelo treinado em {pd.Timestamp.now()}"
)

# 4. Transição para staging
client.transition_model_version_stage(
    name="modelo_classificacao",
    version=result.version,
    stage="Staging"
)

# 5. Validação em staging
modelo_staging = mlflow.pyfunc.load_model(
    model_uri=f"models:/modelo_classificacao/staging"
)
score_staging = modelo_staging.predict(X_val)

# 6. Transição para produção (se aprovado)
if score_staging > 0.95:
    client.transition_model_version_stage(
        name="modelo_classificacao",
        version=result.version,
        stage="Production"
    )
```

## Boas Práticas

1. **Nomenclatura Consistente**
```python
# Use nomes descritivos e versionados
"modelo_classificacao_v2"
"modelo_regressao_2023"
```

2. **Documentação Detalhada**
```python
# Adicione descrições completas
client.update_registered_model(
    name="modelo_classificacao",
    description="""
    Modelo de classificação binária
    - Framework: scikit-learn
    - Algoritmo: LogisticRegression
    - Dataset: dados_2023_v1
    """
)
```

3. **Controle de Versão**
```python
# Mantenha apenas versões necessárias
client.delete_model_version(
    name="modelo_classificacao",
    version=1
)
```

4. **Automação de Transições**
```python
# Automatize transições baseadas em métricas
def avaliar_e_promover(modelo, versao, X_val, y_val, threshold=0.95):
    score = modelo.score(X_val, y_val)
    if score > threshold:
        client.transition_model_version_stage(
            name=modelo,
            version=versao,
            stage="Production"
        )
```

## Próximos Passos

1. [Implantação de Modelos](../deployment/README.md)
2. [Monitoramento](../monitoring/README.md)
3. [MLflow Projects](../projects/README.md)
