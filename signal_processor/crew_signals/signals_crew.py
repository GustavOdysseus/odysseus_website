from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew, before_kickoff
from tools.vectorbt_get_talib_indicators import TALibAvailableIndicatorsTool
from tools.vectorbt_get_talib_params import TALibIndicatorParamsTool
from tools.vectorbt_pro_knowledge_tool import VectorBTProKnowledgeTool
from crewai_tools import FileWriterTool

import yaml
import os
from dotenv import load_dotenv
import json

@CrewBase
class CrewSignals:
    """Crew para geração e otimização de sinais de trading"""

    def __init__(self):
        super().__init__()
        load_dotenv()

        # Carrega configurações de agentes e tarefas
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, "agents.yaml"), "r", encoding="utf-8") as f:
            self.agents_signals_config = yaml.safe_load(f)
        with open(os.path.join(current_dir, "agents.yaml"), "r", encoding="utf-8") as f:
            self.agents_general_config = yaml.safe_load(f)
        with open(os.path.join(current_dir, "tasks.yaml"), "r", encoding="utf-8") as f:
            self.tasks_signals_config = yaml.safe_load(f)
        with open(os.path.join(current_dir, "tasks.yaml"), "r", encoding="utf-8") as f:
            self.tasks_general_config = yaml.safe_load(f)

        # Mapeamento de ferramentas
        self.tools_map = {
            "talib_available_indicators_tool": TALibAvailableIndicatorsTool(),
            "talib_indicator_params_tool": TALibIndicatorParamsTool(),
            "vectorbt_pro_knowledge_tool": VectorBTProKnowledgeTool(),
            "file_writer_tool": FileWriterTool()
        }

        self._task_inputs = {}

    @before_kickoff
    def prepare_inputs(self, inputs):
        """Prepara os inputs antes da execução da crew"""
        self._task_inputs = inputs
        return inputs

    @agent
    def signal_specialist(self) -> Agent:
        """Especialista em geração de sinais de trading"""
        config = self.agents_general_config["agents"]["signal_specialist"]
        tools = [self.tools_map[tool] for tool in config.get("tools", [])]
        return Agent(
            name=config["name"],
            role=config["role"],
            backstory=config["backstory"],
            goal=config["goals"][0],  # Usando o primeiro goal como principal
            tools=tools,
            allow_delegation=config.get("allow_delegation", True),
            verbose=config.get("verbose", True)
        )

    # Removido o decorador @agent do gerenciador
    def signals_manager(self) -> Agent:
        """Gerente de Sinais - Responsável por coordenar a geração e otimização de sinais"""
        config = self.agents_signals_config["agents"]["signals_manager"]
        tools = [self.tools_map[tool] for tool in config.get("tools", [])]
        return Agent(
            name=config["name"],
            role=config["role"],
            backstory=config["backstory"],
            goal=config["goals"][0],  # Usando o primeiro goal como principal
            tools=tools,
            allow_delegation=config.get("allow_delegation", True),
            verbose=config.get("verbose", True)
        )

    @agent
    def signal_optimizer(self) -> Agent:
        """Especialista em otimização de sinais"""
        config = self.agents_signals_config["agents"]["signal_optimizer"]
        tools = [self.tools_map[tool] for tool in config.get("tools", [])]
        return Agent(
            name=config["name"],
            role=config["role"],
            backstory=config["backstory"],
            goal=config["goals"][0],  # Usando o primeiro goal como principal
            tools=tools,
            allow_delegation=config.get("allow_delegation", True),
            verbose=config.get("verbose", True)
        )

    @agent
    def signal_validator(self) -> Agent:
        """Validador de sinais gerados"""
        config = self.agents_signals_config["agents"]["signal_validator"]
        tools = [self.tools_map[tool] for tool in config.get("tools", [])]
        return Agent(
            name=config["name"],
            role=config["role"],
            backstory=config["backstory"],
            goal=config["goals"][0],  # Usando o primeiro goal como principal
            tools=tools,
            allow_delegation=config.get("allow_delegation", True),
            verbose=config.get("verbose", True)
        )

    @task
    def generate_signals(self) -> Task:
        """Task: Gerar sinais de trading baseados em indicadores técnicos"""
        config = self.tasks_signals_config["tasks"]["generate_signals"]
        tools = [self.tools_map[tool] for tool in config.get("tools", [])]
        return Task(
            description=config["description"],
            expected_output=config["expected_output"],
            agent=self.signal_specialist(),
            tools=tools,
            async_execution=config.get("async_execution", False),
            priority=config.get("priority", 1)
        )

    @task
    def optimize_signals(self) -> Task:
        """Task: Otimizar sinais gerados"""
        config = self.tasks_signals_config["tasks"]["optimize_signals"]
        tools = [self.tools_map[tool] for tool in config.get("tools", [])]
        return Task(
            description=config["description"],
            expected_output=config["expected_output"],
            agent=self.signal_optimizer(),
            tools=tools,
            async_execution=config.get("async_execution", False),
            priority=config.get("priority", 2)
        )

    @task
    def validate_signals(self) -> Task:
        """Task: Validar sinais otimizados"""
        config = self.tasks_signals_config["tasks"]["validate_signals"]
        tools = [self.tools_map[tool] for tool in config.get("tools", [])]
        return Task(
            description=config["description"],
            expected_output=config["expected_output"],
            agent=self.signal_validator(),
            tools=tools,
            async_execution=config.get("async_execution", False),
            priority=config.get("priority", 3)
        )

    @task
    def dynamic_signal_task(self) -> Task:
        """Task: Tarefa Dinâmica para processamento de sinais"""
        return Task(
            description=self._task_inputs.get("task_description", ""),
            expected_output=self._task_inputs.get("task_output", ""),
            name=self._task_inputs.get("task_name", "")
        )

    @crew
    def crew(self) -> Crew:
        """Configura a Crew"""
        # Cria diretório para o log se não existir
        os.makedirs("crew_signals", exist_ok=True)
        
        return Crew(
            agents=self.agents,  # Coleta automática pelo decorator @agent
            tasks=self.tasks,   # Coleta automática pelo decorator @task
            process=Process.hierarchical,
            verbose=True,
            memory=True,
            manager_agent=self.signals_manager(),  # Manager não é um @agent
            planning=True,
            output_log_file="crew_signals/crew_signals.log"
        )

if __name__ == "__main__":
    crew_signals = CrewSignals()
    inputs = {
        "task_description": "Gerar sinais de trading usando RSI e Moving Average",
        "task_output": "Lista de sinais otimizados com seus respectivos parâmetros",
        "task_name": "generate_trading_signals"
    }
    result = crew_signals.crew().kickoff(inputs=inputs)
    print(result)