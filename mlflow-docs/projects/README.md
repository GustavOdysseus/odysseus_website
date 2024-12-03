# MLflow Projects

## Visão Geral

MLflow Projects é um formato padronizado para empacotamento de código de ciência de dados que permite reprodutibilidade e compartilhamento. Ele define convenções para organizar e descrever seu código para que outros cientistas de dados possam executá-lo.

## Estrutura do Projeto

### 1. Arquivo MLproject
```yaml
name: meu_projeto

conda_env: conda.yaml

entry_points:
  main:
    parameters:
      alpha: {type: float, default: 0.5}
      l1_ratio: {type: float, default: 0.1}
    command: "python train.py --alpha {alpha} --l1_ratio {l1_ratio}"
    
  validate:
    parameters:
      data_path: path
    command: "python validate.py --data_path {data_path}"
```

### 2. Ambiente Conda
```yaml
# conda.yaml
name: mlflow-env
channels:
  - conda-forge
dependencies:
  - python=3.8
  - pip
  - scikit-learn
  - pandas
  - pip:
    - mlflow>=2.0.0
    - pytest>=7.0.0
```

### 3. Estrutura de Diretórios
```
meu_projeto/
├── MLproject
├── conda.yaml
├── README.md
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── exploratory.ipynb
├── src/
│   ├── __init__.py
│   ├── train.py
│   └── validate.py
└── tests/
    └── test_model.py
```

## Componentes Principais

### 1. Script de Treinamento
```python
# train.py
import argparse
import mlflow

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--l1_ratio", type=float, default=0.1)
    return parser.parse_args()

def main():
    args = parse_args()
    
    with mlflow.start_run():
        # Logging de parâmetros
        mlflow.log_params({
            "alpha": args.alpha,
            "l1_ratio": args.l1_ratio
        })
        
        # Treinar modelo
        model = train_model(args.alpha, args.l1_ratio)
        
        # Salvar modelo
        mlflow.sklearn.log_model(model, "modelo")

if __name__ == "__main__":
    main()
```

### 2. Script de Validação
```python
# validate.py
import argparse
import mlflow

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, required=True)
    return parser.parse_args()

def main():
    args = parse_args()
    
    with mlflow.start_run():
        # Carregar dados
        data = load_data(args.data_path)
        
        # Carregar modelo
        model = mlflow.sklearn.load_model("modelo")
        
        # Validar modelo
        score = validate_model(model, data)
        
        # Logging de métricas
        mlflow.log_metric("validation_score", score)

if __name__ == "__main__":
    main()
```

## Execução de Projetos

### 1. Local
```bash
# Executar projeto local
mlflow run . -P alpha=0.1 -P l1_ratio=0.2

# Executar entry point específico
mlflow run . -e validate -P data_path=data/test.csv
```

### 2. Git
```bash
# Executar projeto do GitHub
mlflow run https://github.com/usuario/projeto.git -P alpha=0.1

# Executar versão específica
mlflow run https://github.com/usuario/projeto.git -v master
```

### 3. Docker
```bash
# Executar em container Docker
mlflow run . --docker-args gpus=all
```

## Exemplo Completo

### 1. Estrutura do Projeto
```
projeto_ml/
├── MLproject
├── conda.yaml
├── README.md
├── src/
│   ├── train.py
│   ├── validate.py
│   └── utils.py
└── tests/
    └── test_model.py
```

### 2. MLproject
```yaml
name: projeto_ml

conda_env: conda.yaml

entry_points:
  train:
    parameters:
      data_path: path
      num_trees: {type: int, default: 100}
      max_depth: {type: int, default: 10}
    command: "python src/train.py --data_path {data_path} --num_trees {num_trees} --max_depth {max_depth}"
    
  validate:
    parameters:
      model_path: path
      data_path: path
    command: "python src/validate.py --model_path {model_path} --data_path {data_path}"
    
  pipeline:
    parameters:
      data_path: path
      num_trees: {type: int, default: 100}
    command: "python src/pipeline.py --data_path {data_path} --num_trees {num_trees}"
```

### 3. Pipeline Completo
```python
# src/pipeline.py
import mlflow
import argparse
from sklearn.model_selection import train_test_split

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, required=True)
    parser.add_argument("--num_trees", type=int, default=100)
    return parser.parse_args()

def main():
    args = parse_args()
    
    # 1. Carregar e preparar dados
    data = load_data(args.data_path)
    X_train, X_test, y_train, y_test = train_test_split(
        data.drop("target", axis=1),
        data["target"]
    )
    
    # 2. Treinar modelo
    with mlflow.start_run() as run:
        # Configurar experimento
        mlflow.set_experiment("projeto_ml")
        
        # Logging de parâmetros
        mlflow.log_params({
            "num_trees": args.num_trees,
            "data_path": args.data_path
        })
        
        # Treinar modelo
        model = RandomForestClassifier(n_estimators=args.num_trees)
        model.fit(X_train, y_train)
        
        # Avaliar modelo
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        # Logging de métricas
        mlflow.log_metrics({
            "train_score": train_score,
            "test_score": test_score
        })
        
        # Salvar modelo
        mlflow.sklearn.log_model(model, "modelo")
        
        # Salvar artefatos importantes
        plot_importance(model)
        mlflow.log_artifact("feature_importance.png")
        
        # Retornar ID da execução
        run_id = run.info.run_id
    
    # 3. Validar modelo
    with mlflow.start_run(run_id=run_id, nested=True):
        validation_score = validate_model(
            model,
            X_test,
            y_test
        )
        
        mlflow.log_metric("validation_score", validation_score)

if __name__ == "__main__":
    main()
```

## Boas Práticas

### 1. Organização do Código
```python
# Separar código em módulos lógicos
src/
├── data/          # Processamento de dados
├── features/      # Engenharia de features
├── models/        # Definições de modelos
└── evaluation/    # Métricas e validação
```

### 2. Documentação
```markdown
# README.md
## Projeto ML

### Requisitos
- Python 3.8+
- MLflow 2.0.0+
- scikit-learn

### Uso
```bash
mlflow run . -P data_path=data/train.csv -P num_trees=100
```

### Parâmetros
- data_path: Caminho para dados de treino
- num_trees: Número de árvores (default: 100)
```

### 3. Testes
```python
# tests/test_model.py
import pytest
from src.models import train_model

def test_model_training():
    model = train_model(num_trees=10)
    assert model is not None
    assert hasattr(model, 'predict')
```

### 4. Logging
```python
# src/utils.py
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

logger = setup_logging()
```

## Próximos Passos

1. [Integração Contínua](../ci_cd/README.md)
2. [Governança de Modelos](../governance/README.md)
3. [Melhores Práticas](../best_practices/README.md)
