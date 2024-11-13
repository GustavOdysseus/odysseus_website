from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from tools.calculator_tool import CalculatorTool
from tools.sec_tools import SEC10KTool, SEC10QTool

from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool, TXTSearchTool

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

@CrewBase
class StockAnalysisCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def financial_agent(self) -> Agent:
        return Agent(
            role="Analista Financeiro",
            goal="Analisar profundamente os dados financeiros e métricas da empresa",
            backstory="Você é um analista financeiro experiente com vasto conhecimento em análise fundamentalista",
            verbose=True,
            allow_delegation=False,
            llm=llm,
            tools=[
                ScrapeWebsiteTool(),
                WebsiteSearchTool(),
                CalculatorTool(),
                SEC10QTool("AMZN"),
                SEC10KTool("AMZN"),
            ]
        )
    
    @task
    def financial_analysis(self) -> Task: 
        return Task(
            description="Realize uma análise financeira completa da empresa, incluindo métricas importantes como P/L, crescimento do LPA, tendências de receita e relação dívida/patrimônio",
            expected_output="Um relatório detalhado sobre a saúde financeira da empresa, incluindo análise de métricas chave e comparação com concorrentes",
            agent=self.financial_agent(),
        )

    @agent
    def research_analyst_agent(self) -> Agent:
        return Agent(
            role="Analista de Pesquisa",
            goal="Pesquisar e analisar informações de mercado e notícias sobre a empresa",
            backstory="Você é um analista de pesquisa com experiência em análise de mercado e tendências",
            verbose=True,
            allow_delegation=False,
            llm=llm,
            tools=[
                ScrapeWebsiteTool(),
                SEC10QTool("AMZN"),
                SEC10KTool("AMZN"),
            ]
        )
    
    @task
    def research(self) -> Task:
        return Task(
            description="Colete e analise informações de mercado, notícias relevantes e tendências do setor",
            expected_output="Um relatório abrangente sobre as últimas notícias, mudanças no sentimento do mercado e potenciais impactos no valor da ação",
            agent=self.research_analyst_agent(),
        )
    
    @agent
    def financial_analyst_agent(self) -> Agent:
        return Agent(
            role="Analista Financeiro Senior",
            goal="Realizar análise aprofundada de documentos financeiros e métricas avançadas",
            backstory="Você é um analista financeiro senior especializado em análise de documentos SEC e métricas avançadas",
            verbose=True,
            allow_delegation=False,
            llm=llm,
            tools=[
                ScrapeWebsiteTool(),
                WebsiteSearchTool(),
                CalculatorTool(),
                SEC10QTool(),
                SEC10KTool(),
            ]
        )
    
    @task
    def filings_analysis(self) -> Task:
        return Task(
            description="Analise detalhadamente os relatórios 10-K e 10-Q mais recentes, focando em informações críticas e riscos",
            expected_output="Um relatório detalhado destacando descobertas significativas dos documentos SEC, incluindo riscos e oportunidades",
            agent=self.financial_analyst_agent(),
        )

    @agent
    def investment_advisor_agent(self) -> Agent:
        return Agent(
            role="Consultor de Investimentos",
            goal="Fornecer recomendações de investimento baseadas em análises completas",
            backstory="Você é um consultor de investimentos experiente especializado em recomendações estratégicas",
            verbose=True,
            allow_delegation=False,
            llm=llm,
            tools=[
                ScrapeWebsiteTool(),
                WebsiteSearchTool(),
                CalculatorTool(),
            ]
        )

    @task
    def recommend(self) -> Task:
        return Task(
            description="Forneça uma recomendação detalhada de investimento baseada em todas as análises anteriores",
            expected_output="Uma recomendação clara e bem fundamentada, incluindo estratégia de investimento e principais pontos de atenção",
            agent=self.investment_advisor_agent(),
        )
    
    @crew
    def crew(self) -> Crew:
        """Cria a Equipe de Análise de Ações"""
        return Crew(
            agents=self.agents,  
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
