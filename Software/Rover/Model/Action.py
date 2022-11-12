
from Model.ActionType import ActionType


class Action:
    """Class that define a action on a component."""
    def __init__(self):
        self._actionType = ActionType.NONE
        self._actionArguments = []
    
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