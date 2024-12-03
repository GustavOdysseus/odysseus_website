# Escalabilidade com MLflow

## Visão Geral

Este guia aborda as melhores práticas para escalar projetos MLflow, incluindo processamento distribuído, otimização de recursos e gerenciamento de grandes volumes de dados.

## Processamento Distribuído

### 1. Configuração Distribuída
```python
# src/distributed/config.py
import mlflow
import ray
from typing import Dict

def setup_distributed():
    # Inicializar Ray
    ray.init(
        address="auto",
        runtime_env={
            "pip": ["mlflow", "scikit-learn", "pandas"]
        }
    )
    
    # Configurar MLflow
    mlflow.set_tracking_uri("http://tracking-server:5000")
    mlflow.set_experiment("distributed_training")

@ray.remote
class DistributedTrainer:
    def __init__(self, config: Dict):
        self.config = config
        
    def train(self, data_partition):
        with mlflow.start_run():
            # Treinar modelo na partição
            model = self.train_partition(data_partition)
            
            # Log de métricas locais
            metrics = self.evaluate(model, data_partition)
            mlflow.log_metrics(metrics)
            
            return model, metrics
```

### 2. Paralelização
```python
# src/distributed/parallel.py
import mlflow
import ray
import numpy as np
from typing import List

@ray.remote
class DataPartitioner:
    def partition_data(self, data, num_partitions):
        # Particionar dados
        partitions = np.array_split(data, num_partitions)
        return [ray.put(partition) for partition in partitions]

class ParallelTraining:
    def __init__(self, num_workers):
        self.num_workers = num_workers
        self.trainers = [
            DistributedTrainer.remote(config)
            for _ in range(num_workers)
        ]
        
    def train_parallel(self, data):
        # Particionar dados
        partitioner = DataPartitioner.remote()
        partitions = ray.get(
            partitioner.partition_data.remote(data, self.num_workers)
        )
        
        # Treinar em paralelo
        futures = [
            trainer.train.remote(partition)
            for trainer, partition in zip(self.trainers, partitions)
        ]
        
        # Coletar resultados
        results = ray.get(futures)
        
        # Agregar resultados
        return self.aggregate_results(results)
```

## Otimização de Recursos

### 1. Gerenciamento de Memória
```python
# src/optimization/memory.py
import mlflow
import pandas as pd
from typing import Iterator

class MemoryOptimizer:
    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size
        
    def process_in_chunks(self, data_path: str) -> Iterator:
        # Processar dados em chunks
        for chunk in pd.read_csv(data_path, chunksize=self.chunk_size):
            yield self.optimize_chunk(chunk)
            
    def optimize_chunk(self, chunk: pd.DataFrame) -> pd.DataFrame:
        # Otimizar tipos de dados
        for col in chunk.columns:
            if chunk[col].dtype == "object":
                chunk[col] = pd.Categorical(chunk[col])
            elif chunk[col].dtype == "float64":
                chunk[col] = chunk[col].astype("float32")
                
        return chunk
        
    def log_memory_usage(self):
        with mlflow.start_run():
            memory_usage = {
                col: usage for col, usage in
                self.current_chunk.memory_usage(deep=True).items()
            }
            mlflow.log_metrics(memory_usage)
```

### 2. Cache e Armazenamento
```python
# src/optimization/cache.py
import mlflow
import joblib
from pathlib import Path
import hashlib

class CacheManager:
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
    def get_cache_key(self, data, params):
        # Gerar chave única
        key = f"{hashlib.md5(str(data).encode()).hexdigest()}"
        key += f"_{hashlib.md5(str(params).encode()).hexdigest()}"
        return key
        
    def save_to_cache(self, key: str, obj: any):
        cache_path = self.cache_dir / f"{key}.joblib"
        joblib.dump(obj, cache_path)
        
    def load_from_cache(self, key: str) -> any:
        cache_path = self.cache_dir / f"{key}.joblib"
        if cache_path.exists():
            return joblib.load(cache_path)
        return None
```

## Gerenciamento de Dados

