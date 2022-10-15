from Model.Component import Component
from Model.Action import Action


class Mapping:
    """Class that define a button Mapping, this class tell which button is link to which action and component."""
    def __init__(self) -> None:
        self._action = Action()
        self._input = ""
        self._component = None
    
    def __init__(self, action: Action, input: str, component: Component) -> None:
        self._action = action
        self._input = input
        self._component = component
    
    def get_componentType(self):
        return self._component.get_type()
    
    def get_componentPosition(self):
        return self._component.get_position()
    
    def get_action(self):
        return self._action
    
    def validateInput(self, input) -> bool:
        if input == self._input:
            return True
        return False