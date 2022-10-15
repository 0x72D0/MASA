from enum import Enum

class GraphicPage(Enum):
    """Enum that list all the different page for the menu."""
    NONE = 0
    MAIN = 1
    MONITOR = 2
    CONTROLLER = 3
    PROFILE = 4
    WAITING_INPUT = 5