### 1. Armazenamento Distribuído
```python
# src/data/storage.py
import mlflow
import dask.dataframe as dd
from typing import List

class DistributedStorage:
    def __init__(self, storage_options: dict):
        self.storage_options = storage_options
        
    def save_partitions(self, df: dd.DataFrame, path: str):
        # Salvar partições
        df.to_parquet(
            path,
            engine="pyarrow",
            storage_options=self.storage_options
        )
        
    def load_partitions(self, path: str) -> dd.DataFrame:
        # Carregar partições
        return dd.read_parquet(
            path,
            engine="pyarrow",
            storage_options=self.storage_options
        )
        
    def log_partitions(self, path: str):
        with mlflow.start_run():
            mlflow.log_artifact(path)
```

### 2. Streaming de Dados
```python
# src/data/streaming.py
import mlflow
import pandas as pd
from typing import Iterator
from kafka import KafkaConsumer

class DataStreamer:
    def __init__(self, topic: str, bootstrap_servers: List[str]):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda x: pd.read_json(x)
        )
        
    def stream_data(self) -> Iterator[pd.DataFrame]:
        for message in self.consumer:
            yield message.value
            
    def process_stream(self, processor):
        for batch in self.stream_data():
            # Processar batch
            results = processor(batch)
            
            # Log de métricas
            with mlflow.start_run():
                mlflow.log_metrics({
                    "processed_records": len(batch),
                    "processing_time": results["time"]
                })
```

## Monitoramento de Performance

### 1. Métricas de Performance
```python
# src/monitoring/performance.py
import mlflow
import time
import psutil
from dataclasses import dataclass

@dataclass
class PerformanceMetrics:
    cpu_usage: float
    memory_usage: float
    processing_time: float
    throughput: float

class PerformanceMonitor:
    def __init__(self):
        self.start_time = None
        
    def start_monitoring(self):
        self.start_time = time.time()
        
    def get_metrics(self) -> PerformanceMetrics:
        return PerformanceMetrics(
            cpu_usage=psutil.cpu_percent(),
            memory_usage=psutil.virtual_memory().percent,
            processing_time=time.time() - self.start_time,
            throughput=self.calculate_throughput()
        )
        
    def log_metrics(self):
        metrics = self.get_metrics()
        with mlflow.start_run():
            mlflow.log_metrics({
                "cpu_usage": metrics.cpu_usage,
                "memory_usage": metrics.memory_usage,
                "processing_time": metrics.processing_time,
                "throughput": metrics.throughput
            })
```

### 2. Otimização Automática
```python
# src/optimization/auto_optimize.py
import mlflow
from typing import Dict
import optuna

class AutoOptimizer:
    def __init__(self, param_space: Dict):
        self.param_space = param_space
        
    def optimize(self, objective, n_trials=100):
        study = optuna.create_study(direction="minimize")
        study.optimize(objective, n_trials=n_trials)
        
        # Log dos melhores parâmetros
        with mlflow.start_run():
            mlflow.log_params(study.best_params)
            mlflow.log_metric("best_value", study.best_value)
            
        return study.best_params
        
    def suggest_resources(self, data_size: int) -> Dict:
        # Sugerir recursos baseado no tamanho dos dados
        if data_size < 1e6:
            return {"workers": 2, "memory": "4GB"}
        elif data_size < 1e9:
            return {"workers": 4, "memory": "16GB"}
        else:
            return {"workers": 8, "memory": "32GB"}
```

## Exemplos de Uso

### 1. Treinamento Distribuído
```python
# Configurar ambiente distribuído
setup_distributed()

# Inicializar treinamento paralelo
trainer = ParallelTraining(num_workers=4)

# Treinar modelo
results = trainer.train_parallel(data)

# Log de resultados agregados
with mlflow.start_run():
    mlflow.log_metrics(results)
```

### 2. Processamento Otimizado
```python
# Inicializar otimizadores
memory_optimizer = MemoryOptimizer()
cache_manager = CacheManager()

# Processar dados com otimização
for chunk in memory_optimizer.process_in_chunks(data_path):
    # Verificar cache
    cache_key = cache_manager.get_cache_key(chunk, params)
    results = cache_manager.load_from_cache(cache_key)
    
    if results is None:
        # Processar e cachear
        results = process_chunk(chunk)
        cache_manager.save_to_cache(cache_key, results)
```

## Próximos Passos

1. [Integração com Outras Ferramentas](../integrations/README.md)
2. [Manutenção](../maintenance/README.md)
3. [Monitoramento Avançado](../monitoring/advanced.md)
