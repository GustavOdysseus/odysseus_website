"""
Calendar Crew implementation using CrewAI.
This module contains the agent definitions and crew orchestration for calendar operations.
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
import logging
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent.parent.parent)
import sys
sys.path.append(root_dir)

from composio.google.calendar.calendar_teste_completo import CalendarTestSuite

# Configurar logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s')

load_dotenv()

if not os.getenv('OPENAI_API_KEY'):
    raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")

class CalendarCrew:
    def __init__(self):
        self.calendar_suite = CalendarTestSuite()
        logging.info("CalendarCrew iniciado com sucesso")

    def create_interpreter_agent(self):
        logging.info("Criando agente interpretador")
        return Agent(
            role="Natural Language Interpreter",
            goal="Understand user intent and extract calendar operations",
            backstory="You are an AI that understands natural language and converts it into calendar actions. You should identify which calendar action is needed and provide a clear description of what needs to be done.",
            llm=ChatOpenAI(
                api_key=os.getenv('OPENAI_API_KEY'),
                model="gpt-4o-mini",
                temperature=0
            ),
        )

    def create_calendar_agent(self):
        logging.info("Criando agente do calendário")
        return Agent(
            role="Calendar Manager",
            goal="Execute calendar operations based on user requests",
            backstory="You manage calendar operations efficiently using the available calendar actions. You receive a description of what needs to be done and execute it using the appropriate calendar action.",
            tools=self.calendar_suite.composio_toolset.get_tools(actions=self.calendar_suite.all_actions),
            llm=ChatOpenAI(
                api_key=os.getenv('OPENAI_API_KEY'),
                model="gpt-4o-mini",
                temperature=0
            ),
        )

    def process_message(self, message: str):
        logging.info(f"Processando mensagem: {message}")
        interpreter = self.create_interpreter_agent()
        calendar_agent = self.create_calendar_agent()

        interpret_task = Task(
            description=f"Analyze this user message and determine which calendar action is needed: '{message}'. Return a clear description of what needs to be done.",
            agent=interpreter
        )

        calendar_task = Task(
            description="Execute the calendar operation based on the interpretation provided",
            agent=calendar_agent
        )

        crew = Crew(
            agents=[interpreter, calendar_agent],
            tasks=[interpret_task, calendar_task],
            process=Process.sequential
        )

        logging.info("Iniciando execução da crew")
        result = crew.kickoff()
        logging.info(f"Resultado da execução: {result}")
        return result
