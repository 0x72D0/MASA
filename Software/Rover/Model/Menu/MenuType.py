from enum import Enum

class MenuType(Enum):
    """Enum that tell what is the menu type, this menu type is given to the LCD as a template to draw the text."""
    LIST = 0
    STILL_MESSAGE = 1
    