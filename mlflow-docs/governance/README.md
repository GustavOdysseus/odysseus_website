# Governança de Modelos com MLflow

## Visão Geral

A governança de modelos é um conjunto de práticas e políticas que garantem a qualidade, confiabilidade e conformidade dos modelos de machine learning. O MLflow fornece ferramentas poderosas para implementar uma estrutura robusta de governança.

## Componentes Principais

### 1. Registro de Modelos
```python
# src/model_registry.py
import mlflow
from mlflow.tracking import MlflowClient

class ModelRegistry:
    def __init__(self):
        self.client = MlflowClient()
        
    def register_model(self, run_id, model_name):
        # Registrar modelo
        model_uri = f"runs:/{run_id}/model"
        model_version = mlflow.register_model(
            model_uri,
            model_name
        )
        
        return model_version
        
    def transition_model(self, model_name, version, stage):
        # Transicionar modelo para novo estágio
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage
        )
        
    def get_latest_versions(self, model_name):
        # Obter últimas versões
        return self.client.get_latest_versions(model_name)
```

### 2. Políticas de Aprovação
```python
# src/approval_policies.py
import mlflow
from datetime import datetime

class ApprovalPolicy:
    def __init__(self, min_accuracy=0.8, max_drift=0.1):
        self.min_accuracy = min_accuracy
        self.max_drift = max_drift
        
    def check_metrics(self, run_id):
        run = mlflow.get_run(run_id)
        metrics = run.data.metrics
        
        # Verificar métricas mínimas
        if metrics.get("accuracy", 0) < self.min_accuracy:
            return False, "Accuracy below threshold"
            
        if metrics.get("drift_score", 0) > self.max_drift:
            return False, "Data drift too high"
            
        return True, "All checks passed"
        
    def approve_model(self, model_name, version):
        # Aprovar modelo
        with mlflow.start_run():
            mlflow.log_param("approved_by", "approval_policy")
            mlflow.log_param("approved_at", datetime.now().isoformat())
            
            return self.client.update_model_version(
                name=model_name,
                version=version,
                description="Approved by automated policy"
            )
```

### 3. Auditoria
```python
# src/audit.py
import mlflow
import pandas as pd
from datetime import datetime

class ModelAudit:
    def __init__(self):
        self.client = MlflowClient()
        
    def get_model_lineage(self, model_name, version):
        # Obter histórico do modelo
        model_version = self.client.get_model_version(
            name=model_name,
            version=version
        )
        
        run = mlflow.get_run(model_version.run_id)
        
        return {
            "training_date": run.info.start_time,
            "parameters": run.data.params,
            "metrics": run.data.metrics,
            "artifacts": run.info.artifact_uri
        }
        
    def export_audit_report(self, model_name):
        # Gerar relatório de auditoria
        versions = self.client.search_model_versions(f"name='{model_name}'")
        
        audit_data = []
        for version in versions:
            lineage = self.get_model_lineage(model_name, version.version)
            audit_data.append({
                "version": version.version,
                "stage": version.current_stage,
                **lineage
            })
            
        report = pd.DataFrame(audit_data)
        report.to_csv(f"audit_{model_name}_{datetime.now()}.csv")
        return report
```

### 4. Controle de Acesso
```python
# src/access_control.py
import mlflow
from functools import wraps

class AccessControl:
    def __init__(self):
        self.roles = {
            "admin": ["register", "transition", "delete"],
            "data_scientist": ["register", "transition"],
            "viewer": ["view"]
        }
        
    def check_permission(self, user, action):
        user_role = self.get_user_role(user)
        return action in self.roles.get(user_role, [])
        
    def require_permission(action):
        def decorator(f):
            @wraps(f)
            def wrapped(self, *args, **kwargs):
                user = mlflow.get_user()
                if not self.check_permission(user, action):
                    raise PermissionError(f"User {user} not authorized for {action}")
                return f(self, *args, **kwargs)
            return wrapped
        return decorator
        
    @require_permission("register")
    def register_model(self, *args, **kwargs):
        # Implementação do registro
        pass
        
    @require_permission("transition")
    def transition_model(self, *args, **kwargs):
        # Implementação da transição
        pass
```

