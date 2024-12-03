# Monitoramento de Modelos MLflow

## Visão Geral

O monitoramento de modelos em produção é crucial para garantir que eles continuem funcionando conforme esperado. Esta documentação aborda as principais estratégias e ferramentas para monitoramento usando MLflow.

## Tipos de Monitoramento

### 1. Monitoramento de Modelo

#### Performance do Modelo
```python
import mlflow
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score

def monitorar_performance(model, X_val, y_val):
    # Fazer previsões
    y_pred = model.predict(X_val)
    
    # Calcular métricas
    metrics = {
        "acuracia": accuracy_score(y_val, y_pred),
        "precisao": precision_score(y_val, y_pred),
        "recall": recall_score(y_val, y_pred)
    }
    
    # Registrar métricas no MLflow
    with mlflow.start_run():
        for name, value in metrics.items():
            mlflow.log_metric(name, value)
```

#### Drift de Dados
```python
from scipy.stats import ks_2samp

def detectar_drift(dados_treino, dados_producao):
    resultados = {}
    
    for coluna in dados_treino.columns:
        # Teste Kolmogorov-Smirnov
        estatistica, p_valor = ks_2samp(
            dados_treino[coluna],
            dados_producao[coluna]
        )
        
        resultados[coluna] = {
            "estatistica": estatistica,
            "p_valor": p_valor,
            "drift_detectado": p_valor < 0.05
        }
    
    return resultados
```

### 2. Monitoramento de Sistema

#### Métricas de Sistema
```python
import psutil
import time

def coletar_metricas_sistema():
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }

def monitorar_sistema(intervalo=60):
    while True:
        metricas = coletar_metricas_sistema()
        
        with mlflow.start_run():
            for nome, valor in metricas.items():
                mlflow.log_metric(nome, valor)
        
        time.sleep(intervalo)
```

#### Latência de Predições
```python
import time
from functools import wraps

def medir_latencia(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fim = time.time()
        
        latencia = fim - inicio
        with mlflow.start_run():
            mlflow.log_metric("latencia_predicao", latencia)
        
        return resultado
    return wrapper

@medir_latencia
def fazer_predicao(modelo, dados):
    return modelo.predict(dados)
```

### 3. Monitoramento de Logs

#### Configuração de Logging
```python
import logging
import mlflow.tracking

def configurar_logging():
    logger = logging.getLogger("mlflow")
    logger.setLevel(logging.INFO)
    
    # Handler para arquivo
    fh = logging.FileHandler("mlflow_modelo.log")
    fh.setLevel(logging.INFO)
    
    # Handler para console
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

logger = configurar_logging()
```

## Dashboards e Visualizações

### 1. MLflow UI
```python
# Iniciar servidor MLflow UI
mlflow.ui.serve()
```

### 2. Grafana
```python
# docker-compose.yml para Grafana + Prometheus
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
      
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
```

## Alertas

### 1. Configuração de Alertas
```python
import smtplib
from email.mime.text import MIMEText

def enviar_alerta(assunto, mensagem, destinatario):
    # Configurações do servidor SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "seu_email@gmail.com"
    smtp_password = "sua_senha"
    
    # Criar mensagem
    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = smtp_user
    msg['To'] = destinatario
    
    # Enviar email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

def monitorar_com_alertas(modelo, dados, limiar=0.8):
    # Fazer predições
    score = modelo.predict_proba(dados)
    
    # Verificar performance
    if score.mean() < limiar:
        enviar_alerta(
            "Alerta de Performance",
            f"Score do modelo caiu para {score.mean():.2f}",
            "equipe@empresa.com"
        )
```

### 2. Webhooks
```python
import requests

def notificar_slack(webhook_url, mensagem):
    payload = {"text": mensagem}
    requests.post(webhook_url, json=payload)

def alertar_drift(dados_treino, dados_producao, webhook_url):
    resultados = detectar_drift(dados_treino, dados_producao)
    
    for coluna, info in resultados.items():
        if info["drift_detectado"]:
            mensagem = f"Drift detectado na coluna {coluna}"
            notificar_slack(webhook_url, mensagem)
```

## Exemplo Completo: Sistema de Monitoramento

```python
import mlflow
import pandas as pd
import numpy as np
from datetime import datetime
import time

class MonitoramentoModelo:
    def __init__(self, model_name, stage="Production"):
        self.client = mlflow.tracking.MlflowClient()
        self.model = mlflow.pyfunc.load_model(
            f"models:/{model_name}/{stage}"
        )
        self.logger = configurar_logging()
        
    def monitorar_predicoes(self, dados):
        try:
            # Fazer predições
            inicio = time.time()
            predicoes = self.model.predict(dados)
            latencia = time.time() - inicio
            
            # Registrar métricas
            with mlflow.start_run():
                mlflow.log_metric("latencia", latencia)
                mlflow.log_metric("tamanho_batch", len(dados))
                
                if hasattr(predicoes, "mean"):
                    mlflow.log_metric("media_predicoes", predicoes.mean())
                    mlflow.log_metric("std_predicoes", predicoes.std())
            
            return predicoes
            
        except Exception as e:
            self.logger.error(f"Erro nas predições: {str(e)}")
            raise
    
    def monitorar_drift(self, dados_ref, dados_atual):
        try:
            resultados = detectar_drift(dados_ref, dados_atual)
            
            with mlflow.start_run():
                for coluna, info in resultados.items():
                    mlflow.log_metric(f"drift_{coluna}", info["estatistica"])
                    
            return resultados
            
        except Exception as e:
            self.logger.error(f"Erro na detecção de drift: {str(e)}")
            raise
    
    def monitorar_sistema(self):
        try:
            metricas = coletar_metricas_sistema()
            
            with mlflow.start_run():
                for nome, valor in metricas.items():
                    mlflow.log_metric(nome, valor)
                    
            return metricas
            
        except Exception as e:
            self.logger.error(f"Erro no monitoramento do sistema: {str(e)}")
            raise

# Uso do sistema de monitoramento
if __name__ == "__main__":
    # Inicializar monitoramento
    monitor = MonitoramentoModelo("modelo_classificacao")
    
    # Loop de monitoramento
    while True:
        # Coletar dados mais recentes
        dados_atuais = pd.read_csv("dados_producao.csv")
        dados_ref = pd.read_csv("dados_referencia.csv")
        
        # Monitorar predições
        predicoes = monitor.monitorar_predicoes(dados_atuais)
        
        # Verificar drift
        drift = monitor.monitorar_drift(dados_ref, dados_atuais)
        
        # Monitorar sistema
        sistema = monitor.monitorar_sistema()
        
        # Aguardar próximo ciclo
        time.sleep(300)  # 5 minutos
```

## Boas Práticas

1. **Monitoramento Proativo**
   - Estabeleça baselines claros
   - Defina limiares de alerta
   - Implemente verificações automáticas

2. **Logs Estruturados**
   - Use níveis de log apropriados
   - Inclua contexto suficiente
   - Mantenha rotação de logs

3. **Backup e Retenção**
   - Faça backup regular das métricas
   - Defina política de retenção
   - Mantenha histórico de alertas

4. **Documentação**
   - Mantenha runbooks atualizados
   - Documente procedimentos de resposta
   - Registre incidentes e resoluções

## Próximos Passos

1. [MLflow Projects](../projects/README.md)
2. [Integração Contínua](../ci_cd/README.md)
3. [Governança de Modelos](../governance/README.md)
