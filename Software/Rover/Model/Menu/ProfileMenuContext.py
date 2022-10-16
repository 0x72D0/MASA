from collections import deque
from random import randint
from Model.Menu.MenuType import MenuType
from Model.Menu.ProfileConfigContext import ProfileConfigContext
from Model.Model import Model
from Model.Menu.IMenuContext import IMenuContext
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Menu.GraphicPage import GraphicPage


class ProfileMenuContext(IMenuContext):
    """Menu that decide what profile the user gonna use."""
    def __init__(self, model: Model) -> None:
        self._profile_list = [u'New profile']
        super().__init__(model, GraphicPage.CONTROLLER)
    
    def get_menuStructure(self) -> tuple:
        return MenuType.LIST, self._profile_list

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: deque):
        self._handleListMenuIndex(encoderHandle)

        self._profile_list = [u'New profile']
        for profile in self._model.get_profileNameList():
            self._profile_list.append(profile)
        
        # manage the menu Accept button
        acceptButtonState = buttonHandle.get_rotaryEncoderButtonState()
        backButtonState = buttonHandle.get_backButtonState()

        if acceptButtonState == 1:
            if self._currentIndex == 0:
                profile_name = "profile"+str(randint(0, 10000))
                self._model.startNewProfile(profile_name)
                self._model.setCurrentProfileName(profile_name)
            else:
                self._model.setCurrentProfileName(self._profile_list[self._currentIndex])
            
            menuStack.append(ProfileConfigContext(self._model))