from crewai import Crew, Task, Agent, Process
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
import os
import yaml
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
from tools import FetchMarketDataTool, ValidateComplianceTool, CalculateMetricsTool, FetchAcademicReferencesTool, FetchHistoricalDataTool

def load_yaml(file_path: str) -> dict:
    """Utility function to load YAML configuration files."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    with open(file_path, "r") as file:
        try:
            data = yaml.safe_load(file)
            if not isinstance(data, dict):
                raise ValueError(f"Invalid YAML format: Expected a dictionary but got {type(data)}")
            return data
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file {file_path}: {str(e)}")


# Load environment variables
load_dotenv()

@CrewBase
class ModularStrategyCrew:
    """
    Dynamically builds a crew using YAML configurations and modular methods.
    """

    agents_config_path = "config/agents.yaml"
    tasks_config_path = "config/tasks.yaml"
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

    def __init__(self):
        self.agents_config = load_yaml(self.agents_config_path)
        self.tasks_config = load_yaml(self.tasks_config_path)

    @agent
    def strategy_committee(self) -> Agent:
        """Creates the Strategy Committee agent."""
        return Agent(
            config=self.agents_config["strategy_committee"],
            llm=self.llm,
            memory=True,
            verbose=True,
            allow_delegation=True,
            cache=True
        )

    @agent
    def market_analysis(self) -> Agent:
        """Creates the Market Analysis agent."""
        market_tool = FetchMarketDataTool()  # Example of a tool
        return Agent(
            config=self.agents_config["market_analysis"],
            llm=self.llm,
            tools=[market_tool],
            verbose=True,
            cache=True,

        )

    @agent
    def quantitative_researcher(self) -> Agent:
        """Creates the Quantitative Researcher agent."""
        return Agent(
            config=self.agents_config["quantitative_researcher"],
            llm=self.llm,
            memory=True,
            verbose=True,
            cache=True,
        )

    @agent
    def data_analyst(self) -> Agent:
        """Creates the Data Analyst agent."""
        return Agent(
            config=self.agents_config["data_analyst"],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def risk_manager(self) -> Agent:
        """Creates the Risk Manager agent."""
        compliance_tool = ValidateComplianceTool()  # Example of a compliance tool
        return Agent(
            config=self.agents_config["risk_manager"],
            llm=self.llm,
            tools=[compliance_tool],
            verbose=True,
        )

    @task
    def define_goals(self) -> Task:
        """Task to define strategic goals."""
        return Task(config=self.tasks_config["define_goals"])

    @task
    def collect_market_data(self) -> Task:
        """Task to collect macro and microeconomic data."""
        return Task(config=self.tasks_config["collect_market_data"])

    @task
    def analyze_data(self) -> Task:
        """Task to analyze data and generate indicators."""
        return Task(config=self.tasks_config["analyze_data"])

    @task
    def prepare_historical_data(self) -> Task:
        """Task to collect and prepare historical data."""
        return Task(config=self.tasks_config["prepare_historical_data"])

    @task
    def validate_compliance(self) -> Task:
        """Task to validate compliance with policies."""
        return Task(config=self.tasks_config["validate_compliance"])

    @task
    def document_results(self) -> Task:
        """Task to document the final results."""
        return Task(config=self.tasks_config["document_results"])

    @crew
    def build(self) -> Crew:
        """Creates the Modular Strategy Crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
