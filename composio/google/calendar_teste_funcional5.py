from calendar_agent import CalendarAgent
import time

def test_all_calendar_functions():
    calendar_agent = CalendarAgent()
    
    test_cases = [
        "Create a quick event for lunch tomorrow at 12pm.",  # GOOGLECALENDAR_QUICK_ADD
        "List my calendars.",  # GOOGLECALENDAR_LIST_CALENDARS
        "Find my event for tomorrow.",  # GOOGLECALENDAR_FIND_EVENT
        "Delete my lunch event for tomorrow.",  # GOOGLECALENDAR_DELETE_EVENT
        "Update my lunch event to 1pm instead of 12pm.",  # GOOGLECALENDAR_UPDATE_EVENT
        "Create a detailed meeting for next week.",  # GOOGLECALENDAR_CREATE_EVENT
        "What time is it now?",  # GOOGLECALENDAR_GET_CURRENT_DATE_TIME
        "Get my calendar details.",  # GOOGLECALENDAR_GET_CALENDAR
        "Patch my calendar settings.",  # GOOGLECALENDAR_PATCH_CALENDAR
        "Duplicate my calendar.",  # GOOGLECALENDAR_DUPLICATE_CALENDAR
        "Find free slots for tomorrow afternoon.",  # GOOGLECALENDAR_FIND_FREE_SLOTS
        "Remove an attendee from my meeting.",  # GOOGLECALENDAR_REMOVE_ATTENDEE
    ]
    
    for test_case in test_cases:
        print("\n" + "="*50)
        print(f"Testing: {test_case}")
        response = calendar_agent.process_request(test_case)
        print(f"Response: {response}")
        time.sleep(2)  # Pequena pausa entre as requisições

if __name__ == "__main__":
    print("Starting all calendar function tests...")
    test_all_calendar_functions()
