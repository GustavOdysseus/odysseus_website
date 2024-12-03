# Documentação da Interface Storage

## Visão Geral

A classe `Storage` define a interface base para todos os sistemas de armazenamento no CrewAI. Esta interface estabelece o contrato mínimo que todas as implementações de storage devem seguir, garantindo consistência e interoperabilidade entre diferentes tipos de armazenamento.

## Estrutura da Interface

```python
from typing import Any, Dict, List

class Storage:
    """Abstract base class defining the storage interface"""
```

### Tipos de Dados
- `Any`: Tipo genérico para valores flexíveis
- `Dict[str, Any]`: Dicionário para metadados
- `List[Any]`: Lista para resultados de busca

## Métodos da Interface

### 1. Salvamento

```python
def save(self, value: Any, metadata: Dict[str, Any]) -> None:
    """
    Salva um valor com seus metadados associados no storage.
    
    Args:
        value (Any): O valor a ser armazenado
        metadata (Dict[str, Any]): Metadados associados ao valor
    """
    pass
```

#### Características:
- Aceita qualquer tipo de valor
- Suporta metadados estruturados
- Não retorna valor
- Operação síncrona

### 2. Busca

```python
def search(
    self,
    query: str,
    limit: int,
    score_threshold: float
) -> Dict[str, Any] | List[Any]:
    """
    Busca valores no storage baseado em uma query.
    
    Args:
        query (str): String de busca
        limit (int): Número máximo de resultados
        score_threshold (float): Pontuação mínima para resultados
        
    Returns:
        Dict[str, Any] | List[Any]: Resultados da busca
    """
    return {}
```

#### Características:
- Busca por string
- Limitação de resultados
- Filtragem por score
- Retorno flexível

### 3. Reset

```python
def reset(self) -> None:
    """
    Reinicializa o storage, limpando todos os dados.
    """
    pass
```

#### Características:
- Limpa todos os dados
- Não retorna valor
- Operação destrutiva
- Sem parâmetros

## Implementação

### 1. Exemplo Básico

```python
class SimpleStorage(Storage):
    def __init__(self):
        self._data = {}
        
    def save(self, value: Any, metadata: Dict[str, Any]) -> None:
        key = str(len(self._data))
        self._data[key] = {"value": value, "metadata": metadata}
        
    def search(
        self,
        query: str,
        limit: int,
        score_threshold: float
    ) -> List[Any]:
        results = []
        for item in self._data.values():
            if query.lower() in str(item["value"]).lower():
                results.append(item)
                if len(results) >= limit:
                    break
        return results
        
    def reset(self) -> None:
        self._data.clear()
```

### 2. Implementação com Cache

```python
class CachedStorage(Storage):
    def __init__(self):
        self._data = {}
        self._cache = {}
        
    def save(self, value: Any, metadata: Dict[str, Any]) -> None:
        key = str(len(self._data))
        self._data[key] = {"value": value, "metadata": metadata}
        self._cache.clear()  # Invalida cache
        
    def search(
        self,
        query: str,
        limit: int,
        score_threshold: float
    ) -> List[Any]:
        cache_key = f"{query}:{limit}:{score_threshold}"
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        results = []
        for item in self._data.values():
            if query.lower() in str(item["value"]).lower():
                results.append(item)
                if len(results) >= limit:
                    break
                    
        self._cache[cache_key] = results
        return results
        
    def reset(self) -> None:
        self._data.clear()
        self._cache.clear()
```

## Melhores Práticas

### 1. Implementação
- Implemente todos os métodos
- Mantenha consistência de tipos
- Gerencie erros adequadamente
- Documente comportamentos

### 2. Dados
- Valide entradas
- Sanitize dados
- Gerencie recursos
- Implemente cache

### 3. Performance
- Otimize buscas
- Limite resultados
- Implemente índices
- Gerencie memória

## Considerações de Design

### 1. Flexibilidade
- Interface minimalista
- Tipos genéricos
- Retornos flexíveis
- Metadados extensíveis

### 2. Consistência
- Operações atômicas
- Estados consistentes
- Validações uniformes
- Comportamento previsível

### 3. Extensibilidade
- Fácil extensão
- Baixo acoplamento
- Alta coesão
- Reutilização

## Segurança

### 1. Validação
- Valide entradas
- Sanitize dados
- Limite tamanhos
- Verifique tipos

### 2. Recursos
- Limite memória
- Gerencie conexões
- Implemente timeouts
- Limpe recursos

## Extensibilidade

### 1. Novos Tipos
- Herde da interface
- Mantenha contrato
- Adicione features
- Documente mudanças

### 2. Melhorias
- Cache inteligente
- Índices otimizados
- Compressão
- Distribuição

## Conclusão

A interface `Storage` fornece:

1. Contrato mínimo
2. Flexibilidade máxima
3. Extensibilidade natural
4. Consistência garantida

Esta interface é crucial para:
- Implementações consistentes
- Interoperabilidade
- Extensibilidade
- Manutenibilidade

O design equilibra:
- Simplicidade
- Flexibilidade
- Performance
- Segurança

## Notas de Desenvolvimento

### Limitações Atuais
- Tipagem genérica
- Sem validações
- Métodos síncronos
- Interface mínima

### Próximos Passos
1. Validações padrão
2. Métodos assíncronos
3. Eventos/Hooks
4. Métricas/Logging
