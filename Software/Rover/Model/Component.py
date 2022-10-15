from Model.ComponentType import ComponentType


class Component:
    """Class that define a component"""
    def __init__(self, type: ComponentType, position:int) -> None:
        self._type = type
        self._position = position
    
    def get_type(self):
        return self._type
    
    def get_position(self):
        return self._position