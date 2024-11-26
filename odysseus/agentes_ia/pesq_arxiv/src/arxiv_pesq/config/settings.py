# Configurações de controle para os agentes
CONTROLES_ARXIV = """
NÍVEIS DE CONTROLE:
1. Entonação: Formal Científico.
2. Foco de Tópico: Você deve reponder sempre com alto foco no texto do artigo científico.
3. Língua: Responda sempre em Português do Brasil como os Brasileiros costumam escrever textos científicos aderindo aos padrões de redação científica do país a não ser o que será especificado para não traduzir.
4. Controle de Sentimento: Neutro e científico. Evite superlativos como: inovador, revolucionário e etc.
5. Nível Originalidade: 10, onde 1 é pouco original e 10 é muito original. Em hipótese alguma copie frases do texto original.
6. Nível de Abstração: 1, onde 1 é muito concreto e real e 10 é muito abstrado e irreal.
7. Tempo Verbal: Escreva no passado.
"""

RESTRICOES_ARXIV = """
O QUE NÃO DEVE SER TRADUZIDO DO INGLÊS PARA PORTUGUÊS:
1. Termos técnicos em inglês amplamente aceitos e usado nos textos em português.
2. Nome de algoritmos de machine learning.
3. Métricas usadas no trabalho.
4. Nome dos datasets.
5. Não envolva o retorno do YAML com ```yaml.
6. Não coloque ``` nem ´´´ no texto de retorno.
"""

SOLICITACOES_ARXIV = """
1 - OBJETIVOS - Identificação dos Objetivos: Realize uma análise cuidadosa do conteúdo do trabalho para extrair os objetivos principais. Resuma esses objetivos em um parágrafo claro e conciso, capturando a essência das metas e intenções do estudo.

2 - GAP - Identificação do GAP: Analise o conteúdo do trabalho para identificar o GAP científico que ele aborda, mesmo que não esteja explicitamente mencionado. Formule um parágrafo conciso, focando em destacar a questão central que o estudo procura resolver ou elucidar.

3 - METODOLOGIA - Extração Detalhada da Metodologia do Trabalho: Identificação e Descrição da Metodologia: Proceda com uma análise minuciosa do trabalho para identificar a metodologia utilizada. Detalhe cada aspecto da metodologia, incluindo o desenho do estudo, as técnicas e ferramentas empregadas, os procedimentos de coleta e análise de dados, os passos do método e quaisquer metodologias específicas ou inovadoras adotadas. Formule uma descrição compreensiva em texto corrido, limitando-se a um máximo de 250 palavras para manter a concisão sem sacrificar detalhes importantes.

4 - DATASET - Identifique os datasets usados no trabalho. Descreva-os brevemente em texto corrido, limitando-se a 40 palavras. Quero somente o nome dos dataset na mesma linha e separados por virgula. Se o dataset foi criado pelos autores escreve "OWN DATASET"

5 - RESULTADOS - Escreva em um parágrafo os resultados obitidos estudo dando enfase a dados quantitativos, quero dados numéricos explicitamente. Nesse paragrafo também dê enfase a comparação ao melhor trabalho anterior em relação ao trabalho proposto. Não use superlativos. Deixe o tom neuro e científico.

6 - LIMITAÇÕES - Produza um texto parafraseado das limitações do trabalho.

7 - CONCLUSÃO - Resuma as conclusões dos autores em relação ao trabalho.

8 - FUTURO - Extraia as Recomendações para Pesquisa Futura: Aponte recomendações para futuras investigações baseadas nas conclusões do artigo.

9 - AVALIAÇÃO - Faça uma avalição crítica ao trabalho. Não seja generalista faça uma crítica aprofundada.
"""

# Template para o Pesquisador do Arxiv
TEMPLATE_PESQUISADOR_ARXIV = """
ARTIGO:
    TÍTULO: "Título completo do artigo"
    LINK: "URL do artigo no Arxiv"
    RESUMO: "Breve resumo do abstract"
    JUSTIFICATIVA:
        - Por que este artigo parece promissor para trading
        - Indicações preliminares de viabilidade para backtesting
        - Tipo de dados/mercados mencionados
"""

# Template para o Leitor de PDF do Arxiv
TEMPLATE_LEITOR_PDF_ARXIV = """
ANÁLISE_DETALHADA:
    OBJETIVOS: "Objetivo geral e específicos"
    GAP: "Gap científico"
    METODOLOGIA: "Metodologia"
    DATASET: "Datasets utilizados"
    RESULTADOS: "Resultados do artigo"
    LIMITAÇÕES: "Limitações do artigo científico"
    CONCLUSÃO: "Conclusões"
    FUTURO: "Recomendações para pesquisas futuras"
    AVALIAÇÃO: "Análise crítica do artigo"
"""

# Critérios para o Pesquisador do Arxiv
CRITERIOS_PESQUISADOR_ARXIV = """
CRITÉRIOS DE SELEÇÃO:
1. Relevância para Trading:
   - Aplicabilidade prática em estratégias de trading
   - Menção a backtesting ou validação quantitativa
   - Uso de dados de mercado reais

2. Atualidade:
   - Priorizar artigos de 2023-2024
   - Considerar relevância das referências

3. Viabilidade:
   - Indicações de metodologia reproduzível
   - Menção a dados acessíveis
   - Potencial para implementação prática
"""