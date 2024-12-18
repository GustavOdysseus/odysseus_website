# Define version
__version__ = '0.1.0'

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

class WorkspaceType(Enum):
    """Enum for workspace types"""
    LOCAL = "local"
    REMOTE = "remote"

class ActionType(Enum):
    """Enum for action types"""
    FUNCTION = "function"
    SCRIPT = "script"
    API = "api"

class AppType(Enum):
    """Enum for app types"""
    WEB = "web"
    CLI = "cli"
    SERVICE = "service"

class TagType(Enum):
    """Enum for tag types"""
    CATEGORY = "category"
    VERSION = "version"
    ENVIRONMENT = "environment"

@dataclass
class Action:
    """Action class for defining composio actions"""
    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    type: ActionType = ActionType.FUNCTION

@dataclass
class Tag:
    """Tag class for defining composio tags"""
    name: str
    value: str
    type: TagType = TagType.CATEGORY

@dataclass
class Trigger:
    """Trigger class for defining composio triggers"""
    name: str
    description: Optional[str] = None

@dataclass
class App:
    """App class for defining composio applications"""
    name: str
    description: Optional[str] = None
    type: AppType = AppType.SERVICE
    actions: List[Action] = None
    tags: List[Tag] = None
    triggers: List[Trigger] = None

def action(name: str):
    """Decorator for actions"""
    def decorator(func):
        func.action_name = name
        return func
    return decorator

# Expose main components
__all__ = [
    'CalendarAgent',
    'WorkspaceType',
    'ActionType',
    'AppType',
    'TagType',
    'action',
    'Action',
    'App',
    'Tag',
    'Trigger'
]

# Import components lazily to avoid circular imports
def get_calendar_agent():
    from .google.calendar_agent import CalendarAgent
    return CalendarAgent