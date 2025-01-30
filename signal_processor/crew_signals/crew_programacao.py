from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew, before_kickoff
from tools.vectorbt_get_talib_indicators import TALibAvailableIndicatorsTool
from tools.vectorbt_get_talib_params import TALibIndicatorParamsTool
from tools.vectorbt_pro_knowledge_tool import VectorBTKnowledgeTool
from crewai_tools import FileWriterTool

import yaml
import os
from dotenv import load_dotenv
import json



@CrewBase
class CrewProgramacao:
    """Crew para programação de estratégias de trading algorítmico"""

    def __init__(self):
        super().__init__()
        load_dotenv()

        # Configuração da LLM
        self.gemini_llm = LLM(
            model="gemini-2.0-flash",
            api_key=os.getenv("API_KEY_GEMINI"),
            temperature=0.7,
            max_tokens=8192
        )

        # Carrega configurações de agentes e tarefas
        with open("config/programacao/agents.yaml", "r", encoding="utf-8") as f:
            self.agents_programacao_config = yaml.safe_load(f)
        with open("config/geral/agents.yaml", "r", encoding="utf-8") as f:
            self.agents_general_config = yaml.safe_load(f)
        with open("config/programacao/tasks.yaml", "r", encoding="utf-8") as f:
            self.tasks_programacao_config = yaml.safe_load(f)
        with open("config/geral/tasks.yaml", "r", encoding="utf-8") as f:
            self.tasks_general_config = yaml.safe_load(f)

        # Carrega as expressões VectorBT predefinidas a partir de um arquivo .txt
        with open("docs/expressoes_validas_exemplos.txt", "r", encoding="utf-8") as f:
            self.exemplos_estrategia = f.read()

        # Mapeamento de ferramentas
        self.tools_map = {
            "talib_available_indicators_tool": TALibAvailableIndicatorsTool(),
            "talib_indicator_params_tool": TALibIndicatorParamsTool(),
            "vectorbt_pro_knowledge_tool": VectorBTKnowledgeTool(),
            "file_writer_tool": FileWriterTool()
        }

        self._task_inputs = {}

    @before_kickoff
    def prepare_inputs(self, inputs):
        """Prepara os inputs antes da execução da crew"""
        self._task_inputs = inputs
        return inputs

    @agent
    def vbt_pro_specialist(self) -> Agent:
        """Especialista de implementação e uso do VectorBT PRO"""
        config = self.agents_general_config["agents"]["vbt_pro_specialist"]
        if "tools" in config:
            config["tools"] = [self.tools_map[tool] for tool in config["tools"]]
        return Agent(config=config)

    def vbt_dev_manager(self) -> Agent:
        """Gerente de Desenvolvimento de Software"""
        config = self.agents_programacao_config["agents"]["vbt_dev_manager"]
        return Agent(config=config)

    @agent
    def vbt_pro_programmer(self) -> Agent:
        """Programador de VectorBT PRO"""
        config = self.agents_programacao_config["agents"]["vbt_pro_programmer"]
        if "tools" in config:
            config["tools"] = [self.tools_map[tool] for tool in config["tools"]]
        return Agent(config=config, code_execution_mode='unsafe')

    @agent
    def vbt_code_reviewer(self) -> Agent:
        """Analista de Revisão de Código"""
        config = self.agents_programacao_config["agents"]["vbt_code_reviewer"]
        if "tools" in config:
            config["tools"] = [self.tools_map[tool] for tool in config["tools"]]
        return Agent(config=config)

    @task
    def provide_vbt_expertise(self) -> Task:
        """Task: Fornecer conhecimento técnico sobre recursos do VectorBT PRO"""
        config = self.tasks_general_config["tasks"]["provide_vbt_expertise"]
        if "tools" in config:
            config["tools"] = [self.tools_map[tool] for tool in config["tools"]]
        return Task(config = config)

    @task
    def implement_vbt_code(self) -> Task:
        """Task: Implementação de Código VectorBT PRO"""
        config = self.tasks_programacao_config["tasks"]["implement_vbt_code"]
        if "tools" in config:
            config["tools"] = [self.tools_map[tool] for tool in config["tools"]]
        return Task(config = config)

    @task
    def review_vbt_code(self) -> Task:
        """Task: Revisão de Código VectorBT PRO"""
        config = self.tasks_programacao_config["tasks"]["review_vbt_code"]
        if "tools" in config:
            config["tools"] = [self.tools_map[tool] for tool in config["tools"]]
        return Task(config = config)

    @task
    def save_vbt_code(self) -> Task:
        """Task: Salvar o código VectorBT PRO implementado e sua documentação"""
        config = self.tasks_programacao_config["tasks"]["save_vbt_code"]
        if "tools" in config:
            config["tools"] = [self.tools_map[tool] for tool in config["tools"]]
        return Task(config=config)


    @task
    def dynamic_vbt_task(self) -> Task:
        """Task: Tarefa Dinâmica VectorBT PRO"""
        return Task(
            description=self._task_inputs.get("task_description", ""),  # Corrigir aqui
            expected_output=self._task_inputs.get("task_output", ""),  # Corrigir aqui
            name=self._task_inputs.get("task_name", "")               # Corrigir aqui
        )

    @crew
    def crew(self) -> Crew:
        """Configura a Crew"""
        return Crew(
            agents=self.agents,  # Coleta automática pelo decorator @agent
            tasks=self.tasks,   # Coleta automática pelo decorator @task
            process=Process.hierarchical,
            verbose=True,
            memory=True,
            manager_agent=self.vbt_dev_manager(),
            planning=True,
            llm=self.gemini_llm,
            output_log_file="crew_programacao/crew_bt.log"
        )

if __name__ == "__main__":
    crew_pg = CrewProgramacao()
    inputs = {
        "task_description": "Implementar indicador RSI customizado",
        "task_output": "Código Python do indicador RSI customizado com documentação",
        "task_name": "Implementar Indicador RSI Customizado"
    }
    result = crew_pg.crew().kickoff(inputs=inputs)
    print(result)