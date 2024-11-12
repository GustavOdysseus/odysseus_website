import os
import time
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq

# Configuração da chave de API (substitua com sua chave Groq API)
os.environ["GROQ_API_KEY"] = "sua_chave_groq_api"

# Limite de requisições por minuto e intervalo entre requisições
REQUESTS_PER_MINUTE = 1
INTERVAL = 60 / REQUESTS_PER_MINUTE  # Intervalo mínimo entre as requisições em segundos

# Configuração do modelo de LLM (Llama3–70B da Groq)
llm = ChatGroq(
    temperature=0,
    model_name="groq/llama3-8b-8192",
    api_key=os.environ["GROQ_API_KEY"]
)

# Configuração do modelo de LLM do gerente
manager_llm = ChatGroq(
    temperature=0,
    model_name="groq/llama3-8b-8192",
    api_key=os.environ["GROQ_API_KEY"]
)

# Solicita entradas do usuário para o número de agentes, rodadas e descrição do problema
num_agents = int(input("Digite o número de agentes debatendo: "))
num_rounds = int(input("Digite o número de rodadas de debate: "))
problem_description = input("Digite a descrição do problema a ser debatido: ")

# Agente Gerente - Consolida o resultado final após o debate
manager_agent = Agent(
    llm=llm,
    role='Gerente',
    goal='Consolidar as respostas dos agentes e resolver o problema',
    backstory="Você é o gerente dos agentes debatedores, que sempre responde em português brasileiro, responsável por consolidar a solução final.",
    verbose=True
)

# Função auxiliar para criar cada agente debatedor
def create_debating_agent(agent_id, problem_description):
    return Agent(
        llm=llm,
        role=f'Agente{agent_id}',
        goal=f"Resolver o problema: {problem_description}",
        backstory=f"Você é um debatedor, que sempre responde em português brasileiro, focado em resolver o problema: {problem_description}.",
        verbose=True
    )

# Lista de agentes debatedores
debating_agents = [create_debating_agent(i, problem_description) for i in range(1, num_agents + 1)]

# Função callback para aplicar o atraso após cada tarefa
def rate_limited_callback(output):
    print(f"[{output.agent.role}] Resumo: {output.raw_output}")
    time.sleep(INTERVAL)  # Aplica o intervalo definido entre cada tarefa

# Tarefas de debate para cada agente em cada rodada
debate_tasks = []
for round_num in range(num_rounds):
    for agent in debating_agents:
        debate_tasks.append(
            Task(
                description=f"Rodada {round_num + 1} de debate para resolver: {problem_description}",
                expected_output="Solução ou opinião atualizada para o problema.",
                agent=agent,
                async_execution=True,
                callback=rate_limited_callback  # Aplica o callback com controle de taxa
            )
        )

# Tarefa de Consolidação pelo Gerente após o debate
consolidation_task = Task(
    description="Consolidação final das soluções dos agentes.",
    expected_output="Solução consolidada para o problema proposto.",
    agent=manager_agent,
    callback=lambda output: print(f"[Gerente] Solução consolidada final: {output.raw_output}")
)

# Configuração da Crew com os agentes e as tarefas
crew = Crew(
    agents=[manager_agent] + debating_agents,
    tasks=debate_tasks + [consolidation_task],
    process=Process.hierarchical,  # Processamento hierárquico para consolidar a solução ao final
    manager_llm=manager_llm,  # Adiciona o manager_llm para gerenciar o processo hierárquico
    verbose=True,
)

# Inicialização do fluxo de trabalho com execução das tarefas com controle de taxa
crew_result = crew.kickoff()

# Exibe o resultado final consolidado
print("Resultado consolidado da Crew:", crew_result)
