from collections import deque
from Model.Menu.MenuStack import MenuStack
from Model.Menu.MonitorSelectionMenu import MonitorSelectionMenu
from Model.Menu.ProfileMenuContext import ProfileMenuContext
from Model.Menu.CustomStillImageMenuContext import CustomStillImageMenuContext
from Model.Model import Model
from Model.Menu.IMenuContext import IMenuContext
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Menu.MenuType import MenuType


class MainMenuContext(IMenuContext):
    """Menu context of the main menu."""
    def __init__(self, model: Model) -> None:
        self._MAX_INDEX = 2
        super().__init__(model)

    def get_menuStructure(self) -> tuple:
        return MenuType.LIST, [u'Monitor >', u'Profile >', u'Save Profiles']

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: MenuStack) -> None:
        self._handleListMenuIndex(encoderHandle, self._MAX_INDEX)
        
        # manage the menu Accept button
        acceptButtonState = buttonHandle.get_rotaryEncoderButtonState()
        backButtonState = buttonHandle.get_backButtonState()

        if acceptButtonState == 1:
            print("accept")
            if self._currentIndex == 0:
                print("monitor menu")
                menuStack.add(MonitorSelectionMenu(self._model))
            if self._currentIndex == 1:
                print("profile menu")
                menuStack.add(ProfileMenuContext(self._model))
            if self._currentIndex == 2:
                print("save profiles")
                self._model.saveProfiles()
                menuStack.add(CustomStillImageMenuContext(self._model, "Profile Saved!"))
