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


class WaitingInputMenuContext(IMenuContext):
    """Menu Context for the waiting input menu context."""
    def __init__(self, model: Model, action: Action, component: Component) -> None:
        self._action = action
        self._component = component
        super().__init__(model)
    
    def get_menuStructure(self) -> tuple:
        return MenuType.STILL_MESSAGE, [u'waiting for input']

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: MenuStack)-> None:

        accept = buttonHandle.get_rotaryEncoderButtonState()
        back = buttonHandle.get_backButtonState()
        
        if self._model.mapDigitalInputToProfile(self._action, self._component):
            menuStack.pop()
        
        if back == 1:
            menuStack.pop()