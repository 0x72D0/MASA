from Model.Model import Model
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Menu.GraphicPage import GraphicPage

class IMenuContext:
    __graphicPageMaxIndex = {
            GraphicPage.MAIN: 7
        }

    def __init__(self, model: Model, graphicPage: GraphicPage) -> None:
        self._model = model
        self._graphicPage = graphicPage
        self._maxIndex = IMenuContext.__graphicPageMaxIndex[graphicPage]
        self._currentIndex = 0
    
    def _handleClassicMenuIndex(self, encoderHandle: RotaryEncoderController):
        self._currentIndex = encoderHandle.getValue()

        if self._currentIndex < 0:
            self._currentIndex = 0
            encoderHandle.setValue(0)

        elif self._currentIndex > self._maxIndex:
            self._currentIndex = self._maxIndex
            encoderHandle.setValue(self._maxIndex)

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController):
        pass

    def get_currentGraphicPage(self) -> GraphicPage:
        return self._graphicPage

    def get_currentIndex(self) -> int:
        return self._currentIndex