from Model.Menu.GraphicPage import GraphicPage
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Model import Model
from Model.Menu.MainMenuContext import MainMenuContext

class Menu:
    def __init__(self, model: Model) -> None:
        self._encoder = RotaryEncoderController()
        self._button = ButtonController()
        self._currentContext = MainMenuContext(model)

    def get_currentGraphicPage(self) -> GraphicPage:
        return self._currentContext.get_currentGraphicPage()
    
    def get_currentIndex(self) -> int:
        return self._currentContext.get_currentIndex()
    
    def update(self):
        # manage the cursor index
        self._currentContext = self._currentContext.update(self._encoder, self._button)

        

