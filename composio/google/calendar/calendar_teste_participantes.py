from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet
import os
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s')

load_dotenv()

def criar_evento_com_participantes():
    composio_toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
    
    # Criar ferramenta para criar evento
    tools = composio_toolset.get_tools(actions=['GOOGLECALENDAR_CREATE_EVENT'])
    
    agent = Agent(
        role="Calendar Assistant",
        goal="Create a meeting with participants",
        backstory="You are an AI assistant that creates calendar events",
        verbose=True,
        tools=tools,
        llm=ChatOpenAI(temperature=0),
    )
    
    # Criar tarefa para criar evento com participantes
    task = Task(
        description="Create a team meeting tomorrow at 2pm with title 'Team Planning' and description 'Weekly planning meeting' with two participants: test1@example.com and test2@example.com",
        agent=agent,
        expected_output="Event created successfully"
    )
    
    crew = Crew(
        agents=[agent],
        tasks=[task]
    )
    
    result = crew.kickoff()
    print(f"\nResponse: {result}")
    return result

if __name__ == "__main__":
    criar_evento_com_participantes()
