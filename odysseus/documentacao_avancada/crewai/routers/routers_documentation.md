# Documentação Avançada: CrewAI Routers

## Visão Geral

O sistema de roteamento do CrewAI é um componente sofisticado que permite o direcionamento dinâmico de fluxos de trabalho baseado em condições. Este sistema é fundamental para criar pipelines flexíveis e adaptáveis que podem mudar seu comportamento com base em diferentes inputs.

## Arquitetura

### 1. Componentes Principais

#### 1.1 Classe Route
```python
class Route(BaseModel):
    condition: Callable[[Dict[str, Any]], bool]
    pipeline: Any
```
- Define uma rota individual
- Contém uma condição e um pipeline associado
- Herda de Pydantic BaseModel para validação

#### 1.2 Classe Router
```python
class Router(BaseModel):
    routes: Dict[str, Route]
    default: Any
    _route_types: Dict[str, type]
```
- Gerencia múltiplas rotas
- Mantém um pipeline padrão
- Rastreia tipos de pipeline por rota

### 2. Funcionalidades Principais

#### 2.1 Adição de Rotas
```python
def add_route(
    self,
    name: str,
    condition: Callable[[Dict[str, Any]], bool],
    pipeline: Any,
) -> "Router"
```
- Adiciona novas rotas dinamicamente
- Valida a capacidade de cópia do pipeline
- Suporta encadeamento de métodos

#### 2.2 Roteamento
```python
def route(self, input_data: Dict[str, Any]) -> Tuple[Any, str]
```
- Avalia condições sequencialmente
- Retorna pipeline apropriado
- Inclui nome da rota utilizada

#### 2.3 Sistema de Cópia
```python
def copy(self) -> "Router"
```
- Cria cópias profundas do router
- Mantém independência entre instâncias
- Preserva condições e pipelines

## Implementação

### 1. Validação e Segurança

#### 1.1 Verificação de Copyable
```python
@staticmethod
def _check_copyable(obj: Any) -> None:
    if not hasattr(obj, "copy") or not callable(getattr(obj, "copy")):
        raise ValueError(f"Object of type {type(obj)} must have a 'copy' method")
```
- Garante que objetos são copiáveis
- Previne referências compartilhadas
- Lança erros descritivos

#### 1.2 Configuração Pydantic
```python
class Config:
    arbitrary_types_allowed = True
```
- Permite tipos arbitrários
- Mantém flexibilidade do sistema
- Suporta validação personalizada

### 2. Gerenciamento de Estado

#### 2.1 Rastreamento de Tipos
```python
_route_types: Dict[str, type] = PrivateAttr(default_factory=dict)
```
- Mantém registro de tipos
- Uso de atributos privados
- Facilita debugging

#### 2.2 Inicialização Segura
```python
def __init__(self, routes: Dict[str, Route], default: Any, **data):
    super().__init__(routes=routes, default=default, **data)
    self._check_copyable(default)
    for name, route in routes.items():
        self._check_copyable(route.pipeline)
        self._route_types[name] = type(route.pipeline)
```
- Validação na construção
- Inicialização de tipos
- Suporte a dados extras

## Padrões de Uso

### 1. Roteamento Básico
```python
router = Router(
    routes={
        "route1": Route(
            condition=lambda x: x["type"] == "A",
            pipeline=PipelineA()
        )
    },
    default=DefaultPipeline()
)
```

### 2. Roteamento Encadeado
```python
router.add_route(
    "route2",
    condition=lambda x: x["priority"] > 5,
    pipeline=HighPriorityPipeline()
).add_route(
    "route3",
    condition=lambda x: x["complexity"] == "high",
    pipeline=ComplexPipeline()
)
```

### 3. Execução de Rota
```python
pipeline, route_name = router.route({
    "type": "A",
    "priority": 7,
    "complexity": "high"
})
```

## Melhores Práticas

### 1. Design de Condições
- Manter condições simples e atômicas
- Evitar efeitos colaterais
- Priorizar performance

### 2. Gestão de Pipelines
- Implementar método copy()
- Manter independência
- Documentar comportamentos

### 3. Organização de Rotas
- Usar nomes descritivos
- Ordenar por prioridade
- Manter documentação atualizada

## Considerações Técnicas

### 1. Performance
- Avaliação sequencial de condições
- Overhead de cópia profunda
- Impacto de validação Pydantic

### 2. Manutenibilidade
- Estrutura modular
- Facilidade de extensão
- Debuggability

### 3. Escalabilidade
- Suporte a múltiplas rotas
- Flexibilidade de tipos
- Extensibilidade do sistema

## Conclusão

O sistema de roteamento do CrewAI é um componente fundamental que:
1. Permite fluxos de trabalho dinâmicos
2. Mantém isolamento entre pipelines
3. Suporta extensão e personalização
4. Garante segurança e consistência

Este sistema é crucial para a flexibilidade e adaptabilidade do framework, permitindo comportamentos complexos e personalizados baseados em condições específicas.