## Políticas e Procedimentos

### 1. Ciclo de Vida do Modelo
```python
# src/model_lifecycle.py
from enum import Enum

class ModelStage(Enum):
    DEVELOPMENT = "Development"
    STAGING = "Staging"
    PRODUCTION = "Production"
    ARCHIVED = "Archived"

class ModelLifecycle:
    def __init__(self):
        self.registry = ModelRegistry()
        self.approval = ApprovalPolicy()
        
    def promote_to_staging(self, model_name, version):
        # Verificar métricas
        approved, message = self.approval.check_metrics(version)
        
        if approved:
            self.registry.transition_model(
                model_name,
                version,
                ModelStage.STAGING.value
            )
            
    def promote_to_production(self, model_name, version):
        # Verificar aprovação
        if not self.approval.is_approved(model_name, version):
            raise ValueError("Model not approved for production")
            
        # Arquivar versão atual em produção
        current = self.registry.get_latest_versions(
            model_name,
            stages=[ModelStage.PRODUCTION.value]
        )
        
        if current:
            self.registry.transition_model(
                model_name,
                current[0].version,
                ModelStage.ARCHIVED.value
            )
            
        # Promover nova versão
        self.registry.transition_model(
            model_name,
            version,
            ModelStage.PRODUCTION.value
        )
```

### 2. Documentação Obrigatória
```python
# src/model_documentation.py
import mlflow
import yaml

class ModelDocumentation:
    def __init__(self):
        self.required_fields = [
            "purpose",
            "input_schema",
            "output_schema",
            "training_data",
            "performance_metrics",
            "limitations"
        ]
        
    def validate_documentation(self, doc_path):
        with open(doc_path) as f:
            doc = yaml.safe_load(f)
            
        missing = [
            field for field in self.required_fields
            if field not in doc
        ]
        
        if missing:
            raise ValueError(f"Missing required fields: {missing}")
            
        return True
        
    def log_documentation(self, run_id, doc_path):
        if self.validate_documentation(doc_path):
            with mlflow.start_run(run_id=run_id):
                mlflow.log_artifact(
                    doc_path,
                    artifact_path="documentation"
                )
```

### 3. Monitoramento de Compliance
```python
# src/compliance.py
import mlflow
import json
from datetime import datetime

class ComplianceMonitor:
    def __init__(self):
        self.client = MlflowClient()
        
    def check_compliance(self, model_name, version):
        # Verificar documentação
        model_version = self.client.get_model_version(
            name=model_name,
            version=version
        )
        
        run = mlflow.get_run(model_version.run_id)
        artifacts = self.client.list_artifacts(run.info.run_id)
        
        compliance_checks = {
            "has_documentation": any(
                a.path == "documentation/model_card.yaml"
                for a in artifacts
            ),
            "has_validation": any(
                a.path == "validation/report.txt"
                for a in artifacts
            ),
            "has_approval": model_version.description.startswith("Approved")
        }
        
        # Logging de resultados
        with mlflow.start_run():
            mlflow.log_dict(
                compliance_checks,
                "compliance_report.json"
            )
            
        return all(compliance_checks.values())
```

## Melhores Práticas

### 1. Versionamento
```python
# src/versioning.py
import mlflow
import semver

class ModelVersioning:
    def __init__(self):
        self.client = MlflowClient()
        
    def get_next_version(self, model_name):
        versions = self.client.search_model_versions(
            f"name='{model_name}'"
        )
        
        if not versions:
            return "1.0.0"
            
        latest = max(
            versions,
            key=lambda v: semver.VersionInfo.parse(v.version)
        )
        
        current = semver.VersionInfo.parse(latest.version)
        return str(current.bump_minor())
        
    def tag_version(self, model_name, version, tags):
        self.client.set_model_version_tag(
            name=model_name,
            version=version,
            key="semantic_version",
            value=self.get_next_version(model_name)
        )
```

### 2. Documentação de Decisões
```python
# src/decision_log.py
import mlflow
from datetime import datetime

class DecisionLog:
    def __init__(self):
        self.client = MlflowClient()
        
    def log_decision(self, model_name, version, decision, reason):
        decision_log = {
            "timestamp": datetime.now().isoformat(),
            "model_name": model_name,
            "version": version,
            "decision": decision,
            "reason": reason
        }
        
        with mlflow.start_run():
            mlflow.log_dict(
                decision_log,
                "decisions/decision_log.json"
            )
```

