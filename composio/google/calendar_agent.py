from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet
import logging
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import pytz
import json

logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s')

load_dotenv()

class CalendarAgent:
    def __init__(self):
        self._api_key = os.getenv("COMPOSIO_API_KEY")
        if not self._api_key:
            raise ValueError("COMPOSIO_API_KEY não encontrada nas variáveis de ambiente")
            
        self.composio_toolset = ComposioToolSet(api_key=self._api_key)
        self.timezone = pytz.timezone('America/Sao_Paulo')
        
        self.actions = [
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

    def find_event_by_summary(self, summary: str) -> dict:
        """Find an event by its summary/title"""
        try:
            tools = self.composio_toolset.get_tools(actions=['GOOGLECALENDAR_FIND_EVENT'])
            result = tools[0].run({"calendar_id": "primary", "q": summary})
            
            if result.get('successfull'):
                events = result.get('data', {}).get('events', [])
                return events[0] if events else None
            return None
        except Exception as e:
            logging.error(f"Error finding event: {str(e)}")
            return None

    def process_request(self, user_message: str) -> str:
        """Process a user request and return the result"""
        try:
            tools = self.composio_toolset.get_tools(actions=self.actions)
            
            agent = Agent(
                role="Assistente de Calendário",
                goal="Gerenciar eventos e compromissos no Google Calendar de forma eficiente",
                backstory="""Sou um assistente especializado em gerenciar calendários do Google. 
                Posso ajudar com:
                - Criação, atualização e remoção de eventos
                - Busca de horários livres
                - Gerenciamento de participantes
                - Configurações do calendário
                - Duplicação de calendários""",
                verbose=True,
                tools=tools,
                llm=ChatOpenAI(temperature=0),
            )
            
            # Tratamento especial para remoção de participantes
            if "remova o participante" in user_message.lower() and "do evento" in user_message.lower():
                try:
                    email = user_message.split("participante")[-1].split("do evento")[0].strip().strip("'").strip('"')
                    event_name = user_message.split("do evento")[-1].strip().strip("'").strip('"')
                    event = self.find_event_by_summary(event_name)
                    
                    if event:
                        remove_tools = self.composio_toolset.get_tools(actions=['GOOGLECALENDAR_REMOVE_ATTENDEE'])
                        result = remove_tools[0].run({
                            "calendar_id": "primary",
                            "event_id": event['id'],
                            "attendee_email": email
                        })
                        return f"Participante {email} removido do evento {event_name}" if result.get('successfull') else f"Erro ao remover participante: {result.get('error')}"
                    return f"Evento '{event_name}' não encontrado"
                except Exception as e:
                    return f"Erro ao remover participante: {str(e)}"
            
            # Processamento padrão usando o CrewAI
            task = Task(
                description=user_message,
                agent=agent,
                expected_output="Resultado da operação no calendário"
            )
            
            crew = Crew(
                agents=[agent],
                tasks=[task]
            )
            
            result = crew.kickoff()
            
            # Formata a resposta para ser mais amigável
            if isinstance(result, str) and (result.startswith('{') or result.startswith('[')):
                try:
                    data = json.loads(result)
                    if data.get('successfull'):
                        if 'calendars' in str(data):
                            calendars = data['data']['calendars']
                            return f"Encontrei {len(calendars)} calendários:\n{json.dumps(calendars, indent=2)}"
                        elif 'event' in str(data):
                            return f"Operação no evento realizada com sucesso:\n{json.dumps(data['data'], indent=2)}"
                        elif 'calendar' in str(data):
                            return f"Operação no calendário realizada com sucesso:\n{json.dumps(data['data'], indent=2)}"
                    elif data.get('error'):
                        return f"Erro: {data['error']}"
                except json.JSONDecodeError:
                    pass
                    
            return result
            
        except Exception as e:
            logging.error(f"Erro ao processar solicitação: {str(e)}")
            return f"Erro ao processar solicitação: {str(e)}"

if __name__ == "__main__":
    # Testes
    agent = CalendarAgent()
    
    mensagens = [
        "Liste meus calendários",
        "Crie um evento chamado 'Reunião' para amanhã às 10h",
        "Atualize o nome do meu calendário para 'Calendário Principal'",
        "Encontre horários livres amanhã entre 9h e 17h",
        "Duplique meu calendário principal",
        "Remova o participante 'joao@email.com' do evento 'Reunião'"
    ]
    
    for msg in mensagens:
        print(f"\nTestando: {msg}")
        resposta = agent.process_request(msg)
        print(f"Resposta: {resposta}\n")
