
from Model.ActionType import ActionType


class Action:
    """Class that define a action on a component."""
    def __init__(self):
        self._actionType = ActionType.NONE
        self._actionArguments = []
    
    def __init__(self, actionType: ActionType, actionArguments: list):
        self._actionType = actionType
        self._actionArguments = actionArguments
    
    def get_actionType(self):
        return self._actionType
    
    def get_actionArguments(self):
        return self._actionArguments