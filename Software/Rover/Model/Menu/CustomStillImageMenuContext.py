from Model.Action import Action
from Model.Action import ActionType
from Model.Component import Component
from Model.Component import ComponentType
from Model.Menu.MenuStack import MenuStack
from Model.Menu.MenuType import MenuType
from Model.Model import Model
from Model.Menu.IMenuContext import IMenuContext
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController


class CustomStillImageMenuContext(IMenuContext):
    """Menu Context for printing a String on the LCD screen"""
    def __init__(self, model: Model, text: str) -> None:
        self._text = text
        super().__init__(model)
    
    def get_menuStructure(self) -> tuple:
        return MenuType.STILL_MESSAGE, [self._text]

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: MenuStack)-> None:

        accept = buttonHandle.get_rotaryEncoderButtonState()
        back = buttonHandle.get_backButtonState()
        
        if accept == 1:
            menuStack.pop
        if back == 1:
            menuStack.pop()