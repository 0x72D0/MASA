from Model.Menu.MenuType import MenuType
from Model.Menu.ProfileConfigContext import ProfileConfigContext
from Model.Model import Model
from Model.Menu.IMenuContext import IMenuContext
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Menu.GraphicPage import GraphicPage


class ControllerMenuContext(IMenuContext):
    """Menu that decide what profile the user gonna use."""
    def __init__(self, model: Model) -> None:
        super().__init__(model, GraphicPage.CONTROLLER)
    
    def get_menuStructure(self) -> tuple:
        return MenuType.LIST, [u' ', u' ']

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController) -> IMenuContext:
        nextContext = self
        self._handleListMenuIndex(encoderHandle)
        
        # manage the menu Accept button
        acceptButtonState = buttonHandle.get_rotaryEncoderButtonState()
        backButtonState = buttonHandle.get_backButtonState()

        nextContext = ProfileConfigContext(self._model)
        
        return nextContext