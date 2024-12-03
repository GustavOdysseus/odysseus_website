# Monitoramento Avançado do MLflow

## Visão Geral

Este guia aborda técnicas avançadas de monitoramento para ambientes MLflow, incluindo métricas de performance, detecção de anomalias, alertas e visualizações.

## Métricas de Performance

### 1. Métricas do Sistema
```python
# src/monitoring/system_metrics.py
import psutil
import time
import mlflow
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SystemMetrics:
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: Dict[str, int]
    process_count: int

class SystemMonitor:
    def __init__(self, interval: int = 60):
        self.interval = interval
        
    def collect_metrics(self) -> SystemMetrics:
        return SystemMetrics(
            cpu_percent=psutil.cpu_percent(),
            memory_percent=psutil.virtual_memory().percent,
            disk_percent=psutil.disk_usage('/').percent,
            network_io={
                'bytes_sent': psutil.net_io_counters().bytes_sent,
                'bytes_recv': psutil.net_io_counters().bytes_recv
            },
            process_count=len(psutil.pids())
        )
        
    def log_metrics(self):
        metrics = self.collect_metrics()
        with mlflow.start_run():
            mlflow.log_metrics({
                'system.cpu': metrics.cpu_percent,
                'system.memory': metrics.memory_percent,
                'system.disk': metrics.disk_percent,
                'system.network.sent': metrics.network_io['bytes_sent'],
                'system.network.recv': metrics.network_io['bytes_recv'],
                'system.processes': metrics.process_count
            })
```

### 2. Métricas de Aplicação
```python
# src/monitoring/app_metrics.py
import mlflow
import time
from typing import Dict, Any, List
from prometheus_client import Counter, Histogram

class MLflowMetrics:
    def __init__(self):
        # Contadores Prometheus
        self.model_predictions = Counter(
            'mlflow_model_predictions_total',
            'Total de predições realizadas'
        )
        self.prediction_latency = Histogram(
            'mlflow_prediction_latency_seconds',
            'Latência das predições'
        )
        
    def log_prediction(self, model_name: str, latency: float):
        self.model_predictions.inc()
        self.prediction_latency.observe(latency)
        
        with mlflow.start_run():
            mlflow.log_metrics({
                'prediction_count': 1,
                'prediction_latency': latency
            })
            
    def get_prediction_stats(self) -> Dict[str, float]:
        return {
            'total_predictions': self.model_predictions._value.get(),
            'avg_latency': self.prediction_latency._sum.get() / 
                         self.prediction_latency._count.get()
        }
```

## Detecção de Anomalias

### 1. Monitoramento de Drift
```python
# src/monitoring/drift.py
import numpy as np
from scipy import stats
from typing import Dict, Any, List
import mlflow

class DriftDetector:
    def __init__(self, baseline_data: np.ndarray):
        self.baseline_data = baseline_data
        self.baseline_stats = self._compute_stats(baseline_data)
        
    def _compute_stats(self, data: np.ndarray) -> Dict[str, float]:
        return {
            'mean': np.mean(data),
            'std': np.std(data),
            'skew': stats.skew(data),
            'kurtosis': stats.kurtosis(data)
        }
        
    def detect_drift(
        self,
        current_data: np.ndarray,
        threshold: float = 0.05
    ) -> Dict[str, Any]:
        current_stats = self._compute_stats(current_data)
        
        # Teste KS para drift
        ks_statistic, p_value = stats.ks_2samp(
            self.baseline_data,
            current_data
        )
        
        drift_detected = p_value < threshold
        
        with mlflow.start_run():
            mlflow.log_metrics({
                'drift.ks_statistic': ks_statistic,
                'drift.p_value': p_value
            })
            
        return {
            'drift_detected': drift_detected,
            'p_value': p_value,
            'baseline_stats': self.baseline_stats,
            'current_stats': current_stats
        }
```

### 2. Detecção de Outliers
```python
# src/monitoring/outliers.py
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict, Any, List
import mlflow

class OutlierDetector:
    def __init__(self, contamination: float = 0.1):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42
        )
        
    def fit(self, data: np.ndarray):
        self.model.fit(data)
        
    def detect_outliers(
        self,
        data: np.ndarray
    ) -> Dict[str, Any]:
        # Detectar outliers
        predictions = self.model.predict(data)
        outlier_mask = predictions == -1
        
        outlier_indices = np.where(outlier_mask)[0]
        outlier_scores = self.model.score_samples(data)
        
        with mlflow.start_run():
            mlflow.log_metrics({
                'outliers.count': len(outlier_indices),
                'outliers.ratio': len(outlier_indices) / len(data)
            })
            
        return {
            'outlier_indices': outlier_indices,
            'outlier_scores': outlier_scores[outlier_mask],
            'total_outliers': len(outlier_indices)
        }
```

## Sistema de Alertas

### 1. Configuração de Alertas
```python
# src/monitoring/alerts.py
import smtplib
import requests
from typing import Dict, Any, List
import logging

class AlertSystem:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def send_email_alert(
        self,
        subject: str,
        message: str,
        recipients: List[str]
    ):
        try:
            with smtplib.SMTP(self.config['smtp_server']) as server:
                server.starttls()
                server.login(
                    self.config['smtp_user'],
                    self.config['smtp_password']
                )
                
                email_text = f"Subject: {subject}\n\n{message}"
                server.sendmail(
                    self.config['smtp_user'],
                    recipients,
                    email_text
                )
        except Exception as e:
            self.logger.error(f"Erro ao enviar email: {e}")
            
    def send_slack_alert(self, message: str):
        try:
            requests.post(
                self.config['slack_webhook_url'],
                json={'text': message}
            )
        except Exception as e:
            self.logger.error(f"Erro ao enviar alerta Slack: {e}")
```

