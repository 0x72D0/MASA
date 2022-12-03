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
        return MenuType.LIST, [ 
                                u'servo toggle', u'servo release', u'servo stepping', u'servo analogic', 
                                u'motor toggle', u'motor release', u'motor stepping', u'motor analogic', 
                                u'stepper toggle', u'stepper release', u'stepper stepping', u'stepper analogic'
                              ]

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: MenuStack)-> None:
        self._handleListMenuIndex(encoderHandle, self._MAX_INDEX)
        
        # manage the menu Accept button
        acceptButtonState = buttonHandle.get_rotaryEncoderButtonState()
        backButtonState = buttonHandle.get_backButtonState()

        if acceptButtonState == 1:

            # servo toggle
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
            
            # servo release
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
            
            # servo stepping
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
            
            # servo analogic
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
            
            # DC Motor Toggle
            elif self._currentIndex == 4:
                action = Action()
                component = Component()
                action.set_actionType(ActionType.TOGGLE)
                component.set_type(ComponentType.DC_MOTOR)
                nextContext = MappingMenuContext(self._model, 
                [
                    ChooseComponentMenuContext(self._model, action, component),
                    AddNumberArgumentsMenuContext(self._model, action, component, u'motor speed', 100, -100),
                    AnalogicInputMenuContext(self._model, action, component)
                ])
                menuStack.add(nextContext)
            
            # DC Motor release
            elif self._currentIndex == 5:
                action1 = Action()
                component1 = Component()
                action2 = Action()
                component2 = Component()
                action2.set_actionType(ActionType.RELEASE_OFF)
                component2.set_type(ComponentType.DC_MOTOR)
                component2.set_position(component.get_position())
                nextContext2 = MappingMenuContext(self._model, 
                [
                    WaitingInputMenuContext(self._model, action2, component2)
                ])
                menuStack.add(nextContext2)
                action1.set_actionType(ActionType.RELEASE_ON)
                component1.set_type(ComponentType.DC_MOTOR)
                nextContext1 = MappingMenuContext(self._model, 
                [
                    ChooseComponentMenuContext2(self._model, action, component, component2),
                    AddNumberArgumentsMenuContext(self._model, action1, component1, u'motor speed', 100, -100),
                    WaitingInputMenuContext(self._model, action1, component1)
                ])
                menuStack.add(nextContext1)
            
            # DC Motor stepping
            elif self._currentIndex == 6:
                action = Action()
                component = Component()
                action.set_actionType(ActionType.STEP)
                component.set_type(ComponentType.DC_MOTOR)
                nextContext = MappingMenuContext(self._model, 
                [
                    ChooseComponentMenuContext(self._model, action, component),
                    AddNumberArgumentsMenuContext(self._model, action, component, u'motor speed', 100, -100),
                    WaitingInputMenuContext(self._model, action, component)
                ])
                menuStack.add(nextContext)
            
            # DC Motor analogic
            elif self._currentIndex == 7:
                action = Action()
                component = Component()
                action.set_actionType(ActionType.ANALOG)
                component.set_type(ComponentType.DC_MOTOR)
                action.addArgument(0)
                nextContext = MappingMenuContext(self._model, 
                [
                    ChooseComponentMenuContext(self._model, action, component),
                    AddNumberArgumentsMenuContext(self._model, action, component, u'motor speed', 100, -100),
                    AnalogicInputMenuContext(self._model, action, component)
                ])
                menuStack.add(nextContext)
            
            # stepper toggle
            if self._currentIndex == 8:
                action = Action()
                component = Component()
                action.set_actionType(ActionType.TOGGLE)
                component.set_type(ComponentType.STEPPER)
                nextContext = MappingMenuContext(self._model, 
                [
                    ChooseComponentMenuContext(self._model, action, component),
                    AddNumberArgumentsMenuContext(self._model, action, component, u'step at a time', 10, -10),
                    WaitingInputMenuContext(self._model, action, component)
                ])
                menuStack.add(nextContext)
            
            # Stepper release
            elif self._currentIndex == 9:
                action1 = Action()
                component1 = Component()
                action2 = Action()
                component2 = Component()
                action2.set_actionType(ActionType.RELEASE_OFF)
                component2.set_type(ComponentType.STEPPER)
                component2.set_position(component.get_position())
                nextContext2 = MappingMenuContext(self._model, 
                [
                    WaitingInputMenuContext(self._model, action2, component2)
                ])
                menuStack.add(nextContext2)
                action1.set_actionType(ActionType.RELEASE_ON)
                component1.set_type(ComponentType.STEPPER)
                nextContext1 = MappingMenuContext(self._model, 
                [
                    ChooseComponentMenuContext2(self._model, action, component, component2),
                    AddNumberArgumentsMenuContext(self._model, action1, component1, u'step at a time', 10, -10),
                    WaitingInputMenuContext(self._model, action1, component1)
                ])
                menuStack.add(nextContext1)
            
            # Stepper stepping
            elif self._currentIndex == 10:
                action = Action()
                component = Component()
                action.set_actionType(ActionType.STEP)
                component.set_type(ComponentType.STEPPER)
                nextContext = MappingMenuContext(self._model, 
                [
                    ChooseComponentMenuContext(self._model, action, component),
                    AddNumberArgumentsMenuContext(self._model, action, component, u'step at a time', 10, -10),
                    WaitingInputMenuContext(self._model, action, component)
                ])
                menuStack.add(nextContext)
            
            # Stepper analogic
            elif self._currentIndex == 11:
                action = Action()
                component = Component()
                action.set_actionType(ActionType.ANALOG)
                component.set_type(ComponentType.STEPPER)
                action.addArgument(0)
                nextContext = MappingMenuContext(self._model, 
                [
                    ChooseComponentMenuContext(self._model, action, component),
                    AddNumberArgumentsMenuContext(self._model, action, component, u'step at a time', 10, -10),
                    AnalogicInputMenuContext(self._model, action, component)
                ])
                menuStack.add(nextContext)
        
        if backButtonState == 1:
            menuStack.pop()