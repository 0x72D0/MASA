from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Menu.IMenuContext import IMenuContext
from Model.Menu.MenuStack import MenuStack
from Model.Menu.MenuType import MenuType
from Model.Menu.ProfileConfigContext import ProfileConfigContext
from Model.Model import Model


class AddProfileNameMenuContext(IMenuContext):
    """Menu Context to add a profile name"""

    _CHARACTER_SET=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def __init__(self, model: Model) -> None:
        self._maxChar = 7
        self._message_array = ["_"]*self._maxChar
        self._message = ""
        self._currentChar = 0
        self._isFinished = False
        super().__init__(model)
    
    def get_menuStructure(self) -> tuple:
        return MenuType.INPUT_CHAR, [self._message]

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: MenuStack):
        # protection if we go back to this state
        if self._isFinished:
            menuStack.pop()
        
        accept = buttonHandle.get_rotaryEncoderButtonState()
        back = buttonHandle.backButtonCallback()

        self._currentIndex += encoderHandle.getValue()

        if self._currentIndex < 0:
            self._currentIndex = len(AddProfileNameMenuContext._CHARACTER_SET)-1

        elif self._currentIndex > len(AddProfileNameMenuContext._CHARACTER_SET)-1:
            self._currentIndex = 0
        
        self._message_array[self._currentChar] = AddProfileNameMenuContext._CHARACTER_SET[self._currentIndex]
        self._message = "".join(self._message_array)


        if accept == 1:
            self._currentChar +=1
            self._currentIndex = 0
            if self._currentChar >= self._maxChar:
                self._model.startNewProfile(self._message)
                self._model.setCurrentProfileName(self._message)
                self._isFinished = True
                menuStack.add(ProfileConfigContext(self._model))
        
        if back == 1:
            menuStack.pop()
            