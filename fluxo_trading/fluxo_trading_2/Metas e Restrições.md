
As Metas e Restrições definem critérios quantitativos e qualitativos que as estratégias devem atender antes de serem consideradas aprovadas. Elas orientam todo o [[Fluxo Iterativo]], desde a coleta de dados até a análise final, garantindo que o desenvolvimento de estratégias esteja sempre alinhado aos objetivos de risco e retorno estabelecidos pelo [[Comitê de Estratégia (Núcleo Central)]].

## Critérios para Forex

- **Lucro Alvo Mensal:** 10%
- **Perda Diária Máxima:** 4%
- **Drawdown Máximo:** 10%
- **Tempo Mínimo de Backtesting:** 5 anos
- **Alavancagem Máxima:** 50x

## Critérios para Criptomoedas

- **Lucro Alvo Mensal:** 40%
- **Perda Diária Máxima:** 8%
- **Drawdown Máximo:** 20%
- **Tempo Mínimo de Backtesting:** 5 anos
- **Alavancagem Máxima:** 10x

## Importância no Fluxo e no CrewAI

- **Orientação das Equipes:**  
    Todas as equipes (Dados, Inteligência de Mercado, Pesquisa, Análise, Programação, Riscos) utilizam essas metas como referência. Por exemplo, a [[Equipe de Análise Quantitativa]] ajusta parâmetros e indicadores via [[VectorBT Pro]] para tentar atingir o lucro alvo e respeitar o drawdown máximo.
    
- **Critério de Aprovação Final:**  
    A [[Equipe de Gestão de Riscos e Compliance]] monitora constantemente se os limites de perda diária, drawdown e alavancagem são respeitados. Caso sejam excedidos, a estratégia é devolvida ao fluxo para ajustes. Apenas quando todos os critérios forem atendidos, o [[Comitê de Estratégia (Núcleo Central)]] aprova a finalização.
    
- **Interação com o CrewAI:**  
    Em um contexto de orquestração com o CrewAI, as Metas e Restrições são parâmetros-chave embutidos no contexto das tarefas e agentes. Isso assegura que cada iteração do fluxo — desde a coleta de dados até o backtesting e otimização — esteja alinhada a essas diretrizes, disparando condicionais que retornam à etapa anterior caso não sejam atingidas.
    
- **Iteração Contínua:**  
    Caso a estratégia não atinja as metas, o fluxo retorna a etapas anteriores, ajustando parâmetros, indicadores ou fontes de dados, em um ciclo contínuo até que a estratégia seja considerada robusta o suficiente.