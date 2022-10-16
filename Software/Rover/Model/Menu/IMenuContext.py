from collections import deque
from Model.Model import Model
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Menu.GraphicPage import GraphicPage
from Model.Menu.MenuType import MenuType

class IMenuContext:
    """Interface that all menu context inherit."""
    __graphicPageMaxIndex = {
            GraphicPage.NONE: 0,
            GraphicPage.MAIN: 7,
            GraphicPage.CONTROLLER: 2,
            GraphicPage.PROFILE: 1,
            GraphicPage.WAITING_INPUT: 0,
            GraphicPage.ADD_ARGUMENT: 0
        }

    def __init__(self, model: Model, graphicPage: GraphicPage) -> None:
        self._model = model
        self._graphicPage = graphicPage
        self._maxIndex = IMenuContext.__graphicPageMaxIndex[graphicPage]
        self._currentIndex = 0
    
    def _handleListMenuIndex(self, encoderHandle: RotaryEncoderController):
        self._currentIndex += encoderHandle.getValue()
        encoderHandle.setValue(0)

        if self._currentIndex < 0:
            self._currentIndex = 0

        elif self._currentIndex > self._maxIndex:
            self._currentIndex = self._maxIndex
    
    def get_currentGraphicPage(self) -> GraphicPage:
        return self._graphicPage

    def get_currentIndex(self) -> int:
        return self._currentIndex
    
    # return a menu type and arguments
    def get_menuStructure(self) -> tuple:
        pass

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: deque):
        pass