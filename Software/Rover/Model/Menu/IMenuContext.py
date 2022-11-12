from Model.Menu.MenuStack import MenuStack
from Model.Model import Model
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController

class IMenuContext:
    """Interface that all menu context inherit."""

    def __init__(self, model: Model) -> None:
        self._model = model
        self._currentIndex = 0
    
    def _handleListMenuIndex(self, encoderHandle: RotaryEncoderController, maxIndex):
        self._currentIndex += encoderHandle.getValue()

        if self._currentIndex < 0:
            self._currentIndex = 0

        elif self._currentIndex >= maxIndex:
            self._currentIndex = maxIndex

    def get_currentIndex(self) -> int:
        return self._currentIndex
    
    # return a menu type and arguments
    def get_menuStructure(self) -> tuple:
        pass

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: MenuStack):
        pass

    def go_back(self):
        pass