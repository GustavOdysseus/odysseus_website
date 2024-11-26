import os
from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from decouple import config
from textwrap import dedent
from pathlib import Path

from core.agents import CustomAgents
from core.tasks import CustomTasks

os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")
#os.environ["OPENAI_ORGANIZATION"] = config("OPENAI_ORGANIZATION_ID")

class DebateCrew:
    def __init__(self, num_agentes: int, num_rodadas: int, problema: str, config_path: str = None):
        self.num_agentes = num_agentes
        self.num_rodadas = num_rodadas
        self.problema = problema
        
        # Permite configurar o caminho dos arquivos YAML
        if config_path is None:
            config_path = Path(__file__).parent / 'config'
            
        self.agents = CustomAgents(config_path=config_path)
        self.tasks = CustomTasks(config_path=config_path)

    def run(self):
        # Criando debatedores
        debatedores = []
        for i in range(1, self.num_agentes + 1):
            debatedor = self.agents.create_debating_agent(
                agent_id=i,
                problem_description=self.problema
            )
            debatedores.append(debatedor)

        # Criando agente gerente
        gerente = self.agents.manager_agent()

        # Criando tarefas de debate
        tarefas_debate = []
        for rodada in range(self.num_rodadas):
            for i in range(1, self.num_agentes + 1):
                tarefa = self.tasks.debate_task(
                    agent=debatedores[i-1],
                    rodada=rodada,
                    i=i
                )
                tarefas_debate.append(tarefa)

        # Tarefa final de consolidação
        tarefa_consolidacao = self.tasks.consolidation_task(
            agent=gerente
        )

        # Formando a crew de debate
        crew = Crew(
            agents=debatedores + [gerente],
            tasks=tarefas_debate + [tarefa_consolidacao],
            process=Process.sequential,
            verbose=True
        )

        # Iniciando o debate
        resultado = crew.kickoff()
        return resultado


if __name__ == "__main__":
    print("## Bem-vindo ao Sistema de Debate com IA")
    print("----------------------------------------")
    
    num_agentes = int(input(dedent("""Número de debatedores: """)))
    num_rodadas = int(input(dedent("""Número de rodadas: """)))
    problema = input(dedent("""Descreva o problema a ser debatido: """))

    debate_crew = DebateCrew(
        num_agentes=num_agentes,
        num_rodadas=num_rodadas,
        problema=problema
    )
    
    resultado = debate_crew.run()
    
    print("\n\n########################")
    print("## Resultado Final do Debate:")
    print("########################\n")
    print(resultado)
