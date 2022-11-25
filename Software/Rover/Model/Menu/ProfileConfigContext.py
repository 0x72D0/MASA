from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Action import Action
from Model.Action import ActionType
from Model.Component import Component
from Model.Component import ComponentType
from Model.Menu.ChooseComponentMenuContext import ChooseComponentMenuContext
from Model.Menu.ChooseComponentMenuContext2 import ChooseComponentMenuContext2
from Model.Menu.IMenuContext import IMenuContext
from Model.Menu.MappingMenuContext import MappingMenuContext
from Model.Menu.MenuStack import MenuStack
from Model.Menu.MenuType import MenuType
from Model.Menu.WaitingInputMenuContext import WaitingInputMenuContext
from Model.Menu.AnalogicInputMenuContext import AnalogicInputMenuContext
from Model.Menu.AddNumberArgumentsMenuContext import AddNumberArgumentsMenuContext
from Model.Model import Model


class ProfileConfigContext(IMenuContext):
    """Menu context of the profile configuration."""
    def __init__(self, model: Model) -> None:
        self._MAX_INDEX = 3
        super().__init__(model)

    def get_menuStructure(self) -> tuple:
        return MenuType.LIST, [u'servo toggle', u'servo release', u'servo stepping', u'servo analogic']

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: MenuStack)-> None:
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
                    ChooseComponentMenuContext(self._model, action, component),
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
                component2.set_position(component.get_position())
                nextContext2 = MappingMenuContext(self._model, 
                [
                    WaitingInputMenuContext(self._model, action2, component2)
                ])
                menuStack.add(nextContext2)
                action1.set_actionType(ActionType.RELEASE_ON)
                component1.set_type(ComponentType.SERVO_MOTOR)
                nextContext1 = MappingMenuContext(self._model, 
                [
                    ChooseComponentMenuContext2(self._model, action, component, component2),
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
                    ChooseComponentMenuContext(self._model, action, component),
                    AddNumberArgumentsMenuContext(self._model, action, component, u'servo angle', 150, -150),
                    WaitingInputMenuContext(self._model, action, component)
                ])
                menuStack.add(nextContext)
            elif self._currentIndex == 3:
                action = Action()
                component = Component()
                action.set_actionType(ActionType.ANALOG)
                component.set_type(ComponentType.SERVO_MOTOR)
                action.addArgument(0)
                nextContext = MappingMenuContext(self._model, 
                [
                    ChooseComponentMenuContext(self._model, action, component),
                    AddNumberArgumentsMenuContext(self._model, action, component, u'servo angle', 150, 0),
                    AnalogicInputMenuContext(self._model, action, component)
                ])
                menuStack.add(nextContext)
        
        if backButtonState == 1:
            menuStack.pop()