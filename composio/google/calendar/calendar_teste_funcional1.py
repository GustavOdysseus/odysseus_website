from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet, Action, App
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
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
                'GOOGLECALENDAR_UPDATE_EVENT'
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
                        Always format responses in a user-friendly way, not raw JSON.""",
            verbose=True,
            tools=self.tools,
            llm=ChatOpenAI(temperature=0),
        )

    def format_datetime(self, dt_str: str) -> str:
        """Format datetime string to local timezone"""
        try:
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            local_dt = dt.astimezone(self.timezone)
            return local_dt.strftime("%B %d, %Y at %I:%M %p")
        except:
            return dt_str

    def format_response(self, response: str) -> str:
        """Format response to be more user-friendly"""
        try:
            data = json.loads(response)
            print(f"Response Data: {data}")  # Log the response data
            if not data.get('successfull'):
                return f"Sorry, an error occurred: {data.get('error', 'Unknown error')}"
            
            # Log the successful response
            print(f"Successful Response: {data}")
            
            # Check for correct structure
            if 'data' not in data:
                return "Sorry, the response does not contain the expected data structure."
            
            if 'calendars' in data.get('data', {}):
                calendars = data['data']['calendars']
                response = "Your calendars:\n"
                for cal in calendars:
                    response += f"- {cal['summary']}\n"
                    if cal.get('description'):
                        response += f"  Description: {cal['description']}\n"
                    response += f"  Access: {cal['accessRole']}\n"
                return response
            
            if 'event_data' in data.get('data', {}):
                events = data['data']['event_data'].get('event_data', [])
                if not events:
                    return "You don't have any events scheduled for this period."
                response = "Events found:\n"
                for event in events:
                    start_time = self.format_datetime(event['start'].get('dateTime', event['start'].get('date')))
                    response += f"- {event['summary']} on {start_time}\n"
                    if event.get('description'):
                        response += f"  Description: {event['description']}\n"
                    if event.get('location'):
                        response += f"  Location: {event['location']}\n"
                return response
            
            if 'event' in data.get('data', {}):
                event = data['data']['event']
                start_time = self.format_datetime(event['start'].get('dateTime', event['start'].get('date')))
                response = f"Event '{event['summary']}' has been scheduled for {start_time}\n"
                if event.get('description'):
                    response += f"Description: {event['description']}\n"
                if event.get('location'):
                    response += f"Location: {event['location']}\n"
                if event.get('hangoutLink'):
                    response += f"Meet link: {event['hangoutLink']}\n"
                
                
            
            return "Operation completed successfully!"
        except Exception as e:
            return f"Sorry, couldn't process the response: {str(e)}"

    def delete_event(self, event_id: str) -> dict:
        """Delete an event by ID"""
        task = Task(
            description=f"Delete event with ID {event_id}",
            expected_output="A user-friendly response about the deletion operation",
            agent=self.agent
        )
        task.add_tool_action(
            tool_name="GOOGLECALENDAR_DELETE_EVENT",
            input_data={"event_id": event_id}
        )
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        try:
            result = crew.kickoff()
            # Ensure the result is in string format before processing
            result_str = str(result)
            # Check if the result is a valid JSON string
            try:
                json.loads(result_str)
            except json.JSONDecodeError:
                return {"successfull": False, "error": "Invalid response"}
            return json.loads(result_str)
        except Exception as e:
            return {"successfull": False, "error": str(e)}

    def quick_add_event(self, task_description: str) -> str:
        """Adiciona um evento rapidamente ao Google Calendar usando o método GOOGLECALENDAR_QUICK_ADD"""
        try:
            task = Task(
                description=task_description,
                expected_output="Um evento foi adicionado com sucesso."
            )
            crew = Crew(
                agents=[self.agent],
                tasks=[task],
                verbose=True
            )
            result = crew.kickoff()
            return self.format_response(str(result))
        except Exception as e:
            return f"Desculpe, ocorreu um erro: {str(e)}"

    def process_request(self, user_message: str) -> str:
        """
        Process user message and return appropriate response
        """
        # Prepare date parameters for event search
        now = datetime.now(self.timezone)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Log the date parameters
        print(f"today_start: {today_start.isoformat()}")
        print(f"today_end: {today_end.isoformat()}")

        # Criar a tarefa corretamente sem usar add_tool_action
        task = Task(
            description=f"Processar a seguinte solicitação de calendário: {user_message}",
            expected_output="Uma resposta amigável sobre a operação do calendário",
            agent=self.agent,
            tools=self.tools  # Passar as ferramentas necessárias aqui
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )

        try:
            result = crew.kickoff()
            # Ensure the result is in string format before processing
            result_str = str(result)

            # Check if the result is a valid JSON string
            try:
                json.loads(result_str)
            except json.JSONDecodeError:
                return "Sorry, the response was not valid."

            return self.format_response(result_str)
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
