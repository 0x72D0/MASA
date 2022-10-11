from Model.Model import Model
from Model.Menu.IMenuContext import IMenuContext
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Menu.GraphicPage import GraphicPage


class MainMenuContext(IMenuContext):
    def __init__(self, model: Model) -> None:
        super().__init__(model, GraphicPage.MAIN)
        pass

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController) -> IMenuContext:
        self._handleClassicMenuIndex(encoderHandle)
        
        # manage the menu Accept button
        acceptButtonState = buttonHandle.get_rotaryEncoderButtonState()
        backButtonState = buttonHandle.get_backButtonState()

        return self

        # if self._graphicPage == GraphicPage.MAIN:
        #     if acceptButtonState == 1:
        #         if currentIndex == 
