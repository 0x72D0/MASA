from Model.Action import Action
from Model.Component import Component
from Model.Component import ComponentType
from Model.Menu.MenuStack import MenuStack
from Model.Menu.MenuType import MenuType
from Model.Menu.MonitorMenu import MonitorMenu
from Model.Model import Model
from Model.Menu.IMenuContext import IMenuContext
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController

class MonitorSelectionMenu(IMenuContext):
    """Menu Context for the waiting input menu context."""
    def __init__(self, model: Model) -> None:
        self._selectedComponent = []
        self._listElement = []
        super().__init__(model)
    
    def _find_component(self, componentType: ComponentType, position: int) -> bool:
        for component in self._selectedComponent:
            if component.get_type() == componentType and component.get_position() == position:
                return True
        return False
    
    def get_menuStructure(self) -> tuple:
        return MenuType.LIST, self._listElement   

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: MenuStack) -> None:
        self._handleListMenuIndex(encoderHandle, (self._model.get_servoNum() + self._model.get_motorNum() + self._model.get_stepperNum()))

        self._listElement = []

        # search for Servo
        for i in range(self._model.get_servoNum()):
            if self._find_component(ComponentType.SERVO_MOTOR, i):
                self._listElement.append("Servo " + str(i) + " \x02") # \x02 is the check mark character
            else:
                self._listElement.append("Servo " + str(i))
        
        # search for DC Motor
        for i in range(self._model.get_motorNum()):
            if self._find_component(ComponentType.DC_MOTOR, i):
                self._listElement.append("DC Motor " + str(i) + "\x02") # \x02 is the check mark character
            else:
                self._listElement.append("DC Motor " + str(i))
        
        # search for Stepper
        for i in range(self._model.get_stepperNum()):
            if self._find_component(ComponentType.STEPPER, i):
                self._listElement.append("Stepper " + str(i) + "\x02") # \x02 is the check mark character
            else:
                self._listElement.append("Stepper " + str(i))
        
        self._listElement.append("Done")

        accept = buttonHandle.get_rotaryEncoderButtonState()
        back = buttonHandle.backButtonCallback()
        
        if accept == 1:
            servoIndex = self._model.get_servoNum()
            motorIndex = (self._model.get_servoNum() + self._model.get_motorNum())
            stepperIndex = (self._model.get_servoNum() + self._model.get_motorNum() + self._model.get_stepperNum())

            if self._currentIndex < servoIndex:
                component = Component()
                component.set_position(self._currentIndex)
                component.set_type(ComponentType.SERVO_MOTOR)
                if self._find_component(ComponentType.SERVO_MOTOR, self._currentIndex):
                    self._selectedComponent.remove(component)
                else:
                    self._selectedComponent.append(component)

            elif self._currentIndex < motorIndex:
                component = Component()
                component.set_position(self._currentIndex - servoIndex)
                component.set_type(ComponentType.DC_MOTOR)
                if self._find_component(ComponentType.DC_MOTOR, self._currentIndex - servoIndex):
                    self._selectedComponent.remove(component)
                else:
                    self._selectedComponent.append(component)

            elif self._currentIndex < stepperIndex:
                component = Component()
                component.set_position(self._currentIndex - motorIndex)
                component.set_type(ComponentType.STEPPER)
                if self._find_component(ComponentType.STEPPER, self._currentIndex - motorIndex):
                    self._selectedComponent.remove(component)
                else:
                    self._selectedComponent.append(component)

            elif self._currentIndex == stepperIndex:
                menuStack.add(MonitorMenu(self._model, self._selectedComponent))
        
        if back == 1:
            menuStack.pop()