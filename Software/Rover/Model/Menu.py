from Model.GraphicPage import GraphicPage
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController

class Menu:
    def __init__(self) -> None:
        self._currentGraphicPage = GraphicPage.MAIN
        self._encoder = RotaryEncoderController()
        self._backButton = ButtonController()

    def getCurrentGraphicPage(self) -> GraphicPage:
        return self._currentGraphicPage

