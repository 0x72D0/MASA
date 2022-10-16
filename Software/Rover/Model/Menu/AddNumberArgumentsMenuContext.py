from collections import deque
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Action import Action
from Model.Component import Component
from Model.Menu.GraphicPage import GraphicPage
from Model.Menu.IMenuContext import IMenuContext
from Model.Menu.MenuType import MenuType
from Model.Model import Model


class AddNumberArgumentsMenuContext(IMenuContext):
    """Menu Context for the waiting input menu context."""
    def __init__(self, model: Model, action: Action, component: Component, message: str, max: int, min: int) -> None:
        self._action = action
        self._component = component
        self._message = message
        self._max = max
        self._min = min
        super().__init__(model, GraphicPage.ADD_ARGUMENT)
    
    def get_menuStructure(self) -> tuple:
        return MenuType.NUMBER_ARGUMENT, [self._message, self._currentIndex]

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: deque):
        accept = buttonHandle.get_rotaryEncoderButtonState()
        back = buttonHandle.backButtonCallback()

        self._currentIndex = encoderHandle.getValue()

        if self._currentIndex < self._min:
            self._currentIndex = self._min
            encoderHandle.setValue(self._min)

        elif self._currentIndex > self._max:
            self._currentIndex = self._max
            encoderHandle.setValue(self._max)

        if accept == 1:
            self._action.addArgument(self._currentIndex)
            menuStack.pop()
        
        if back == 1:
            menuStack.pop()
            menuStack[-1].go_back()
            