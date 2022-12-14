from enum import Enum

class ComponentType(Enum):
    """Enum of all the type of component avalaible"""
    NONE = 0
    SERVO_MOTOR = 1
    DC_MOTOR = 2
    STEPPER = 3

class Component:
    """Class that define a component"""
    def __init__(self, type = ComponentType.NONE, position = 0) -> None:
        self._type = type
        self._position = position
    
    def set_position(self, pos: int) -> None:
        self._position = pos
    
    def set_type(self, componentType: ComponentType) -> None:
        self._type = componentType
    
    def get_type(self) -> ComponentType:
        return self._type
    
    def get_position(self) -> int:
        return self._position