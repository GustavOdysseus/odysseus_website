# Troubleshooting do MLflow

## Visão Geral

Este guia aborda os problemas mais comuns encontrados ao usar o MLflow e suas soluções, incluindo diagnóstico, resolução de problemas e prevenção.

## Problemas Comuns

### 1. Problemas de Conexão
```python
# src/troubleshooting/connection.py
import mlflow
import requests
import socket
import logging
from typing import Dict, Any

class ConnectionTroubleshooter:
    def __init__(self, tracking_uri: str):
        self.tracking_uri = tracking_uri
        self.logger = logging.getLogger(__name__)
        
    def check_connection(self) -> Dict[str, Any]:
        try:
            # Verificar conectividade
            mlflow.set_tracking_uri(self.tracking_uri)
            mlflow.search_experiments()
            
            return {
                'status': 'success',
                'message': 'Conexão estabelecida com sucesso'
            }
        except requests.exceptions.ConnectionError:
            self.logger.error("Erro de conexão com servidor MLflow")
            return {
                'status': 'error',
                'message': 'Não foi possível conectar ao servidor',
                'solution': 'Verifique se o servidor está rodando e acessível'
            }
        except Exception as e:
            self.logger.error(f"Erro inesperado: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'solution': 'Verifique logs do servidor para mais detalhes'
            }
```

### 2. Problemas de Armazenamento
```python
# src/troubleshooting/storage.py
import os
import shutil
import psutil
from typing import Dict, Any

class StorageTroubleshooter:
    def __init__(self, artifacts_dir: str):
        self.artifacts_dir = artifacts_dir
        
    def check_storage(self) -> Dict[str, Any]:
        # Verificar espaço em disco
        disk_usage = psutil.disk_usage(self.artifacts_dir)
        
        issues = []
        if disk_usage.percent > 90:
            issues.append({
                'type': 'disk_space',
                'message': 'Espaço em disco crítico',
                'solution': 'Limpe artefatos antigos ou expanda storage'
            })
            
        # Verificar permissões
        try:
            test_file = os.path.join(self.artifacts_dir, 'test.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except PermissionError:
            issues.append({
                'type': 'permissions',
                'message': 'Sem permissão de escrita',
                'solution': 'Ajuste permissões do diretório'
            })
            
        return {
            'status': 'error' if issues else 'success',
            'issues': issues,
            'disk_usage': disk_usage._asdict()
        }
```

### 3. Problemas de Logging
```python
# src/troubleshooting/logging.py
import mlflow
import logging
from typing import Dict, Any, List

class LoggingTroubleshooter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def validate_metrics(
        self,
        metrics: Dict[str, float]
    ) -> Dict[str, Any]:
        issues = []
        
        for key, value in metrics.items():
            if not isinstance(value, (int, float)):
                issues.append({
                    'metric': key,
                    'value': value,
                    'message': 'Métrica deve ser numérica',
                    'solution': 'Converta para float/int'
                })
                
        return {
            'status': 'error' if issues else 'success',
            'issues': issues
        }
        
    def validate_params(
        self,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        issues = []
        
        for key, value in params.items():
            if not isinstance(value, (str, int, float, bool)):
                issues.append({
                    'param': key,
                    'value': value,
                    'message': 'Parâmetro com tipo inválido',
                    'solution': 'Use tipos básicos (str/int/float/bool)'
                })
                
        return {
            'status': 'error' if issues else 'success',
            'issues': issues
        }
```

### 4. Problemas de Modelo
```python
# src/troubleshooting/model.py
import mlflow
import joblib
import pickle
from typing import Dict, Any, Optional

class ModelTroubleshooter:
    def __init__(self):
        self.client = mlflow.tracking.MlflowClient()
        
    def validate_model(
        self,
        model_uri: str
    ) -> Dict[str, Any]:
        try:
            # Tentar carregar modelo
            model = mlflow.pyfunc.load_model(model_uri)
            
            return {
                'status': 'success',
                'message': 'Modelo carregado com sucesso'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'solution': 'Verifique formato e dependências do modelo'
            }
            
    def check_model_dependencies(
        self,
        model_uri: str
    ) -> Dict[str, Any]:
        try:
            # Carregar conda env
            model_info = self.client.get_model_version_download_uri(
                model_uri
            )
            conda_env = mlflow.pyfunc.get_model_dependencies(
                model_info
            )
            
            return {
                'status': 'success',
                'dependencies': conda_env
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'solution': 'Verifique ambiente conda do modelo'
            }
```

## Ferramentas de Diagnóstico

