# Manutenção do MLflow

## Visão Geral

Este guia aborda as melhores práticas e procedimentos para manutenção de ambientes MLflow, incluindo backup, limpeza, atualizações e resolução de problemas comuns.

## Backup e Recuperação

### 1. Backup do Banco de Dados
```python
# src/maintenance/backup.py
import sqlite3
import psycopg2
import os
from datetime import datetime
from typing import Dict, Any

class MLflowBackup:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.backup_dir = config["backup_dir"]
        os.makedirs(self.backup_dir, exist_ok=True)
        
    def backup_sqlite(self, db_path: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(
            self.backup_dir,
            f"mlflow_backup_{timestamp}.db"
        )
        
        # Criar backup
        connection = sqlite3.connect(db_path)
        backup = sqlite3.connect(backup_path)
        connection.backup(backup)
        
        connection.close()
        backup.close()
        
    def backup_postgres(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(
            self.backup_dir,
            f"mlflow_backup_{timestamp}.sql"
        )
        
        # Criar backup usando pg_dump
        os.system(
            f"pg_dump -U {self.config['db_user']} "
            f"-h {self.config['db_host']} "
            f"-p {self.config['db_port']} "
            f"{self.config['db_name']} > {backup_path}"
        )
```

### 2. Backup de Artefatos
```python
# src/maintenance/artifacts.py
import shutil
import boto3
from typing import Dict, Any

class ArtifactBackup:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def backup_local_artifacts(self, source_dir: str, dest_dir: str):
        # Backup de artefatos locais
        shutil.copytree(source_dir, dest_dir)
        
    def backup_s3_artifacts(
        self,
        source_bucket: str,
        dest_bucket: str,
        prefix: str = ""
    ):
        s3 = boto3.client("s3")
        
        # Listar objetos
        objects = s3.list_objects_v2(
            Bucket=source_bucket,
            Prefix=prefix
        )
        
        # Copiar objetos
        for obj in objects.get("Contents", []):
            s3.copy_object(
                Bucket=dest_bucket,
                Key=obj["Key"],
                CopySource={
                    "Bucket": source_bucket,
                    "Key": obj["Key"]
                }
            )
```

## Limpeza e Otimização

### 1. Limpeza de Runs Antigos
```python
# src/maintenance/cleanup.py
import mlflow
from datetime import datetime, timedelta
from typing import List

class RunCleanup:
    def __init__(self, experiment_id: str):
        self.experiment_id = experiment_id
        
    def delete_old_runs(self, days: int):
        # Buscar runs antigos
        cutoff_date = datetime.now() - timedelta(days=days)
        
        client = mlflow.tracking.MlflowClient()
        runs = client.search_runs(
            experiment_ids=[self.experiment_id]
        )
        
        # Deletar runs antigos
        for run in runs:
            if run.info.start_time < cutoff_date.timestamp() * 1000:
                client.delete_run(run.info.run_id)
                
    def archive_runs(self, run_ids: List[str]):
        client = mlflow.tracking.MlflowClient()
        
        # Arquivar runs
        for run_id in run_ids:
            client.set_terminated(run_id)
```

### 2. Otimização de Banco de Dados
```python
# src/maintenance/optimization.py
import sqlite3
import psycopg2
from typing import Dict, Any

class DatabaseOptimizer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def optimize_sqlite(self, db_path: str):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Otimizar banco
        cursor.execute("VACUUM")
        cursor.execute("ANALYZE")
        
        conn.close()
        
    def optimize_postgres(self):
        conn = psycopg2.connect(**self.config)
        cursor = conn.cursor()
        
        # Otimizar banco
        cursor.execute("VACUUM ANALYZE")
        
        conn.close()
```

## Atualizações

