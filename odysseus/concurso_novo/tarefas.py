from crewai import Task
from typing import List
from agentes import AgentesPortugues

class TarefasAnalise:
    def __init__(self, caminho_pdf: str):
        self.caminho_pdf = caminho_pdf
        self.agentes = AgentesPortugues()

    def criar_tarefa_leitura(self) -> Task:
        """Cria tarefa para leitura do PDF"""
        return Task(
            description=f"""
            1. Leia o arquivo PDF em {self.caminho_pdf}
            2. Extraia todas as questões de português
            3. Organize cada questão em um formato estruturado com:
               - Texto base (se houver)
               - Enunciado
               - Alternativas
               - Resposta correta
            4. Mantenha a formatação original do texto
            """,
            agent=self.agentes.criar_agente_leitor()
        )

    def criar_tarefa_analise_gramatical(self) -> Task:
        """Cria tarefa para análise gramatical"""
        return Task(
            description="""
            1. Analise cada questão identificando:
               - Regras gramaticais abordadas
               - Exceções gramaticais
               - Níveis de dificuldade
            2. Categorize as questões por tópicos gramaticais
            3. Identifique padrões de erro comuns nas alternativas
            """,
            agent=self.agentes.criar_agente_analista_gramatical()
        )

    def criar_tarefa_analise_interpretacao(self) -> Task:
        """Cria tarefa para análise de interpretação"""
        return Task(
            description="""
            1. Analise aspectos de interpretação como:
               - Tipos de inferência
               - Relações de coesão e coerência
               - Figuras de linguagem
               - Argumentação
            2. Identifique níveis de complexidade interpretativa
            3. Categorize as questões por habilidades requeridas
            """,
            agent=self.agentes.criar_agente_analista_interpretacao()
        )

    def criar_tarefa_padronizacao(self) -> Task:
        """Cria tarefa para identificação de padrões"""
        return Task(
            description="""
            1. Analise os padrões identificados nas questões:
               - Estruturas comuns de questões
               - Temas recorrentes
               - Tipos de abordagem mais frequentes
            2. Crie uma classificação das questões por padrões
            3. Identifique tendências e preferências da banca
            """,
            agent=self.agentes.criar_agente_padronizador()
        )