### 3. Revisão de Código
```python
# src/code_review.py
import mlflow
import git

class CodeReview:
    def __init__(self):
        self.repo = git.Repo(".")
        
    def log_code_version(self, run_id):
        with mlflow.start_run(run_id=run_id):
            mlflow.log_param("git_commit", self.repo.head.commit.hexsha)
            mlflow.log_param("git_branch", self.repo.active_branch.name)
            
    def log_review_status(self, run_id, reviewer, status):
        with mlflow.start_run(run_id=run_id):
            mlflow.log_param("code_reviewer", reviewer)
            mlflow.log_param("review_status", status)
            mlflow.log_param("review_date", datetime.now().isoformat())
```

## Exemplos de Uso

### 1. Pipeline de Governança
```python
# Inicializar componentes
lifecycle = ModelLifecycle()
documentation = ModelDocumentation()
compliance = ComplianceMonitor()

# Registrar e promover modelo
model_version = lifecycle.registry.register_model(run_id, "my_model")
documentation.log_documentation(run_id, "docs/model_card.yaml")

if compliance.check_compliance("my_model", model_version.version):
    lifecycle.promote_to_staging("my_model", model_version.version)
```

### 2. Auditoria
```python
# Gerar relatório de auditoria
auditor = ModelAudit()
report = auditor.export_audit_report("my_model")

# Verificar compliance
monitor = ComplianceMonitor()
is_compliant = monitor.check_compliance("my_model", "1")
```

## Próximos Passos

1. [Melhores Práticas](../best_practices/README.md)
2. [Monitoramento](../monitoring/README.md)
3. [Segurança](../security/README.md)

# Governança de Modelos no MLflow

Este documento descreve as práticas e ferramentas para governança de modelos no MLflow.

## 1. Registro de Modelos

### 1.1 Versionamento
```python
import mlflow
from mlflow.tracking import MlflowClient

def register_model_version():
    client = MlflowClient()
    
    with mlflow.start_run():
        # Treinar e registrar modelo
        model = train_model()
        
        # Registrar nova versão
        result = mlflow.register_model(
            "runs:/run_id/model",
            "my_model"
        )
        
        # Adicionar descrição
        client.update_model_version(
            name="my_model",
            version=result.version,
            description="Modelo treinado em 01/01/2024"
        )
```

### 1.2 Transições de Estágio
```python
def transition_model_stage():
    client = MlflowClient()
    
    # Transicionar para staging
    client.transition_model_version_stage(
        name="my_model",
        version=1,
        stage="Staging"
    )
    
    # Validar modelo
    if validate_model():
        # Promover para produção
        client.transition_model_version_stage(
            name="my_model",
            version=1,
            stage="Production"
        )
```

## 2. Documentação de Modelos

### 2.1 Metadados
```python
def document_model():
    with mlflow.start_run():
        # Adicionar tags
        mlflow.set_tags({
            "team": "data_science",
            "project": "churn_prediction",
            "framework": "sklearn",
            "python_version": "3.8"
        })
        
        # Adicionar descrição
        mlflow.set_tag(
            "description",
            "Modelo de previsão de churn usando Random Forest"
        )
        
        # Logging de requisitos
        mlflow.log_artifact(
            "requirements.txt",
            "dependencies"
        )
```

### 2.2 Cartão de Modelo
```python
from mlflow.models import ModelCard, ModelCardData

def create_model_card():
    card_data = ModelCardData(
        name="Churn Prediction Model",
        version="1.0.0",
        authors=["Data Science Team"],
        use_cases="Previsão de churn de clientes",
        limitations="Não adequado para clientes novos",
        ethical_considerations="Não usa dados sensíveis",
        metrics={
            "accuracy": 0.85,
            "precision": 0.82,
            "recall": 0.78
        }
    )
    
    card = ModelCard(card_data)
    
    with mlflow.start_run():
        mlflow.log_dict(
            card.to_dict(),
            "model_card.json"
        )
```

