import pytest
from composio.google.calendar_agent import CalendarAgent


def test_create_event():
    agent = CalendarAgent()
    response = agent.create_event("Test Event", "2024-12-13T10:00:00-03:00", "2024-12-13T11:00:00-03:00")
    assert "Event 'Test Event' has been scheduled" in response


def test_delete_event():
    agent = CalendarAgent()
    response = agent.delete_event("test_event_id")
    assert "Event deleted successfully" in response
