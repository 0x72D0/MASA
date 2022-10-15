from Model.Menu.ControllerMenuContext import ControllerMenuContext
from Model.Model import Model
from Model.Menu.IMenuContext import IMenuContext
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Menu.GraphicPage import GraphicPage
from Model.Menu.MenuType import MenuType


class MainMenuContext(IMenuContext):
    """Menu context of the main menu."""
    def __init__(self, model: Model) -> None:
        super().__init__(model, GraphicPage.MAIN)

    def get_menuStructure(self) -> tuple:
        return MenuType.LIST, [u'Monitor >', u'Pairing >', u'Controller >', u'Test >', u'Test2 >']

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController) -> IMenuContext:
        nextContext = self
        self._handleListMenuIndex(encoderHandle)
        
        # manage the menu Accept button
        acceptButtonState = buttonHandle.get_rotaryEncoderButtonState()
        backButtonState = buttonHandle.get_backButtonState()

        if acceptButtonState == 1:
            print("accept")
            if self._currentIndex == 2:
                print("controller menu")
                nextContext = ControllerMenuContext(self._model)
        
        return nextContext
