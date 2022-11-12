from Model.Menu.AddProfileNameMenuContext import AddProfileNameMenuContext
from Model.Menu.MenuStack import MenuStack
from Model.Menu.MenuType import MenuType
from Model.Menu.ProfileConfigContext import ProfileConfigContext
from Model.Model import Model
from Model.Menu.IMenuContext import IMenuContext
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController


class ProfileOptionMenuContext(IMenuContext):
    """Menu that decide what profile the user gonna use."""
    def __init__(self, model: Model, selectedProfile: str) -> None:
        self._currentSelectedProfile = selectedProfile
        self._go_back = False
        super().__init__(model)
    
    def get_menuStructure(self) -> tuple:
        return MenuType.LIST, [u'Select >', u'Modify >', u'Delete >']
    
    def go_back(self):
        self._go_back = True

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: MenuStack):

        if(self._go_back):
            menuStack.pop()
            return

        self._handleListMenuIndex(encoderHandle, 2)
        
        # manage the menu Accept button
        acceptButtonState = buttonHandle.get_rotaryEncoderButtonState()
        backButtonState = buttonHandle.get_backButtonState()

        if acceptButtonState == 1:
            if self._currentIndex == 0:
                self._model.setCurrentProfileName(self._currentSelectedProfile)
                menuStack.pop()
            if self._currentIndex == 1:
                self._model.setCurrentProfileName(self._currentSelectedProfile)
                menuStack.add(ProfileConfigContext(self._model))
            if self._currentIndex == 2:
                self._model.deleteProfileName(self._currentSelectedProfile)
                menuStack.pop()
                
        if backButtonState == 1:
            menuStack.pop()