# Cache Tools - Documentação Detalhada

## Visão Geral
O sistema de cache do CrewAI fornece ferramentas para otimização de performance através do armazenamento e recuperação eficiente de resultados de operações anteriores.

## Componentes Principais

### 1. CacheTools
```python
class CacheTools(BaseModel):
    """Ferramentas padrão para acesso ao cache."""
    
    name: str = "Hit Cache"
    cache_handler: CacheHandler = Field(
        description="Gerenciador de cache para o crew",
        default_factory=CacheHandler,
    )
    
    def tool(self):
        return CrewStructuredTool.from_function(
            func=self.hit_cache,
            name=self.name,
            description="Lê diretamente do cache",
        )
```

### 2. CacheHandler
```python
class CacheHandler:
    """Gerenciador de cache para armazenamento e recuperação."""
    
    def __init__(self):
        self._cache = {}
        
    def read(self, tool: str, tool_input: str) -> Any:
        """Lê valor do cache."""
        key = self._make_key(tool, tool_input)
        return self._cache.get(key)
        
    def write(self, tool: str, tool_input: str, result: Any):
        """Escreve valor no cache."""
        key = self._make_key(tool, tool_input)
        self._cache[key] = result
```

## Funcionalidades

### 1. Acesso ao Cache
```python
def hit_cache(self, key: str) -> Any:
    """Acessa valor no cache usando chave composta."""
    split = key.split("tool:")
    tool = split[1].split("|input:")[0].strip()
    tool_input = split[1].split("|input:")[1].strip()
    return self.cache_handler.read(tool, tool_input)
```

### 2. Geração de Chaves
```python
def _make_key(self, tool: str, tool_input: str) -> str:
    """Gera chave única para o cache."""
    return f"tool:{tool}|input:{tool_input}"
```

## Padrões de Uso

### 1. Cache Básico
```python
# Criação do cache
cache_tools = CacheTools()
cache_tool = cache_tools.tool()

# Uso
result = cache_tool.run(
    key="tool:calculator|input:1+1"
)
```

### 2. Cache com Validação
```python
class ValidatedCacheTools(CacheTools):
    def hit_cache(self, key: str) -> Any:
        # Valida formato da chave
        if not self._validate_key(key):
            raise ValueError("Formato de chave inválido")
            
        return super().hit_cache(key)
        
    def _validate_key(self, key: str) -> bool:
        return "tool:" in key and "|input:" in key
```

## Estratégias de Cache

### 1. Cache em Memória
```python
class MemoryCacheHandler(CacheHandler):
    def __init__(self, max_size: int = 1000):
        super().__init__()
        self.max_size = max_size
        
    def write(self, tool: str, tool_input: str, result: Any):
        # Limpa cache se necessário
        if len(self._cache) >= self.max_size:
            self._clean_cache()
            
        super().write(tool, tool_input, result)
        
    def _clean_cache(self):
        """Remove entradas antigas do cache."""
        sorted_items = sorted(
            self._cache.items(),
            key=lambda x: x[1].get("timestamp", 0)
        )
        to_remove = len(sorted_items) // 2
        for key, _ in sorted_items[:to_remove]:
            del self._cache[key]
```

### 2. Cache Persistente
```python
class PersistentCacheHandler(CacheHandler):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._load_cache()
        
    def _load_cache(self):
        """Carrega cache do disco."""
        try:
            with open(self.file_path, "r") as f:
                self._cache = json.load(f)
        except FileNotFoundError:
            self._cache = {}
            
    def _save_cache(self):
        """Salva cache no disco."""
        with open(self.file_path, "w") as f:
            json.dump(self._cache, f)
            
    def write(self, tool: str, tool_input: str, result: Any):
        super().write(tool, tool_input, result)
        self._save_cache()
```

## Melhores Práticas

### 1. Gerenciamento de Cache
- Limite tamanho máximo
- Implemente expiração
- Monitore uso de memória

### 2. Chaves de Cache
- Use formato consistente
- Inclua versão se necessário
- Valide formato

### 3. Invalidação
- Defina política clara
- Implemente limpeza
- Monitore hit rate

## Considerações Técnicas

### 1. Performance
- Cache eficiente
- Otimização de memória
- Serialização rápida

### 2. Persistência
- Backup regular
- Recuperação de falhas
- Migração de dados

### 3. Monitoramento
- Hit rate
- Uso de memória
- Tempo de resposta

## Exemplos Avançados

### 1. Cache Distribuído
```python
class DistributedCacheTools(CacheTools):
    def __init__(self, redis_url: str):
        super().__init__()
        self.redis = Redis.from_url(redis_url)
        
    def hit_cache(self, key: str) -> Any:
        # Usa Redis como backend
        value = self.redis.get(key)
        if value:
            return pickle.loads(value)
        return None
```

### 2. Cache com TTL
```python
class TTLCacheTools(CacheTools):
    def __init__(self, ttl: int = 3600):
        super().__init__()
        self.ttl = ttl
        
    def hit_cache(self, key: str) -> Any:
        value = super().hit_cache(key)
        if value and self._is_expired(value):
            self.cache_handler._cache.pop(key)
            return None
        return value
        
    def _is_expired(self, value: Any) -> bool:
        timestamp = value.get("timestamp", 0)
        return time.time() - timestamp > self.ttl
```

### 3. Cache com Prioridade
```python
class PriorityCacheTools(CacheTools):
    def __init__(self, max_size: int = 1000):
        super().__init__()
        self.max_size = max_size
        self.priorities = {}
        
    def hit_cache(self, key: str) -> Any:
        value = super().hit_cache(key)
        if value:
            self.priorities[key] = self.priorities.get(key, 0) + 1
        return value
        
    def _clean_cache(self):
        """Remove entradas com menor prioridade."""
        sorted_items = sorted(
            self.priorities.items(),
            key=lambda x: x[1]
        )
        for key, _ in sorted_items[:len(sorted_items)//2]:
            del self.cache_handler._cache[key]
            del self.priorities[key]
```

## Conclusão
O sistema de cache do CrewAI fornece uma implementação flexível e eficiente para otimização de performance através de caching. Sua arquitetura permite diferentes estratégias de cache e é facilmente extensível para atender a necessidades específicas de diferentes cenários de uso.
