from crewai import Agent
from textwrap import dedent
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import yaml
from langchain_ollama import OllamaLLM
from pathlib import Path

load_dotenv()

# This is an example of how to define custom agents.
# You can define as many agents as you want.
# You can also define custom tasks in tasks.py
class CustomAgents:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'config'
            print(f"Procurando configuração em: {config_path}")
        else:
            config_path = Path(config_path)
        
        config_file = config_path / 'agents.yaml'
        if not config_file.exists():
            alt_path = Path(__file__).parent.parent.parent / 'config'
            if (alt_path / 'agents.yaml').exists():
                config_file = alt_path / 'agents.yaml'
            else:
                raise FileNotFoundError(f"Arquivo de configuração não encontrado em: {config_file} nem em {alt_path}")
        
        with open(config_file, 'r', encoding='utf-8') as file:
            self.agents_config = yaml.safe_load(file)
            
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4MINI = ChatOpenAI(model_name="gpt-4o-mini", temperature=1.4)
        self.Ollama = OllamaLLM(model="openhermes")

    # Agente Gerente - Consolida o resultado final após o debate
    def manager_agent(self):
        moderador_config = self.agents_config['moderador']
        return Agent(
            role=moderador_config['role'],
            goal=moderador_config['goal'],
            backstory=moderador_config['backstory'],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4MINI,
        )

    # Função auxiliar para criar cada agente debatedor
    def create_debating_agent(self, agent_id, problem_description):
        debater_config = self.agents_config['debatedores']
        
        return Agent(
            role=debater_config['role'].format(agent_id=agent_id),
            goal=debater_config['goal'].format(problem_description=problem_description),
            backstory=debater_config['backstory'].format(problem_description=problem_description),
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4MINI,
        )
