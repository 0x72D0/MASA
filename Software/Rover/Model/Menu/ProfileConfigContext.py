from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Menu.GraphicPage import GraphicPage
from Model.Menu.IMenuContext import IMenuContext
from Model.Menu.MenuType import MenuType
from Model.Model import Model


class ProfileConfigContext(IMenuContext):
    def __init__(self, model: Model) -> None:
        super().__init__(model, GraphicPage.PROFILE)

    def get_menuStructure(self) -> tuple:
        return MenuType.LIST, [u'servo motor toggle']

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController) -> IMenuContext:
        nextContext = self
        self._handleListMenuIndex(encoderHandle)
        
        # manage the menu Accept button
        acceptButtonState = buttonHandle.get_rotaryEncoderButtonState()
        backButtonState = buttonHandle.get_backButtonState()
        
        return nextContext