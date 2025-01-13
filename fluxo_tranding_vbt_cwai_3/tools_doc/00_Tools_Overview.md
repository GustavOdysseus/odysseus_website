# CrewAI Tools - Visão Geral

## Introdução
O sistema de ferramentas do CrewAI é uma arquitetura modular e extensível que permite que agentes executem ações específicas. Este documento serve como índice e visão geral de todos os componentes do sistema.

## Arquitetura
O sistema de ferramentas é composto por várias camadas:

1. **Ferramentas Base**
   - `BaseTool`: Classe base abstrata que define a interface fundamental para todas as ferramentas
   - `StructuredTool`: Implementação que integra com o ecossistema LangChain

2. **Sistema de Chamadas**
   - `ToolCalling`: Gerencia como as ferramentas são invocadas
   - `ToolUsage`: Controla a execução e ciclo de vida das ferramentas

3. **Ferramentas Especializadas**
   - `AgentTools`: Ferramentas para interação entre agentes
   - `CacheTools`: Sistema de cache para otimização

4. **Sistemas de Suporte**
   - Sistema de eventos para monitoramento
   - Telemetria para análise de uso
   - Cache para otimização de performance

## Documentação Detalhada

1. [Ferramentas Base](01_Base_Tool.md)
   - Estrutura fundamental
   - Sistema de tipos e validação
   - Integração com LangChain

2. [Ferramentas Estruturadas](02_Structured_Tool.md)
   - Implementação customizada
   - Sistema de argumentos
   - Validação de esquema

3. [Sistema de Chamadas](03_Tool_Calling.md)
   - Formatos de chamada
   - Parsing de argumentos
   - Tratamento de erros

4. [Gerenciamento de Uso](04_Tool_Usage.md)
   - Ciclo de vida das ferramentas
   - Sistema de cache
   - Telemetria e eventos

5. [Ferramentas de Agente](05_Agent_Tools.md)
   - Delegação de trabalho
   - Comunicação entre agentes
   - Gerenciamento de contexto

6. [Ferramentas de Cache](06_Cache_Tools.md)
   - Sistema de cache
   - Otimização de performance
   - Estratégias de invalidação

## Guias Práticos

1. [Criando Novas Ferramentas](guides/Creating_New_Tools.md)
2. [Melhores Práticas](guides/Best_Practices.md)
3. [Padrões de Design](guides/Design_Patterns.md)

## Referências
- [Documentação API](api_reference.md)
- [Exemplos](examples.md)
- [FAQ](faq.md)
