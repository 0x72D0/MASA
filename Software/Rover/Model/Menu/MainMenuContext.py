from collections import deque
from Model.Menu.MenuStack import MenuStack
from Model.Menu.ProfileMenuContext import ProfileMenuContext
from Model.Model import Model
from Model.Menu.IMenuContext import IMenuContext
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Menu.MenuType import MenuType


class MainMenuContext(IMenuContext):
    """Menu context of the main menu."""
    def __init__(self, model: Model) -> None:
        self._MAX_INDEX = 7
        super().__init__(model)

    def get_menuStructure(self) -> tuple:
        return MenuType.LIST, [u'Monitor >', u'Pairing >', u'Profile >', u'Test >', u'Test2 >']

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: MenuStack) -> IMenuContext:
        self._handleListMenuIndex(encoderHandle, self._MAX_INDEX)
        
        # manage the menu Accept button
        acceptButtonState = buttonHandle.get_rotaryEncoderButtonState()
        backButtonState = buttonHandle.get_backButtonState()

        if acceptButtonState == 1:
            print("accept")
            if self._currentIndex == 2:
                print("profile menu")
                menuStack.add(ProfileMenuContext(self._model))
