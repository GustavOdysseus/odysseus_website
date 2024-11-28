# Documentação Avançada: CrewAI Translations

## Visão Geral

O sistema de traduções do CrewAI é um componente essencial que permite a internacionalização do framework. Ele fornece suporte para múltiplos idiomas e permite que os agentes se comuniquem em diferentes línguas.

## Estrutura

### 1. Arquivos de Tradução

#### 1.1 Formato Base (en.json)
- Template principal em inglês
- Base para outras traduções
- Estrutura JSON padronizada

#### 1.2 Outros Idiomas
- Português (pt.json)
- Estrutura idêntica ao en.json
- Traduções mantêm contexto original

### 2. Componentes

#### 2.1 Mensagens de Sistema
- Instruções para agentes
- Mensagens de erro
- Comunicações padrão

#### 2.2 Templates de Agente
- Descrições de papel
- Instruções de tarefa
- Formatos de resposta

## Implementação

### 1. Carregamento de Traduções
```python
class TranslationLoader:
    def __init__(self, language: str = "en"):
        self.language = language
        self.translations = self._load_translations()

    def _load_translations(self) -> dict:
        # Carrega arquivo de tradução baseado no idioma
        pass
```

### 2. Uso em Agentes
```python
class Agent:
    def __init__(self, language: str = "en"):
        self.translator = TranslationLoader(language)
        
    def get_message(self, key: str) -> str:
        return self.translator.get(key)
```

## Extensões

### 1. Novos Idiomas
```json
{
    "agent_instructions": {
        "role_description": "...",
        "task_format": "...",
        "response_template": "..."
    }
}
```

### 2. Formatos Personalizados
```python
class CustomTranslation:
    def add_custom_template(self, key: str, template: str)
    def modify_existing_template(self, key: str, new_template: str)
```

## Melhores Práticas

### 1. Desenvolvimento
- Manter consistência entre idiomas
- Testar todas as traduções
- Documentar alterações

### 2. Manutenção
- Atualizar todos os idiomas
- Verificar formatação
- Manter backup das traduções

## Conclusão

O sistema de traduções é fundamental para:
1. Internacionalização do framework
2. Flexibilidade de comunicação
3. Consistência entre idiomas
4. Extensibilidade do sistema