### 1. Atualização de Versão
```python
# src/maintenance/updates.py
import subprocess
import sys
from typing import Dict, Any

class MLflowUpdater:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def backup_before_update(self):
        # Realizar backup antes da atualização
        backup = MLflowBackup(self.config)
        backup.backup_sqlite("mlflow.db")
        
    def update_mlflow(self, version: str = None):
        # Backup
        self.backup_before_update()
        
        # Atualizar MLflow
        if version:
            subprocess.check_call([
                sys.executable,
                "-m",
                "pip",
                "install",
                f"mlflow=={version}"
            ])
        else:
            subprocess.check_call([
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "mlflow"
            ])
```

### 2. Migração de Banco de Dados
```python
# src/maintenance/migration.py
import alembic
from alembic.config import Config
from typing import Dict, Any

class DatabaseMigration:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def create_alembic_config(self):
        alembic_cfg = Config()
        alembic_cfg.set_main_option(
            "script_location",
            "mlflow/alembic"
        )
        alembic_cfg.set_main_option(
            "sqlalchemy.url",
            self.config["db_uri"]
        )
        return alembic_cfg
        
    def upgrade_database(self):
        # Configurar Alembic
        alembic_cfg = self.create_alembic_config()
        
        # Executar migração
        alembic.command.upgrade(alembic_cfg, "head")
```

## Monitoramento e Diagnóstico

### 1. Monitoramento de Saúde
```python
# src/maintenance/health.py
import requests
import psutil
import os
from typing import Dict, Any

class HealthMonitor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def check_server_health(self) -> Dict[str, Any]:
        # Verificar servidor MLflow
        try:
            response = requests.get(self.config["tracking_uri"])
            server_status = response.status_code == 200
        except:
            server_status = False
            
        # Verificar recursos
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage("/").percent
        
        return {
            "server_status": server_status,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage
        }
```

### 2. Diagnóstico de Problemas
```python
# src/maintenance/diagnostics.py
import mlflow
import logging
from typing import Dict, Any, List

class MLflowDiagnostics:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def check_connectivity(self) -> bool:
        try:
            mlflow.set_tracking_uri(self.config["tracking_uri"])
            mlflow.search_experiments()
            return True
        except Exception as e:
            self.logger.error(f"Erro de conectividade: {e}")
            return False
            
    def validate_artifacts(
        self,
        experiment_id: str
    ) -> List[Dict[str, Any]]:
        client = mlflow.tracking.MlflowClient()
        runs = client.search_runs([experiment_id])
        
        invalid_artifacts = []
        for run in runs:
            artifacts = client.list_artifacts(run.info.run_id)
            for artifact in artifacts:
                try:
                    # Tentar acessar artefato
                    client.download_artifacts(
                        run.info.run_id,
                        artifact.path
                    )
                except Exception as e:
                    invalid_artifacts.append({
                        "run_id": run.info.run_id,
                        "artifact": artifact.path,
                        "error": str(e)
                    })
                    
        return invalid_artifacts
```

## Exemplos de Uso

### 1. Backup Completo
```python
# Configuração
config = {
    "backup_dir": "/path/to/backup",
    "db_user": "mlflow",
    "db_host": "localhost",
    "db_port": 5432,
    "db_name": "mlflow"
}

# Criar backups
backup = MLflowBackup(config)
backup.backup_postgres()

artifact_backup = ArtifactBackup(config)
artifact_backup.backup_s3_artifacts(
    "source-bucket",
    "backup-bucket",
    "mlflow/artifacts"
)
```

### 2. Manutenção Periódica
```python
# Limpeza de runs antigos
cleanup = RunCleanup("experiment_id")
cleanup.delete_old_runs(days=30)

# Otimização de banco
optimizer = DatabaseOptimizer(config)
optimizer.optimize_postgres()

# Verificação de saúde
monitor = HealthMonitor(config)
health_status = monitor.check_server_health()
```

## Próximos Passos

1. [Monitoramento Avançado](../monitoring/advanced.md)
2. [Segurança](../security/README.md)
3. [Troubleshooting](../troubleshooting/README.md)