## 3. Políticas de Governança

### 3.1 Validação de Modelos
```python
def validate_model():
    # Carregar modelo
    model = mlflow.pyfunc.load_model(
        "models:/my_model/Staging"
    )
    
    # Validar performance
    metrics = evaluate_model(model)
    
    # Verificar critérios
    if metrics["accuracy"] < 0.8:
        raise ValueError("Accuracy abaixo do threshold")
        
    if metrics["latency"] > 100:
        raise ValueError("Latência muito alta")
        
    return True

def evaluate_model(model):
    # Carregar dados de validação
    data = load_validation_data()
    
    # Calcular métricas
    predictions = model.predict(data.drop("target", axis=1))
    metrics = calculate_metrics(data["target"], predictions)
    
    return metrics
```

### 3.2 Aprovação de Modelos
```python
from typing import List, Dict
import datetime

class ModelApproval:
    def __init__(self, required_approvers: List[str]):
        self.required_approvers = required_approvers
        self.approvals = {}
        
    def approve_model(
        self,
        model_name: str,
        version: int,
        approver: str,
        comments: str = ""
    ):
        if approver not in self.required_approvers:
            raise ValueError("Approver não autorizado")
            
        self.approvals[approver] = {
            "timestamp": datetime.datetime.now(),
            "comments": comments
        }
        
    def check_approval_status(
        self,
        model_name: str,
        version: int
    ) -> Dict:
        missing_approvers = set(self.required_approvers) - set(self.approvals.keys())
        
        return {
            "approved": len(missing_approvers) == 0,
            "missing_approvers": list(missing_approvers),
            "approvals": self.approvals
        }
```

## 4. Auditoria de Modelos

### 4.1 Logging de Eventos
```python
def log_model_event(
    model_name: str,
    version: int,
    event_type: str,
    details: Dict
):
    with mlflow.start_run():
        mlflow.log_dict(
            {
                "timestamp": datetime.datetime.now().isoformat(),
                "model_name": model_name,
                "version": version,
                "event_type": event_type,
                "details": details
            },
            f"events/{event_type}.json"
        )
```

### 4.2 Relatórios de Auditoria
```python
def generate_audit_report(
    model_name: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime
) -> Dict:
    client = MlflowClient()
    
    # Buscar versões do modelo
    versions = client.search_model_versions(
        f"name = '{model_name}'"
    )
    
    report = {
        "model_name": model_name,
        "period": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        },
        "versions": []
    }
    
    for version in versions:
        # Filtrar por período
        creation_time = datetime.datetime.fromtimestamp(
            version.creation_timestamp / 1000.0
        )
        
        if start_date <= creation_time <= end_date:
            report["versions"].append({
                "version": version.version,
                "stage": version.current_stage,
                "creator": version.user_id,
                "creation_time": creation_time.isoformat()
            })
    
    return report
```

## 5. Conformidade

### 5.1 Verificação de Conformidade
```python
def check_compliance(
    model_name: str,
    version: int
) -> Dict[str, bool]:
    client = MlflowClient()
    version = client.get_model_version(
        model_name,
        version
    )
    
    checks = {
        "has_description": bool(version.description),
        "has_model_card": check_model_card(version),
        "has_requirements": check_requirements(version),
        "has_tests": check_tests(version),
        "has_approvals": check_approvals(version)
    }
    
    return checks

def enforce_compliance(
    model_name: str,
    version: int
):
    checks = check_compliance(model_name, version)
    
    if not all(checks.values()):
        raise ValueError(
            f"Modelo não conforme: {checks}"
        )
```

### 5.2 Documentação de Conformidade
```python
def document_compliance(
    model_name: str,
    version: int,
    checks: Dict[str, bool]
):
    with mlflow.start_run():
        mlflow.log_dict(
            {
                "timestamp": datetime.datetime.now().isoformat(),
                "model_name": model_name,
                "version": version,
                "compliance_checks": checks,
                "compliant": all(checks.values())
            },
            "compliance/report.json"
        )
```

## Próximos Passos

1. [Monitoramento Avançado](../monitoring/advanced.md)
2. [Troubleshooting](../troubleshooting/README.md)
3. [Manutenção](../maintenance/README.md)
