from Model.Action import Action
from Model.Component import Component
from Model.ComponentType import ComponentType
from Model.Menu.MenuStack import MenuStack
from Model.Menu.MenuType import MenuType
from Model.Model import Model
from Model.Menu.IMenuContext import IMenuContext
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController

class MonitorMenu(IMenuContext):
    """Menu Context for the waiting input menu context."""
    def __init__(self, model: Model, selectedComponent: list) -> None:
        self._selectedComponent = selectedComponent
        self._monitorElement = []
        super().__init__(model)
    
    def get_menuStructure(self) -> tuple:
        return MenuType.MONITOR, self._monitorElement   

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: MenuStack):
        self._monitorElement = []

        # search for Servo
        for component in self._selectedComponent:
            self._monitorElement.append(component.get_type())
            self._monitorElement.append(component.get_position())

            if component.get_type() == ComponentType.SERVO_MOTOR:
                self._monitorElement.append(self._model.get_servoComponent(component.get_position()).getAngle())
            if component.get_type() == ComponentType.DC_MOTOR:
                self._monitorElement.append(self._model.get_motorComponent(component.get_position()).getSpeed())
            if component.get_type() == ComponentType.STEPPER:
                self._monitorElement.append(self._model.get_stepperComponent(component.get_position()).getStep())

        back = buttonHandle.backButtonCallback()
        
        if back == 1:
            menuStack.pop()