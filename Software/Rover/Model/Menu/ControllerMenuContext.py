from Model.Model import Model
from Model.Menu.IMenuContext import IMenuContext
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Menu.GraphicPage import GraphicPage


class ControllerMenuContext(IMenuContext):
    def __init__(self, model: Model) -> None:
        super().__init__(model, GraphicPage.CONTROLLER)
        pass

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController) -> IMenuContext:
        nextContext = self
        self._handleClassicMenuIndex(encoderHandle)
        
        # manage the menu Accept button
        acceptButtonState = buttonHandle.get_rotaryEncoderButtonState()
        backButtonState = buttonHandle.get_backButtonState()

        if self._graphicPage == GraphicPage.MAIN:
            if acceptButtonState == 1:
                if self._currentIndex == 2:
                    nextContext = ControllerMenuContext(model)
        
        return nextContext