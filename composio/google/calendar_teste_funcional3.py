from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet, Action, App
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz

load_dotenv()

class CalendarAgent:
    def __init__(self):
        self.composio_toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
        self.timezone = pytz.timezone('America/New_York')
        
        # Initialize tools for all calendar actions
        self.tools = self.composio_toolset.get_tools(
            actions=[
                'GOOGLECALENDAR_QUICK_ADD',
                'GOOGLECALENDAR_LIST_CALENDARS',
                'GOOGLECALENDAR_FIND_EVENT',
                'GOOGLECALENDAR_DELETE_EVENT',
                'GOOGLECALENDAR_UPDATE_EVENT',
                'GOOGLECALENDAR_CREATE_EVENT',
                'GOOGLECALENDAR_GET_CURRENT_DATE_TIME',
                'GOOGLECALENDAR_GET_CALENDAR',
                'GOOGLECALENDAR_PATCH_CALENDAR',
                'GOOGLECALENDAR_DUPLICATE_CALENDAR',
                'GOOGLECALENDAR_FIND_FREE_SLOTS',
                'GOOGLECALENDAR_REMOVE_ATTENDEE'
            ]
        )
        
        # Define the main agent
        self.agent = Agent(
            role="Calendar Assistant",
            goal="""You are an AI assistant specialized in managing Google Calendar. 
                   Your job is to help users manage their calendar efficiently.""",
            backstory="""You are a helpful calendar assistant that understands natural 
                        language and helps users manage their Google Calendar. You can create
                        events, find existing events, update or delete events, and list available calendars.
                        Always format responses in a user-friendly way.""",
            verbose=True,
            tools=self.tools,
            llm=ChatOpenAI(temperature=0),
        )

    def process_request(self, user_message: str) -> str:
        """Process user message and return appropriate response"""
        task = Task(
            description=f"Process the following calendar request: {user_message}",
            expected_output="A user-friendly response about the calendar operation",
            agent=self.agent
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )

        try:
            result = crew.kickoff()
            return str(result)
        except Exception as e:
            return f"Sorry, an error occurred: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Basic test
    calendar_agent = CalendarAgent()
    test_messages = [
        "Create a meeting tomorrow at 2pm with title 'Team Sync' and description 'Weekly team sync meeting'",
        "What events do I have today?",
        "Show my calendars",
        "Find events for next week",
        "Delete my meeting tomorrow"
    ]
    
    for msg in test_messages:
        print(f"\nTesting: {msg}")
        response = calendar_agent.process_request(msg)
        print(f"Response: {response}")



"""
Criação de Evento ✅
Funcionou corretamente
Criou o evento "Team Sync" para amanhã às 14h
Busca de Eventos ❌
Problema: Está usando datas fixas erradas (2023-10-25)
Deveria usar a data atual (2024-12-12)
Por isso não está encontrando os eventos
Listagem de Calendários ✅
Funcionou corretamente
Mostrou todos os calendários disponíveis
Eventos da Próxima Semana ❌
Problema: Está passando "next week" como string literal
Precisa converter para datas reais
Deleção de Evento ❌
Problema: Também está usando datas fixas erradas (2023-10-10)
Não está realmente encontrando e deletando o evento que criamos
Falta testar as outra funcionalidades"""