### 2. Regras de Alerta
```python
# src/monitoring/alert_rules.py
from typing import Dict, Any, List, Callable
import mlflow

class AlertRule:
    def __init__(
        self,
        name: str,
        condition: Callable[[Dict[str, Any]], bool],
        message_template: str,
        severity: str = "info"
    ):
        self.name = name
        self.condition = condition
        self.message_template = message_template
        self.severity = severity
        
class AlertManager:
    def __init__(self, alert_system: AlertSystem):
        self.alert_system = alert_system
        self.rules: List[AlertRule] = []
        
    def add_rule(self, rule: AlertRule):
        self.rules.append(rule)
        
    def evaluate_rules(self, metrics: Dict[str, Any]):
        for rule in self.rules:
            if rule.condition(metrics):
                message = rule.message_template.format(**metrics)
                
                # Log do alerta
                with mlflow.start_run():
                    mlflow.log_params({
                        'alert.name': rule.name,
                        'alert.severity': rule.severity
                    })
                    
                # Enviar alertas
                if rule.severity == "critical":
                    self.alert_system.send_email_alert(
                        f"Alerta Crítico: {rule.name}",
                        message,
                        ["admin@example.com"]
                    )
                
                self.alert_system.send_slack_alert(message)
```

## Visualizações

### 1. Dashboards
```python
# src/monitoring/dashboards.py
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, List

class MLflowDashboard:
    def __init__(self):
        self.figures = []
        
    def add_metric_chart(
        self,
        data: pd.DataFrame,
        metric_name: str,
        title: str
    ):
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data['timestamp'],
            y=data[metric_name],
            mode='lines+markers',
            name=metric_name
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Tempo",
            yaxis_title=metric_name
        )
        
        self.figures.append(fig)
        
    def add_drift_chart(
        self,
        baseline_data: np.ndarray,
        current_data: np.ndarray,
        title: str
    ):
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=baseline_data,
            name='Baseline',
            opacity=0.75
        ))
        
        fig.add_trace(go.Histogram(
            x=current_data,
            name='Atual',
            opacity=0.75
        ))
        
        fig.update_layout(
            title=title,
            barmode='overlay'
        )
        
        self.figures.append(fig)
        
    def save_dashboard(self, output_path: str):
        with open(output_path, 'w') as f:
            for fig in self.figures:
                f.write(fig.to_html(full_html=False))
```

### 2. Relatórios
```python
# src/monitoring/reports.py
import pandas as pd
from typing import Dict, Any, List
import mlflow

class MLflowReport:
    def __init__(self):
        self.client = mlflow.tracking.MlflowClient()
        
    def generate_experiment_report(
        self,
        experiment_id: str
    ) -> Dict[str, Any]:
        runs = self.client.search_runs([experiment_id])
        
        metrics_df = pd.DataFrame([
            {
                'run_id': run.info.run_id,
                'status': run.info.status,
                'start_time': run.info.start_time,
                **run.data.metrics
            }
            for run in runs
        ])
        
        report = {
            'total_runs': len(runs),
            'successful_runs': len(
                metrics_df[metrics_df['status'] == 'FINISHED']
            ),
            'failed_runs': len(
                metrics_df[metrics_df['status'] == 'FAILED']
            ),
            'average_metrics': metrics_df.mean().to_dict(),
            'best_metrics': metrics_df.max().to_dict(),
            'worst_metrics': metrics_df.min().to_dict()
        }
        
        return report
```

## Exemplos de Uso

### 1. Monitoramento Completo
```python
# Inicializar monitores
system_monitor = SystemMonitor()
mlflow_metrics = MLflowMetrics()
drift_detector = DriftDetector(baseline_data)
outlier_detector = OutlierDetector()

# Configurar alertas
alert_system = AlertSystem(config)
alert_manager = AlertManager(alert_system)

# Adicionar regras
alert_manager.add_rule(
    AlertRule(
        name="high_cpu",
        condition=lambda m: m['cpu_percent'] > 90,
        message_template="CPU usage is {cpu_percent}%",
        severity="critical"
    )
)

# Coletar métricas
metrics = system_monitor.collect_metrics()
alert_manager.evaluate_rules(metrics.__dict__)

# Gerar relatório
report = MLflowReport()
experiment_report = report.generate_experiment_report("experiment_id")
```

### 2. Dashboard Interativo
```python
# Criar dashboard
dashboard = MLflowDashboard()

# Adicionar visualizações
dashboard.add_metric_chart(
    metrics_df,
    'accuracy',
    'Model Accuracy Over Time'
)

dashboard.add_drift_chart(
    baseline_data,
    current_data,
    'Feature Drift Analysis'
)

# Salvar dashboard
dashboard.save_dashboard('mlflow_dashboard.html')
```

## Próximos Passos

1. [Segurança](../security/README.md)
2. [Troubleshooting](../troubleshooting/README.md)
3. [Integração Contínua](../ci_cd/README.md)
