from enum import Enum

class ActionType(Enum):
    """Enumeration of all type of action."""
    NONE = 0
    TOGGLE = 1
    RELEASE_ON = 2
    RELEASE_OFF = 3
    STEP = 4
    ANALOG = 5

class Action:
    """Class that define a action on a component."""
    def __init__(self):
        self._actionType = ActionType.NONE
        self._actionArguments = list()
    
    def set_actionType(self, actionType: ActionType):
        self._actionType = actionType
    
    def addArgument(self, arg):
        self._actionArguments.append(arg)
    
    def get_actionType(self):
        return self._actionType
    
    def get_actionArguments(self):
        return self._actionArguments
    
    def isAnalogic(self):
        if self._actionType == ActionType.ANALOG:
            return True
        return False