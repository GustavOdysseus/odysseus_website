# Melhores Práticas do AgentOps

## Estrutura do Projeto

### 1. Organização de Código
```
projeto/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── specialized/
│   ├── monitoring/
│   │   ├── __init__.py
│   │   └── metrics.py
│   └── utils/
│       ├── __init__.py
│       └── logging.py
├── config/
│   ├── agentops.yaml
│   └── logging.yaml
└── tests/
    ├── __init__.py
    └── test_agents.py
```

### 2. Configuração
```yaml
# config/agentops.yaml
api_key: ${AGENTOPS_API_KEY}
organization: "sua_organizacao"
environment: "production"

monitoring:
  refresh_rate: 5
  log_level: "INFO"
  metrics:
    - response_time
    - token_usage
    - error_rate

alerts:
  slack_webhook: ${SLACK_WEBHOOK}
  email: "alerts@empresa.com"
```

## Monitoramento

### 1. Sessões
```python
from agentops import Client

# Boa prática: Use tags descritivas
client.start_session(
    tags=["service:auth", "env:prod"],
    custom_metrics={"team": "auth"}
)

# Boa prática: Sempre finalize sessões
try:
    # Seu código aqui
    pass
finally:
    client.end_session()
```

### 2. Métricas
```python
# Boa prática: Use métricas padronizadas
client.log_metric(
    name="response_time_ms",  # Unidade no nome
    value=response.time,
    tags={
        "endpoint": "/api/v1/auth",
        "method": "POST"
    }
)

# Boa prática: Agrupe métricas relacionadas
client.log_metrics({
    "cpu_usage": cpu,
    "memory_usage": memory,
    "disk_usage": disk
}, tags={"host": hostname})
```

### 3. Erros
```python
# Boa prática: Log detalhado de erros
try:
    result = process_data()
except Exception as e:
    client.log_error(
        error=str(e),
        severity="high",
        context={
            "function": "process_data",
            "input_size": len(data)
        }
    )
    raise
```

## Agentes

### 1. Configuração
```python
# Boa prática: Configuração modular
class AgentConfig:
    def __init__(self, config_path):
        self.config = load_config(config_path)
        self.client = Client()
        self.client.configure(**self.config)

# Uso
config = AgentConfig("config/agent.yaml")
agent = Agent(config)
```

### 2. Monitoramento
```python
# Boa prática: Monitore o ciclo de vida completo
class MonitoredAgent:
    def __init__(self, client):
        self.client = client
    
    def execute(self, task):
        self.client.start_session(
            tags=["agent:worker", "task:process"]
        )
        
        try:
            # Início
            self.client.log_event("task_started")
            
            # Execução
            result = self.process_task(task)
            
            # Métricas
            self.client.log_metrics({
                "execution_time": result.time,
                "memory_used": result.memory
            })
            
            return result
            
        except Exception as e:
            self.client.log_error(error=str(e))
            raise
        finally:
            self.client.end_session()
```

### 3. Performance
```python
# Boa prática: Monitore recursos
class PerformanceMonitor:
    def __init__(self, client):
        self.client = client
    
    def monitor(self):
        while True:
            metrics = self.collect_metrics()
            
            self.client.log_metrics({
                "cpu_usage": metrics.cpu,
                "memory_usage": metrics.memory,
                "active_threads": metrics.threads
            })
            
            time.sleep(5)
```

## Logging

### 1. Estrutura
```python
# Boa prática: Logging estruturado
def log_structured(client, event, data):
    client.log_event(
        name=event,
        data={
            "timestamp": time.time(),
            "service": "auth",
            "environment": "production",
            **data
        }
    )
```

### 2. Níveis
```python
# Boa prática: Use níveis apropriados
def handle_request(client, request):
    # Info para operações normais
    client.log_info("Request received", {
        "method": request.method,
        "path": request.path
    })
    
    try:
        result = process_request(request)
        
        # Debug para detalhes
        client.log_debug("Request processed", {
            "processing_time": result.time
        })
        
        return result
        
    except Exception as e:
        # Error para falhas
        client.log_error("Request failed", {
            "error": str(e),
            "stack_trace": traceback.format_exc()
        })
        raise
```

## Alertas

### 1. Configuração
```python
# Boa prática: Alertas graduais
client.configure_alerts({
    "response_time": {
        "warning": {
            "threshold": 500,  # ms
            "duration": "5m",
            "channels": ["slack"]
        },
        "critical": {
            "threshold": 1000,  # ms
            "duration": "1m",
            "channels": ["slack", "email", "pager"]
        }
    }
})
```

### 2. Notificações
```python
# Boa prática: Contexto em alertas
def send_alert(client, alert):
    client.notify(
        severity=alert.severity,
        message=alert.message,
        context={
            "service": alert.service,
            "metric": alert.metric,
            "threshold": alert.threshold,
            "current_value": alert.value,
            "duration": alert.duration
        },
        actions=[
            {
                "name": "View Dashboard",
                "url": alert.dashboard_url
            }
        ]
    )
```

