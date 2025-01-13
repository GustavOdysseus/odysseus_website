Esta equipe garante que as estratégias desenvolvidas e testadas no CrewAI respeitem estritamente as diretrizes de risco e retorno estabelecidas em [[Metas e Restrições]].

## Responsabilidades

- **Monitoramento Contínuo do Risco:**  
    Avalia indicadores como alavancagem, drawdown, perda diária e exposição total ao risco, utilizando dados e resultados fornecidos pela [[Equipe de Análise Quantitativa]] e métricas obtidas via [[VectorBT Pro]].
    
- **Verificação de Conformidade:**  
    Assegura que a estratégia não ultrapasse os limites de risco definidos (por exemplo, drawdown máximo ou perda diária máxima). Caso ocorram violações, a equipe comunica imediatamente o [[Comitê de Estratégia (Núcleo Central)]].
    
- **Feedback ao Fluxo:**  
    Caso as metas de risco não sejam atingidas, essa equipe sinaliza a necessidade de ajustes no [[Fluxo Iterativo]], retornando às equipes de dados, análise ou pesquisa para correções ou refinamentos.
    

## Integração com o CrewAI

- **Gatilhos Condicionais:**  
    Métricas de risco podem funcionar como condições dentro do CrewAI para decidir se o fluxo segue adiante ou retorna a estágios anteriores.
    
- **Memória de Riscos Históricos:**  
    A equipe pode registrar o histórico de violações e ajustes na memória do CrewAI, criando um registro de evolução do perfil de risco da estratégia.