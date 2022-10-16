from collections import deque
from Model.Menu.GraphicPage import GraphicPage
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Model import Model
from Model.Menu.MainMenuContext import MainMenuContext

class Menu:
    """Model class that contains the menu logic."""
    def __init__(self, model: Model) -> None:
        self._encoder = RotaryEncoderController()
        self._button = ButtonController()
        self._menuStack = deque([MainMenuContext(model)])
    
    def get_currentMenuType(self) -> tuple:
        return self._menuStack[-1].get_menuStructure()

    def get_currentGraphicPage(self) -> GraphicPage:
        return self._menuStack[-1].get_currentGraphicPage()
    
    def get_currentIndex(self) -> int:
        return self._menuStack[-1].get_currentIndex()
    
    def update(self):
        # manage the context
        # here's the menu is a state machine design pattern
        self._menuStack[-1].update(self._encoder, self._button, self._menuStack)

        