## Testes

### 1. Monitoramento
```python
# Boa prática: Monitore testes
class TestMonitor:
    def __init__(self):
        self.client = Client()
        self.client.configure(environment="testing")
    
    def start_test(self, test_name):
        self.client.start_session(
            tags=["test", test_name]
        )
    
    def end_test(self, success):
        self.client.end_session(
            end_state="success" if success else "failure"
        )
```

### 2. Métricas
```python
# Boa prática: Métricas de teste
class TestMetrics:
    def __init__(self, client):
        self.client = client
    
    def record_test(self, result):
        self.client.log_metrics({
            "test_duration": result.duration,
            "assertions_passed": result.passed,
            "assertions_failed": result.failed,
            "coverage": result.coverage
        })
```

## CI/CD

### 1. Pipeline
```yaml
# Boa prática: Monitoramento em CI
name: CI Monitoring

on: [push, pull_request]

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup AgentOps
        run: |
          pip install agentops
          agentops configure
        env:
          AGENTOPS_API_KEY: ${{ secrets.AGENTOPS_API_KEY }}
      
      - name: Run Tests
        run: |
          python -m pytest --agentops
```

### 2. Deployment
```python
# Boa prática: Monitore deployments
class DeploymentMonitor:
    def __init__(self, client):
        self.client = client
    
    def start_deployment(self, version):
        self.client.start_session(
            tags=["deployment", version]
        )
    
    def record_step(self, step, status):
        self.client.log_event(
            f"deployment_{step}",
            {"status": status}
        )
    
    def end_deployment(self, success):
        self.client.end_session(
            end_state="success" if success else "failure"
        )
```

## Dashboard

### 1. Organização
```python
# Boa prática: Dashboards organizados
class DashboardManager:
    def __init__(self, client):
        self.client = client
    
    def setup_dashboards(self):
        # Overview
        self.create_overview_dashboard()
        
        # Performance
        self.create_performance_dashboard()
        
        # Errors
        self.create_error_dashboard()
    
    def create_overview_dashboard(self):
        self.client.create_dashboard(
            name="System Overview",
            description="High-level system metrics",
            refresh_rate=5,
            widgets=[
                {"type": "counter", "metric": "requests"},
                {"type": "graph", "metric": "response_time"},
                {"type": "alert", "metric": "errors"}
            ]
        )
```

### 2. Visualizações
```python
# Boa prática: Visualizações efetivas
class Visualizations:
    def __init__(self, client):
        self.client = client
    
    def create_performance_view(self):
        self.client.create_visualization(
            type="line",
            metrics=["response_time", "throughput"],
            aggregation="avg",
            timeframe="1h",
            annotations={
                "deployments": {"color": "blue"},
                "incidents": {"color": "red"}
            }
        )
```

## Segurança

### 1. Configuração
```python
# Boa prática: Configuração segura
class SecureConfig:
    def __init__(self):
        self.client = Client()
        
        # Carregue secrets de forma segura
        self.api_key = os.environ.get("AGENTOPS_API_KEY")
        
        # Configure com TLS
        self.client.configure(
            api_key=self.api_key,
            ssl_verify=True,
            ssl_cert_path="path/to/cert"
        )
```

### 2. Dados Sensíveis
```python
# Boa prática: Proteja dados sensíveis
class DataSecurity:
    def __init__(self, client):
        self.client = client
    
    def log_user_action(self, user, action):
        # Nunca log dados sensíveis
        self.client.log_event(
            "user_action",
            {
                "user_id": hash(user.id),  # Hash identificadores
                "action": action,
                "timestamp": time.time()
            }
        )
```

## Troubleshooting

### 1. Diagnóstico
```python
# Boa prática: Ferramentas de diagnóstico
class Diagnostics:
    def __init__(self, client):
        self.client = client
    
    def check_health(self):
        try:
            # Verificação de conectividade
            status = self.client.check_connection()
            
            # Verificação de configuração
            config = self.client.validate_config()
            
            # Verificação de métricas
            metrics = self.client.verify_metrics()
            
            return {
                "status": status,
                "config": config,
                "metrics": metrics
            }
            
        except Exception as e:
            self.client.log_error(
                error=str(e),
                context={"check": "health"}
            )
            raise
```

### 2. Recuperação
```python
# Boa prática: Recuperação de falhas
class ErrorRecovery:
    def __init__(self, client):
        self.client = client
    
    def handle_failure(self, error):
        # Log do erro
        self.client.log_error(error)
        
        # Tentativa de recuperação
        try:
            self.recover_from_error(error)
            
            # Log de sucesso
            self.client.log_event(
                "error_recovery",
                {"status": "success"}
            )
            
        except Exception as e:
            # Log de falha na recuperação
            self.client.log_error(
                str(e),
                context={"recovery": "failed"}
            )
            raise
```
