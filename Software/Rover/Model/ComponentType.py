from enum import Enum

class ComponentType(Enum):
    """Enum of all the type of component avalaible"""
    NONE = 0
    SERVO_MOTOR = 1
    DC_MOTOR = 2
    STEPPER = 3