from collections import deque
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Action import Action
from Model.ActionType import ActionType
from Model.Component import Component
from Model.ComponentType import ComponentType
from Model.Menu.GraphicPage import GraphicPage
from Model.Menu.IMenuContext import IMenuContext
from Model.Menu.MappingMenuContext import MappingMenuContext
from Model.Menu.MenuType import MenuType
from Model.Menu.WaitingInputMenuContext import WaitingInputMenuContext
from Model.Menu.AddNumberArgumentsMenuContext import AddNumberArgumentsMenuContext
from Model.Model import Model


class ProfileConfigContext(IMenuContext):
    """Menu context of the profile configuration."""
    def __init__(self, model: Model) -> None:
        super().__init__(model, GraphicPage.PROFILE)

    def get_menuStructure(self) -> tuple:
        return MenuType.LIST, [u'servo toggle']

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: deque):
        self._handleListMenuIndex(encoderHandle)
        
        # manage the menu Accept button
        acceptButtonState = buttonHandle.get_rotaryEncoderButtonState()
        backButtonState = buttonHandle.get_backButtonState()

        if acceptButtonState == 1:
            action = Action()
            component = Component()
            if self._currentIndex == 0:
                action.set_actionType(ActionType.TOGGLE)
                component.set_type(ComponentType.SERVO_MOTOR)
                nextContext = MappingMenuContext(self._model, 
                [
                    AddNumberArgumentsMenuContext(self._model, action, component, u'servo angle', 150, 0),
                    WaitingInputMenuContext(self._model, action, component)
                ])
                menuStack.append(nextContext)