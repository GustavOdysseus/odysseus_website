Este fluxo descreve o processo cíclico de desenvolvimento e validação de estratégias, integrado ao CrewAI. Cada etapa pode ser representada como uma tarefa (Task) executada por um ou mais agentes especializados, seguindo as orientações do [[Comitê de Estratégia (Núcleo Central)]] e atendendo às [[Metas e Restrições]]. O [[VectorBT Pro]] atua como a ferramenta central, enquanto o CrewAI orquestra as equipes e tarefas, utilizando memória, condicionais e integrações com dados externos.







1. **Definição de Objetivos**  
    O [[Comitê de Estratégia (Núcleo Central)]] estabelece metas (lucro alvo, drawdown máximo, perda diária máxima), seleciona o tipo de ativo (Forex ou Cripto) e comunica as [[Metas e Restrições]] a todas as equipes.
    
2. **Preparação de Dados**  
    A [[Equipe de Dados e Integração]] obtém dados históricos (>=5 anos), limpa e normaliza. Essa tarefa garante que o agente responsável pelo backtesting receba dados consistentes e padronizados, prontos para análise no [[VectorBT Pro]].
    
3. **Contexto de Mercado**  
    A [[Equipe de Inteligência de Mercado e Sentimento]] adiciona contexto macroeconômico, eventos geopolíticos e sentimento de mercado, enriquecendo a memória do CrewAI. Essa informação auxilia os agentes de análise e pesquisa a considerar condições reais e atuais.
    
4. **Proposição de Modelos Avançados**  
    A [[Equipe de Pesquisa Quantitativa e Acadêmica]] sugere abordagens teóricas, indicadores inovadores, modelos de machine learning ou insights de estudos acadêmicos. Essas propostas tornam-se insumos para o agente de análise quanti aplicar no [[VectorBT Pro]].
    
5. **Análise Quantitativa e Backtesting**  
    A [[Equipe de Análise Quantitativa]]:
    
    - Utiliza o [[VectorBT Pro]] para gerar indicadores e rodar [[Backtesting]].
    - Otimiza parâmetros buscando atender às metas estabelecidas em [[Metas e Restrições]].
    - Avalia resultados e envia métricas (lucro, drawdown, volatilidade) de volta ao Comitê e à Equipe de Gestão de Riscos.
6. **Automação e Ferramentas**  
    A [[Equipe de Programação e Ferramentas]]:
    
    - Desenvolve integrações, pipelines e scripts para executar backtests e análises de forma automatizada.
    - Gera relatórios (JSON, CSV, gráficos) e garante que as ferramentas estejam prontas para rodar sob demanda (tarefas agendadas ou condicionais no CrewAI).
7. **Verificação de Riscos e Compliance**  
    A [[Equipe de Gestão de Riscos e Compliance]]:
    
    - Monitora se a estratégia atende aos limites de drawdown, perda diária, alavancagem e outras restrições.
    - Caso identifique falhas, notifica o [[Comitê de Estratégia (Núcleo Central)]] para ajustes. Caso esteja tudo conforme o esperado, autoriza continuar.
8. **Decisão Estratégica Final**  
    O [[Comitê de Estratégia (Núcleo Central)]]:
    
    - Se os resultados não atendem às metas, solicita nova iteração no fluxo, voltando para a coleta de dados, análise ou pesquisa.
    - Se resultados satisfatórios são obtidos, finaliza o ciclo, aprovando o salvamento da estratégia.
9. **Salvamento de Dados e Documentação**  
    A [[Equipe de Programação e Ferramentas]] e a [[Equipe de Análise Quantitativa]]:
    
    - Salvam parâmetros, dados de backtesting, relatórios finais (JSON, CSV) e gráficos.
    - Documentam a estratégia aprovada, permitindo histórico e rastreabilidade, mantendo o CrewAI atualizado sobre o estado final da estratégia.