from crewai import Agent, Task, Crew, Process
from langchain.tools import DuckDuckGoSearchRun
from typing import List, Dict, Any
import vectorbt as vbt
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

search_tool = DuckDuckGoSearchRun()

class TradingSystem:
    def __init__(self):
        # Inicializa os agentes principais
        self.research_agent = Agent(
            role='Pesquisador de Mercado',
            goal='Identificar oportunidades de mercado e analisar tendências',
            backstory='Especialista em análise de mercado com forte base quantitativa',
            tools=[search_tool],
            verbose=True,
            allow_delegation=True
        )

        self.strategy_agent = Agent(
            role='Desenvolvedor de Estratégias',
            goal='Criar e otimizar estratégias de trading baseadas em pesquisa',
            backstory='Quant trader com experiência em desenvolvimento de algoritmos',
            tools=[search_tool],
            verbose=True,
            allow_delegation=True
        )

        self.validation_agent = Agent(
            role='Validador de Estratégias',
            goal='Testar e validar estratégias usando backtesting e análise de risco',
            backstory='Especialista em gestão de risco e validação quantitativa',
            tools=[search_tool],
            verbose=True,
            allow_delegation=True
        )

    def create_research_tasks(self, market_context: Dict[str, Any]) -> List[Task]:
        """Cria tarefas de pesquisa baseadas no contexto de mercado"""
        tasks = []
        
        # Tarefa de análise de mercado
        market_analysis = Task(
            description=f"""
            Analise o mercado {market_context['market']} considerando:
            - Ativos: {market_context['assets']}
            - Horizonte temporal: {market_context['timeframe']}
            - Métricas de interesse: {market_context['metrics']}
            
            Identifique:
            1. Tendências principais
            2. Correlações relevantes
            3. Anomalias ou oportunidades
            4. Riscos específicos
            """,
            agent=self.research_agent
        )
        tasks.append(market_analysis)

        # Tarefa de pesquisa específica
        specific_research = Task(
            description=f"""
            Realize pesquisa aprofundada sobre:
            - Tópicos: {market_context['research_topics']}
            - Foco em: {market_context['focus_areas']}
            
            Produza:
            1. Insights principais
            2. Modelos quantitativos relevantes
            3. Recomendações práticas
            """,
            agent=self.research_agent
        )
        tasks.append(specific_research)

        return tasks

    def create_strategy_tasks(self, research_results: Dict[str, Any]) -> List[Task]:
        """Cria tarefas de desenvolvimento de estratégia baseadas nos resultados da pesquisa"""
        tasks = []

        # Tarefa de desenvolvimento de estratégia
        strategy_development = Task(
            description=f"""
            Desenvolva estratégias baseadas em:
            - Insights: {research_results['insights']}
            - Modelos: {research_results['models']}
            
            Crie:
            1. Regras de entrada/saída
            2. Parâmetros de otimização
            3. Filtros de mercado
            4. Gestão de risco inicial
            """,
            agent=self.strategy_agent
        )
        tasks.append(strategy_development)

        # Tarefa de otimização
        strategy_optimization = Task(
            description=f"""
            Otimize as estratégias considerando:
            - Métricas alvo: {research_results['target_metrics']}
            - Restrições: {research_results['constraints']}
            
            Defina:
            1. Parâmetros ótimos
            2. Ajustes de risco
            3. Filtros refinados
            """,
            agent=self.strategy_agent
        )
        tasks.append(strategy_optimization)

        return tasks

    def create_validation_tasks(self, strategies: Dict[str, Any]) -> List[Task]:
        """Cria tarefas de validação para as estratégias desenvolvidas"""
        tasks = []

        # Tarefa de backtesting
        backtesting = Task(
            description=f"""
            Realize backtesting completo:
            - Estratégias: {strategies['rules']}
            - Períodos: {strategies['periods']}
            
            Analise:
            1. Performance histórica
            2. Drawdowns
            3. Métricas de risco
            4. Robustez
            """,
            agent=self.validation_agent
        )
        tasks.append(backtesting)

        # Tarefa de análise de risco
        risk_analysis = Task(
            description=f"""
            Analise riscos detalhadamente:
            - Métricas: {strategies['risk_metrics']}
            - Cenários: {strategies['scenarios']}
            
            Avalie:
            1. VaR e CVaR
            2. Stress tests
            3. Correlações de risco
            4. Exposições específicas
            """,
            agent=self.validation_agent
        )
        tasks.append(risk_analysis)

        return tasks

    def execute_flow(self, market_context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa o fluxo completo do sistema de trading"""
        
        # 1. Criação da crew
        crew = Crew(
            agents=[self.research_agent, self.strategy_agent, self.validation_agent],
            tasks=[],
            process=Process.sequential
        )

        # 2. Execução da pesquisa
        research_tasks = self.create_research_tasks(market_context)
        crew.tasks = research_tasks
        research_results = crew.kickoff()

        # 3. Desenvolvimento de estratégia
        strategy_tasks = self.create_strategy_tasks(research_results)
        crew.tasks = strategy_tasks
        strategies = crew.kickoff()

        # 4. Validação
        validation_tasks = self.create_validation_tasks(strategies)
        crew.tasks = validation_tasks
        validation_results = crew.kickoff()

        # 5. Compilação dos resultados
        final_results = {
            'research': research_results,
            'strategies': strategies,
            'validation': validation_results
        }

        return final_results

# Exemplo de uso
if __name__ == "__main__":
    # Configuração do contexto de mercado
    market_context = {
        'market': 'Crypto',
        'assets': ['BTC', 'ETH', 'SOL'],
        'timeframe': '1h',
        'metrics': ['volume', 'volatility', 'momentum'],
        'research_topics': ['market microstructure', 'on-chain metrics'],
        'focus_areas': ['liquidity analysis', 'whale behavior']
    }

    # Inicialização e execução
    trading_system = TradingSystem()
    results = trading_system.execute_flow(market_context)

    # Implementação das estratégias validadas usando VectorBT
    def implement_strategy(strategy_config: Dict[str, Any]):
        # Obter dados
        symbols = strategy_config['assets']
        timeframe = strategy_config['timeframe']
        
        data = {}
        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='1y', interval=timeframe)
            data[symbol] = hist['Close']
        
        # Criar DataFrame
        df = pd.DataFrame(data)
        
        # Implementar estratégia usando VectorBT
        entries = vbt.signals.generate_random_entries(len(df), n=10)
        exits = vbt.signals.generate_random_exits(entries)
        
        pf = vbt.Portfolio.from_signals(
            df,
            entries,
            exits,
            init_cash=100000,
            fees=0.001
        )
        
        return pf

    # Implementar estratégias validadas
    for strategy in results['strategies']:
        portfolio = implement_strategy(strategy)
        # Análise de performance
        stats = portfolio.stats()
        print(f"Strategy Performance:\n{stats}")
