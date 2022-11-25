from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Action import Action
from Model.Component import Component
from Model.Menu.IMenuContext import IMenuContext
from Model.Menu.MenuStack import MenuStack
from Model.Menu.MenuType import MenuType
from Model.Model import Model


class ChooseComponentMenuContext(IMenuContext):
    """Menu Context that ask the user to input a number"""
    def __init__(self, model: Model, action: Action, component: Component) -> None:
        self._action = action
        self._component = component
        self._max = model.get_servoNum()-1
        self._min = 0
        super().__init__(model)
    
    def get_menuStructure(self) -> tuple:
        return MenuType.COMPONENT_LIST, [self._model.get_servoNum()]

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: MenuStack) -> None:
        accept = buttonHandle.get_rotaryEncoderButtonState()
        back = buttonHandle.backButtonCallback()

        self._currentIndex += encoderHandle.getValue()

        if self._currentIndex < self._min:
            self._currentIndex = self._min

        elif self._currentIndex > self._max:
            self._currentIndex = self._max

        if accept == 1:
            self._component.set_position(self._currentIndex)
            menuStack.pop()
        
        if back == 1:
            menuStack.pop()