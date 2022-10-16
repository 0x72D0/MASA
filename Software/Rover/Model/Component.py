from Model.ComponentType import ComponentType


class Component:
    """Class that define a component"""
    def __init__(self) -> None:
        self._type = ComponentType.NONE
        self._position = 0
    
    def set_position(self, pos: int):
        self._position = pos
    
    def set_type(self, componentType: ComponentType):
        self._type = componentType
    
    def get_type(self):
        return self._type
    
    def get_position(self):
        return self._position