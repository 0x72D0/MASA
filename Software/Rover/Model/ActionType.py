from enum import Enum

class ActionType(Enum):
    """Enumeration of all type of action."""
    NONE = 0
    TOGGLE = 1
    RELEASE_ON = 2
    RELEASE_OFF = 3
    STEP = 4
    ANALOG = 5