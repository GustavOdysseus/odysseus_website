"""Tools module for composio package."""
from typing import List, Optional, Dict, Any
from .google.calendar_agent import CalendarAgent

class ComposioToolSet:
    """Base class for composio tool sets."""
    
    def __init__(self, api_key: str):
        """Initialize the tool set with API key."""
        self.api_key = api_key
        
    def get_tools(self, actions: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Get tools based on specified actions."""
        if not actions:
            return []
            
        tools = []
        for action in actions:
            if action.startswith('GOOGLECALENDAR_'):
                tools.append({
                    'name': action,
                    'description': f'Execute {action} operation',
                    'parameters': {
                        'api_key': self.api_key
                    }
                })
        return tools
