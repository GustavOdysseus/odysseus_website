# Tool Calling - Documentação Detalhada

## Visão Geral
O arquivo `tool_calling.py` define as estruturas fundamentais para a chamada de ferramentas no framework CrewAI. Este módulo implementa dois modelos Pydantic que gerenciam como as ferramentas são invocadas pelos agentes.

## Estruturas Principais

### 1. Classe ToolCalling

```python
class ToolCalling(BaseModel):
    tool_name: str = Field(
        ..., 
        description="The name of the tool to be called."
    )
    arguments: Optional[Dict[str, Any]] = Field(
        ..., 
        description="A dictionary of arguments to be passed to the tool."
    )
```

#### Atributos
1. **tool_name** (str)
   - Nome da ferramenta a ser chamada
   - Campo obrigatório
   - Deve corresponder a uma ferramenta registrada no sistema

2. **arguments** (Optional[Dict[str, Any]])
   - Dicionário de argumentos para a ferramenta
   - Opcional, mas quando presente deve corresponder ao schema da ferramenta
   - Suporta tipos dinâmicos (Any)

### 2. Classe InstructorToolCalling

```python
class InstructorToolCalling(PydanticBaseModel):
    tool_name: str = PydanticField(
        ..., 
        description="The name of the tool to be called."
    )
    arguments: Optional[Dict[str, Any]] = PydanticField(
        ..., 
        description="A dictionary of arguments to be passed to the tool."
    )
```

#### Características
- Estrutura similar a `ToolCalling`
- Usa `PydanticBaseModel` e `PydanticField`
- Específica para uso com o módulo Instructor

## Uso e Funcionalidades

### 1. Chamada de Ferramentas Padrão
```python
tool_call = ToolCalling(
    tool_name="minha_ferramenta",
    arguments={
        "param1": "valor1",
        "param2": 123
    }
)
```

### 2. Chamada com Instructor
```python
instructor_call = InstructorToolCalling(
    tool_name="ferramenta_instructor",
    arguments={
        "input": "dados",
        "config": {"option": "value"}
    }
)
```

## Integração com o Sistema

### 1. Validação de Dados
- Validação automática de tipos através do Pydantic
- Verificação de campos obrigatórios
- Conversão automática de tipos quando possível

### 2. Fluxo de Execução
1. Agente decide usar uma ferramenta
2. Cria instância de ToolCalling/InstructorToolCalling
3. Sistema valida a chamada
4. Ferramenta é executada com argumentos fornecidos

## Melhores Práticas

### 1. Nomeação de Ferramentas
- Use nomes descritivos e únicos
- Mantenha consistência no padrão de nomeação
- Evite caracteres especiais ou espaços

### 2. Gestão de Argumentos
- Documente claramente os argumentos esperados
- Forneça valores padrão quando apropriado
- Valide tipos de dados críticos

### 3. Tratamento de Erros
- Verifique existência da ferramenta
- Valide argumentos antes da execução
- Forneça mensagens de erro claras

## Exemplos de Implementação

### 1. Chamada Simples
```python
# Chamada básica com um argumento
basic_call = ToolCalling(
    tool_name="calculadora",
    arguments={"operacao": "soma", "valores": [1, 2, 3]}
)
```

### 2. Chamada Complexa
```python
# Chamada com múltiplos argumentos e configurações
complex_call = ToolCalling(
    tool_name="processador_dados",
    arguments={
        "input_data": {"tipo": "csv", "caminho": "dados.csv"},
        "configuracoes": {
            "encoding": "utf-8",
            "delimiter": ",",
            "skip_rows": 1
        },
        "transformacoes": ["normalizar", "filtrar_nulos"]
    }
)
```

### 3. Chamada com Instructor
```python
# Chamada usando InstructorToolCalling
instructor_call = InstructorToolCalling(
    tool_name="analise_texto",
    arguments={
        "texto": "Exemplo de texto para análise",
        "opcoes": {
            "linguagem": "pt-br",
            "modo": "sentimentos"
        }
    }
)
```

## Considerações Técnicas

### 1. Performance
- Validação eficiente de tipos
- Baixo overhead de serialização
- Otimização de memória

### 2. Extensibilidade
- Fácil adição de novos campos
- Suporte a tipos personalizados
- Compatibilidade com futuras versões

### 3. Segurança
- Validação de entrada de dados
- Sanitização de argumentos
- Prevenção de injeção de código

## Integração com Outros Componentes

### 1. Sistema de Ferramentas
- Comunicação direta com BaseTool
- Compatibilidade com cache
- Suporte a telemetria

### 2. Agentes
- Interface clara para chamadas
- Feedback de execução
- Gestão de estado

### 3. Pipeline de Execução
- Integração com fluxo de trabalho
- Logging de chamadas
- Monitoramento de performance

## Conclusão
O módulo `tool_calling.py` fornece uma interface robusta e flexível para a chamada de ferramentas no CrewAI. Sua implementação baseada em Pydantic garante tipo-segurança e validação adequada, enquanto mantém a flexibilidade necessária para diferentes casos de uso. A distinção entre `ToolCalling` e `InstructorToolCalling` permite diferentes abordagens de integração, tornando o sistema adaptável a diversos cenários de uso.
