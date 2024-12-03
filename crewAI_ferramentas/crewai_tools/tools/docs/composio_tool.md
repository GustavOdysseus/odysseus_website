# Ferramenta Composio - Documentação

## Descrição
A Ferramenta Composio é um wrapper para ferramentas Composio que permite a integração perfeita de ações Composio no ecossistema CrewAI. Ela fornece funcionalidade para executar ações Composio com tratamento de autenticação e validação de parâmetros.

## Principais Recursos

### Integração de Ações
- Encapsulamento de ação Composio
- Gerenciamento de autenticação
- Validação de parâmetros
- Geração dinâmica de esquema
- Tratamento de execução de ações

### Métodos de Criação de Ferramentas
1. **A partir de Ação**
   - Encapsulamento direto de ação
   - Validação de esquema
   - Verificação de autenticação
   - Tratamento de parâmetros

2. **A partir de Aplicativo**
   - Criação de múltiplas ações
   - Filtragem baseada em tags
   - Filtragem por caso de uso
   - Geração em lote de ferramentas

## Componentes do Sistema

### 1. Funcionalidade Principal
- Wrapper de execução de ação
- Verificação de autenticação
- Geração de esquema
- Validação de parâmetros

### 2. Autenticação
- Verificação de conta conectada
- Autenticação específica do aplicativo
- Gerenciamento de autorização
- Validação de conexão

## Exemplo de Uso

```python
# Criar ferramenta a partir de uma única ação
ferramenta = ComposioTool.from_action(
    action="nome_acao",
    entity_id="id_entidade_personalizado"
)

# Criar ferramentas a partir de aplicativo com tags
ferramentas = ComposioTool.from_app(
    "nome_aplicativo",
    tags=["tag1", "tag2"],
)

# Criar ferramentas a partir de aplicativo com caso de uso
ferramentas = ComposioTool.from_app(
    "nome_aplicativo",
    use_case="caso_uso_especifico"
)

# Executar ação
resultado = ferramenta.run(**parametros_acao)
```

## Características Técnicas
- Geração dinâmica de esquema
- Validação de tipo
- Tratamento de erros
- Gerenciamento de autenticação
- Processamento de parâmetros

## Requisitos
- Instalação do Composio
- Autenticação válida
- Configuração de contas conectadas
- Suporte a type hints Python

## Recursos Especiais
- Geração automática de esquema
- Verificação de autenticação
- Validação de parâmetros
- Múltiplos modos de criação de ferramentas
- Filtragem por caso de uso e tag

## Limitações e Considerações
- Requer configuração do Composio
- Dependências de autenticação
- Compatibilidade de esquema
- Regras de validação de parâmetros
- Requisitos de conexão

## Notas
- Verificar configuração de autenticação
- Tratar erros de conexão
- Validar parâmetros
- Considerar compatibilidade de esquema
- Monitorar execução de ações
- Testar status de autenticação
- Tratar múltiplas ferramentas adequadamente
