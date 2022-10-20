from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Action import Action
from Model.ActionType import ActionType
from Model.Component import Component
from Model.ComponentType import ComponentType
from Model.Menu.IMenuContext import IMenuContext
from Model.Menu.MappingMenuContext import MappingMenuContext
from Model.Menu.MenuStack import MenuStack
from Model.Menu.MenuType import MenuType
from Model.Menu.WaitingInputMenuContext import WaitingInputMenuContext
from Model.Menu.AddNumberArgumentsMenuContext import AddNumberArgumentsMenuContext
from Model.Model import Model


class ProfileConfigContext(IMenuContext):
    """Menu context of the profile configuration."""
    def __init__(self, model: Model) -> None:
        self._MAX_INDEX = 2
        super().__init__(model)

    def get_menuStructure(self) -> tuple:
        return MenuType.LIST, [u'servo toggle', u'servo release', u'servo stepping']

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: MenuStack):
        self._handleListMenuIndex(encoderHandle, self._MAX_INDEX)
        
        # manage the menu Accept button
        acceptButtonState = buttonHandle.get_rotaryEncoderButtonState()
        backButtonState = buttonHandle.get_backButtonState()

        if acceptButtonState == 1:
            if self._currentIndex == 0:
                action = Action()
                component = Component()
                action.set_actionType(ActionType.TOGGLE)
                component.set_type(ComponentType.SERVO_MOTOR)
                nextContext = MappingMenuContext(self._model, 
                [
                    AddNumberArgumentsMenuContext(self._model, action, component, u'servo angle', 150, 0),
                    WaitingInputMenuContext(self._model, action, component)
                ])
                menuStack.add(nextContext)
            elif self._currentIndex == 1:
                action1 = Action()
                component1 = Component()
                action2 = Action()
                component2 = Component()
                action2.set_actionType(ActionType.RELEASE_OFF)
                component2.set_type(ComponentType.SERVO_MOTOR)
                nextContext2 = MappingMenuContext(self._model, 
                [
                    WaitingInputMenuContext(self._model, action2, component2)
                ])
                menuStack.add(nextContext2)
                action1.set_actionType(ActionType.RELEASE_ON)
                component1.set_type(ComponentType.SERVO_MOTOR)
                nextContext1 = MappingMenuContext(self._model, 
                [
                    AddNumberArgumentsMenuContext(self._model, action1, component1, u'servo angle', 150, 0),
                    WaitingInputMenuContext(self._model, action1, component1)
                ])
                menuStack.add(nextContext1)
            elif self._currentIndex == 2:
                action = Action()
                component = Component()
                action.set_actionType(ActionType.STEP)
                component.set_type(ComponentType.SERVO_MOTOR)
                nextContext = MappingMenuContext(self._model, 
                [
                    AddNumberArgumentsMenuContext(self._model, action, component, u'servo angle', 150, -150),
                    WaitingInputMenuContext(self._model, action, component)
                ])
                menuStack.add(nextContext)
        
        if backButtonState == 1:
            menuStack.pop()