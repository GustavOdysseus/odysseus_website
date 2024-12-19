"""
Service Router for handling different Google service integrations.
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
import logging

from .calendar_crew import CalendarCrew
# Futuros imports:
# from .gmail_crew import GmailCrew
# from .drive_crew import DriveCrew

load_dotenv()
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s')

class ServiceRouter:
    """
    Routes user messages to appropriate service crews based on intent.
    """
    
    def __init__(self):
        self.calendar_crew = CalendarCrew()
        # Futuras instâncias:
        # self.gmail_crew = GmailCrew()
        # self.drive_crew = DriveCrew()
        
        # Mapping of services and their keywords
        self.service_mapping = {
            'calendar': [
                'calendar', 'schedule', 'event', 'meeting', 'appointment',
                'reminder', 'agenda', 'book', 'scheduling'
            ],
            'gmail': [
                'email', 'mail', 'gmail', 'message', 'send', 'inbox',
                'draft', 'compose'
            ],
            'drive': [
                'drive', 'file', 'document', 'folder', 'upload',
                'download', 'share', 'storage'
            ]
        }
        
    def create_router_agent(self):
        """Creates an agent to determine which service the user wants to use."""
        return Agent(
            role="Service Router",
            goal="Determine which Google service the user wants to interact with",
            backstory="""You are an AI that understands user intent and routes requests 
            to the appropriate Google service. You analyze messages to determine if they
            relate to Calendar, Gmail, Drive, or other services.""",
            tools=[],  # Router doesn't need tools, just makes decisions
            llm=ChatOpenAI(
                api_key=os.getenv('OPENAI_API_KEY'),
                model="gpt-4o-mini",
                temperature=0
            )
        )
        
    def process_message(self, message: str):
        """
        Process a user message and route it to the appropriate service crew.
        """
        logging.info(f"Router processing message: {message}")
        
        router = self.create_router_agent()
        
        routing_task = Task(
            description=f"""Analyze this message and determine which service it relates to: '{message}'
            Available services: calendar, gmail, drive
            Consider these aspects:
            1. Keywords and context in the message
            2. Type of action being requested
            3. Service-specific terminology
            
            Return ONLY the service name in lowercase, nothing else.""",
            agent=router
        )
        
        crew = Crew(
            agents=[router],
            tasks=[routing_task],
            process=Process.sequential
        )
        
        service = crew.kickoff().lower()
        logging.info(f"Detected service: {service}")
        
        # Route to appropriate crew
        if service == 'calendar':
            return self.calendar_crew.process_message(message)
        elif service == 'gmail':
            # Future implementation
            return "Gmail integration coming soon! Currently, I can only help with Calendar operations."
        elif service == 'drive':
            # Future implementation
            return "Drive integration coming soon! Currently, I can only help with Calendar operations."
        else:
            return f"Sorry, I don't recognize the service '{service}'. Currently, I can only help with Calendar operations."
