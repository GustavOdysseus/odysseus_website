from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet, Action, App
import logging
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import pytz

# Configurar logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s')

load_dotenv()

class CalendarTestSuite:
    def __init__(self):
        self.composio_toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
        self.timezone = pytz.timezone('America/Sao_Paulo')
        self.all_actions = [
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
        
    def format_datetime(self, dt):
        """Format datetime object to string in the correct format"""
        return dt.strftime("%Y-%m-%dT%H:%M:%S%z")
        
    def get_tomorrow_datetime(self, hour=0, minute=0):
        """Get tomorrow's datetime at specified hour"""
        tomorrow = datetime.now(self.timezone) + timedelta(days=1)
        return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)

    def run_test(self, action, description):
        try:
            logging.info(f"\nTesting: {description}")
            tools = self.composio_toolset.get_tools(actions=[action])
            
            agent = Agent(
                role="Calendar Assistant",
                goal=f"Process the following calendar request: {description}",
                backstory="You are an AI agent that manages calendar operations efficiently. Always use the primary calendar unless specified otherwise. Format dates in RFC3339 format. For send_updates parameter, use 'none' unless specified otherwise.",
                verbose=True,
                tools=tools,
                llm=ChatOpenAI(temperature=0),
            )
            
            task = Task(
                description=description,
                agent=agent,
                expected_output="Calendar operation result"
            )
            
            crew = Crew(
                agents=[agent],
                tasks=[task]
            )
            
            result = crew.kickoff()
            logging.info(f"Success: {action}")
            print(f"\nResponse: {result}")
            return result
        except Exception as e:
            logging.error(f"Error in {action}: {str(e)}")
            return f"Error: {str(e)}"

    def run_all_tests(self):
        results = {}
        
        # Test 1: Quick Add
        results['quick_add'] = self.run_test('GOOGLECALENDAR_QUICK_ADD', 
                     "Add a quick lunch meeting tomorrow at 1pm")
        
        # Test 2: List Calendars - Simplificado
        results['list_calendars'] = self.run_test('GOOGLECALENDAR_LIST_CALENDARS',
                     "List all my calendars")
        
        # Test 3: Create Event - Com formato correto de data
        tomorrow = self.get_tomorrow_datetime(hour=14, minute=0)
        tomorrow_str = self.format_datetime(tomorrow)
        results['create_event'] = self.run_test('GOOGLECALENDAR_CREATE_EVENT',
                     f"Create a team meeting tomorrow at 2pm titled 'Team Planning' with participants test1@example.com and test2@example.com")
        
        # Test 4: Find Event - Com datas dinâmicas
        start_time = self.get_tomorrow_datetime(hour=9, minute=0)
        end_time = self.get_tomorrow_datetime(hour=17, minute=0)
        start_time_str = self.format_datetime(start_time)
        end_time_str = self.format_datetime(end_time)
        results['find_event'] = self.run_test('GOOGLECALENDAR_FIND_EVENT',
                     f"Find all meetings scheduled for tomorrow between 9am and 5pm")
        
        # Test 5: Update Event
        results['update_event'] = self.run_test('GOOGLECALENDAR_UPDATE_EVENT',
                     "Update the Team Planning meeting to start at 3pm")
        
        # Test 6: Get Current DateTime
        results['get_datetime'] = self.run_test('GOOGLECALENDAR_GET_CURRENT_DATE_TIME',
                     "Get the current date and time")
        
        # Test 7: Get Calendar Details
        results['get_calendar'] = self.run_test('GOOGLECALENDAR_GET_CALENDAR',
                     "Get details of my primary calendar")
        
        # Test 8: Patch Calendar
        results['patch_calendar'] = self.run_test('GOOGLECALENDAR_PATCH_CALENDAR',
                     "Update my calendar summary to 'My Updated Calendar'")
        
        # Test 9: Duplicate Calendar
        results['duplicate_calendar'] = self.run_test('GOOGLECALENDAR_DUPLICATE_CALENDAR',
                     "Create a duplicate of my primary calendar named 'Backup Calendar'")
        
        # Test 10: Find Free Slots
        start_time = self.get_tomorrow_datetime(hour=9, minute=0)
        end_time = self.get_tomorrow_datetime(hour=17, minute=0)
        start_time_str = self.format_datetime(start_time)
        end_time_str = self.format_datetime(end_time)
        results['find_free_slots'] = self.run_test('GOOGLECALENDAR_FIND_FREE_SLOTS',
                     f"Find free slots tomorrow between 9am and 5pm in my primary calendar")
        
        # Test 11: Remove Attendee
        results['remove_attendee'] = self.run_test('GOOGLECALENDAR_REMOVE_ATTENDEE',
                     "Remove test2@example.com from the Team Planning meeting")
        
        # Test 12: Delete Event
        results['delete_event'] = self.run_test('GOOGLECALENDAR_DELETE_EVENT',
                     "Delete the Team Planning meeting")
        
        # Print summary
        print("\n=== Test Summary ===")
        for test_name, result in results.items():
            success = "Error" not in str(result)
            status = "✅ Success" if success else "❌ Failed"
            print(f"{test_name}: {status}")

if __name__ == "__main__":
    test_suite = CalendarTestSuite()
    test_suite.run_all_tests()