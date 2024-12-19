"""
Calendar test suite using CrewAI and Composio Tools.
This is an alternative implementation using crewai_tools.ComposioTool.
"""

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from crewai_tools import ComposioTool
from composio import Action, App
import logging
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import pytz

# Configurar logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s')

load_dotenv()

class CalendarCrewTools:
    def __init__(self):
        self.calendar_actions = [
            Action.GOOGLECALENDAR_QUICK_ADD,
            Action.GOOGLECALENDAR_LIST_EVENTS,
            Action.GOOGLECALENDAR_CREATE_EVENT,
            Action.GOOGLECALENDAR_UPDATE_EVENT,
            Action.GOOGLECALENDAR_DELETE_EVENT
        ]
        self.tools = [ComposioTool.from_action(action=action) for action in self.calendar_actions]
        self.timezone = pytz.timezone('America/Sao_Paulo')
        logging.info("CalendarCrewTools iniciado com sucesso")

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
            tools=self.tools,
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


if __name__ == "__main__":
    # Exemplo de uso
    crew_tools = CalendarCrewTools()
    result = crew_tools.process_message("Agende uma reunião amanhã às 14h")
    print(f"Resultado: {result}")
