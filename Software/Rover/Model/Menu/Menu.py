from collections import deque
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Menu.MenuStack import MenuStack
from Model.Model import Model
from Model.Menu.MainMenuContext import MainMenuContext

class Menu:
    """Model class that contains the menu logic."""
    def __init__(self, model: Model) -> None:
        self._encoder = RotaryEncoderController()
        self._button = ButtonController()
        self._menuStack = MenuStack(MainMenuContext(model))
    
    def get_currentMenuType(self) -> tuple:
        return self._menuStack.get_top().get_menuStructure()

    def needScreenRefresh(self):
        return self._menuStack.needScreenRefresh()
    
    def get_currentIndex(self) -> int:
        return self._menuStack.get_top().get_currentIndex()
    
    def update(self):
        # manage the context
        # here's the menu is a state machine design pattern
        self._menuStack.get_top().update(self._encoder, self._button, self._menuStack)

        

