from enum import Enum

class MenuType(Enum):
    """Enum that tell what is the menu type, this menu type is given to the LCD as a template to draw the text."""
    NONE = 0
    LIST = 1
    STILL_MESSAGE = 2
    NUMBER_ARGUMENT = 3
    