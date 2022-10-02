from Model.GraphicPage import GraphicPage
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController

class Menu:
    def __init__(self) -> None:
        self._graphicPageMaxIndex = {
            GraphicPage.MAIN: 7
        }

        self._currentGraphicPage = GraphicPage.MAIN
        self._currentPageMaxIndex = self._graphicPageMaxIndex[GraphicPage.MAIN]
        self._currentIndex = 0
        self._encoder = RotaryEncoderController()
        self._button = ButtonController()

    def getCurrentGraphicPage(self) -> GraphicPage:
        return self._currentGraphicPage
    
    def getCurrentIndex(self) -> int:
        return self._currentIndex
    
    def updateMenu(self):
        self._currentIndex = self._encoder.getValue()

        if self._currentIndex < 0:
            self._currentIndex = 0
            self._encoder.setValue(0)

        elif self._currentIndex > self._currentPageMaxIndex:
            self._currentIndex = self._currentPageMaxIndex
            self._encoder.setValue(self._currentPageMaxIndex)

