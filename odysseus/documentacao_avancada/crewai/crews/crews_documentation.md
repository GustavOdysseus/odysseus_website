# Documentação Avançada: CrewAI Crews

## Visão Geral

O módulo `crews` é um componente fundamental do CrewAI que gerencia a saída e os resultados das operações realizadas por crews (equipes de agentes). Este módulo fornece estruturas de dados robustas para representar e manipular os resultados do processamento de tarefas.

## Estrutura do Módulo

```
crews/
├── __init__.py
└── crew_output.py
```

## Componentes Principais

### 1. CrewOutput

A classe `CrewOutput` é o componente central deste módulo, responsável por encapsular e gerenciar os resultados produzidos por um crew.

#### Estrutura Base
```python
class CrewOutput(BaseModel):
    raw: str = Field(
        description="Raw output of crew",
        default=""
    )
    pydantic: Optional[BaseModel] = Field(
        description="Pydantic output of Crew",
        default=None
    )
    json_dict: Optional[Dict[str, Any]] = Field(
        description="JSON dict output of Crew",
        default=None
    )
    tasks_output: list[TaskOutput] = Field(
        description="Output of each task",
        default=[]
    )
    token_usage: UsageMetrics = Field(
        description="Processed token summary",
        default={}
    )
```

#### Funcionalidades Principais

1. **Acesso a JSON**
```python
@property
def json(self) -> Optional[str]:
    """
    Retorna a saída em formato JSON se disponível
    Raises:
        ValueError: Se o formato de saída da última tarefa não for JSON
    """
    if self.tasks_output[-1].output_format != OutputFormat.JSON:
        raise ValueError(
            "No JSON output found in the final task. Please make sure to set the output_json property in the final task in your crew."
        )
    return json.dumps(self.json_dict)
```

2. **Conversão para Dicionário**
```python
def to_dict(self) -> Dict[str, Any]:
    """
    Converte a saída para formato de dicionário
    Prioriza json_dict sobre pydantic
    """
    output_dict = {}
    if self.json_dict:
        output_dict.update(self.json_dict)
    elif self.pydantic:
        output_dict.update(self.pydantic.model_dump())
    return output_dict
```

3. **Acesso a Atributos**
```python
def __getitem__(self, key):
    """
    Permite acesso a atributos via sintaxe de dicionário
    Prioriza pydantic sobre json_dict
    """
    if self.pydantic and hasattr(self.pydantic, key):
        return getattr(self.pydantic, key)
    elif self.json_dict and key in self.json_dict:
        return self.json_dict[key]
    else:
        raise KeyError(f"Key '{key}' not found in CrewOutput.")
```

## Padrões de Uso

### 1. Criação Básica
```python
output = CrewOutput(
    raw="Resultado do processamento",
    tasks_output=[task1_output, task2_output],
    token_usage={"total_tokens": 150}
)
```

### 2. Uso com Modelo Pydantic
```python
class ResultModel(BaseModel):
    status: str
    data: Dict[str, Any]

result_model = ResultModel(
    status="success",
    data={"processed": True}
)

output = CrewOutput(
    raw="Processamento concluído",
    pydantic=result_model,
    tasks_output=[task_output]
)
```

### 3. Uso com JSON
```python
output = CrewOutput(
    raw="Dados processados",
    json_dict={
        "status": "success",
        "data": {
            "processed": True,
            "timestamp": "2024-01-20T10:00:00Z"
        }
    },
    tasks_output=[task_output]
)

# Acesso via propriedade json
json_str = output.json

# Acesso via dicionário
data = output["data"]
```

## Melhores Práticas

### 1. Gerenciamento de Saída
- Sempre fornecer saída raw para fallback
- Preferir modelos Pydantic para validação
- Manter consistência no formato JSON

### 2. Manipulação de Dados
- Usar to_dict() para conversões seguras
- Validar formato antes do acesso
- Tratar exceções adequadamente

### 3. Métricas de Uso
- Rastrear uso de tokens
- Agregar métricas por tarefa
- Monitorar performance

## Considerações Técnicas

### 1. Performance
- Lazy loading de JSON
- Caching de conversões
- Otimização de memória

### 2. Validação
- Verificação de tipos
- Validação de esquema
- Tratamento de erros

### 3. Extensibilidade
- Suporte a novos formatos
- Customização de saída
- Integração com sistemas

## Extensões Potenciais

### 1. Formatos Adicionais
```python
class EnhancedCrewOutput(CrewOutput):
    def to_xml(self) -> str:
        # Conversão para XML
        pass
        
    def to_yaml(self) -> str:
        # Conversão para YAML
        pass
```

### 2. Validação Avançada
```python
class ValidatedCrewOutput(CrewOutput):
    def validate_schema(self, schema: Dict[str, Any]) -> bool:
        # Validação de esquema
        pass
        
    def validate_content(self) -> bool:
        # Validação de conteúdo
        pass
```

### 3. Métricas Detalhadas
```python
class MetricsEnhancedCrewOutput(CrewOutput):
    def detailed_metrics(self) -> Dict[str, Any]:
        # Métricas detalhadas
        pass
        
    def performance_analysis(self) -> Dict[str, Any]:
        # Análise de performance
        pass
```

## Conclusão

O módulo `crews` é um componente essencial que:
1. Gerencia resultados de processamento
2. Fornece múltiplos formatos de saída
3. Facilita acesso e manipulação de dados
4. Suporta extensibilidade

Este módulo é crucial para:
- Padronização de saída
- Validação de dados
- Rastreamento de métricas
- Integração com sistemas externos