### 1. Verificador de Sistema
```python
# src/troubleshooting/system.py
import platform
import sys
import pkg_resources
from typing import Dict, Any

class SystemChecker:
    def check_system(self) -> Dict[str, Any]:
        return {
            'os': platform.system(),
            'python_version': sys.version,
            'mlflow_version': pkg_resources.get_distribution('mlflow').version,
            'cpu_count': platform.machine(),
            'architecture': platform.architecture()[0]
        }
        
    def check_dependencies(self) -> Dict[str, Any]:
        dependencies = {}
        for pkg in ['numpy', 'pandas', 'scikit-learn', 'torch']:
            try:
                version = pkg_resources.get_distribution(pkg).version
                dependencies[pkg] = version
            except pkg_resources.DistributionNotFound:
                dependencies[pkg] = None
                
        return dependencies
```

### 2. Verificador de Logs
```python
# src/troubleshooting/logs.py
import re
from typing import Dict, Any, List
from pathlib import Path

class LogAnalyzer:
    def __init__(self, log_path: str):
        self.log_path = Path(log_path)
        
    def analyze_logs(self) -> Dict[str, Any]:
        if not self.log_path.exists():
            return {
                'status': 'error',
                'message': 'Arquivo de log não encontrado'
            }
            
        errors = []
        warnings = []
        
        with open(self.log_path) as f:
            for line in f:
                if 'ERROR' in line:
                    errors.append(self._parse_log_line(line))
                elif 'WARNING' in line:
                    warnings.append(self._parse_log_line(line))
                    
        return {
            'status': 'success',
            'errors': errors,
            'warnings': warnings,
            'error_count': len(errors),
            'warning_count': len(warnings)
        }
        
    def _parse_log_line(self, line: str) -> Dict[str, str]:
        # Exemplo: 2024-01-01 12:00:00 ERROR Message
        pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)'
        match = re.match(pattern, line)
        
        if match:
            return {
                'timestamp': match.group(1),
                'level': match.group(2),
                'message': match.group(3)
            }
        return {'message': line.strip()}
```

## Soluções Comuns

### 1. Limpeza de Cache
```python
# src/troubleshooting/cleanup.py
import shutil
import os
from typing import Dict, Any

class CacheCleaner:
    def __init__(self, mlflow_home: str):
        self.mlflow_home = mlflow_home
        
    def clean_cache(self) -> Dict[str, Any]:
        cache_dirs = [
            'cache',
            'artifacts/tmp',
            'models/cache'
        ]
        
        cleaned = []
        for dir_name in cache_dirs:
            dir_path = os.path.join(self.mlflow_home, dir_name)
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                cleaned.append(dir_name)
                
        return {
            'status': 'success',
            'cleaned_dirs': cleaned,
            'message': f'Limpeza concluída: {len(cleaned)} diretórios'
        }
```

### 2. Recuperação de Runs
```python
# src/troubleshooting/recovery.py
import mlflow
from typing import Dict, Any, List

class RunRecovery:
    def __init__(self):
        self.client = mlflow.tracking.MlflowClient()
        
    def recover_failed_runs(
        self,
        experiment_id: str
    ) -> Dict[str, Any]:
        # Buscar runs falhos
        failed_runs = self.client.search_runs(
            [experiment_id],
            "status = 'FAILED'"
        )
        
        recovered = []
        for run in failed_runs:
            try:
                # Tentar recuperar run
                self.client.set_terminated(
                    run.info.run_id,
                    status='FINISHED'
                )
                recovered.append(run.info.run_id)
            except Exception as e:
                self.logger.error(
                    f"Erro ao recuperar run {run.info.run_id}: {e}"
                )
                
        return {
            'status': 'success',
            'recovered_runs': recovered,
            'total_recovered': len(recovered)
        }
```

## Exemplos de Uso

### 1. Diagnóstico Completo
```python
# Verificar sistema
system_checker = SystemChecker()
system_info = system_checker.check_system()
dependencies = system_checker.check_dependencies()

# Verificar conexão
connection_checker = ConnectionTroubleshooter("http://localhost:5000")
connection_status = connection_checker.check_connection()

# Verificar storage
storage_checker = StorageTroubleshooter("/mlflow/artifacts")
storage_status = storage_checker.check_storage()

# Analisar logs
log_analyzer = LogAnalyzer("/mlflow/logs/mlflow.log")
log_analysis = log_analyzer.analyze_logs()
```

### 2. Resolução de Problemas
```python
# Limpar cache
cleaner = CacheCleaner("/mlflow")
cleanup_result = cleaner.clean_cache()

# Recuperar runs
recovery = RunRecovery()
recovery_result = recovery.recover_failed_runs("experiment_id")

# Validar modelo
model_checker = ModelTroubleshooter()
model_status = model_checker.validate_model("runs:/run_id/model")
dependencies = model_checker.check_model_dependencies("runs:/run_id/model")
```

## Próximos Passos

1. [Segurança](../security/README.md)
2. [Monitoramento Avançado](../monitoring/advanced.md)
3. [Manutenção](../maintenance/README.md)
