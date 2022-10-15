from Model.Action import Action
from Model.ActionType import ActionType
from Model.Component import Component
from Model.ComponentType import ComponentType
from Model.Menu.MenuType import MenuType
from Model.Model import Model
from Model.Menu.IMenuContext import IMenuContext
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController
from Model.Menu.GraphicPage import GraphicPage


class WaitingInputMenuContext(IMenuContext):
    def __init__(self, model: Model, parentMenu: IMenuContext) -> None:
        self._parentMenu = parentMenu
        super().__init__(model, GraphicPage.WAITING_INPUT)
    
    def get_menuStructure(self) -> tuple:
        return MenuType.STILL_MESSAGE, [u'waiting for input']

    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController) -> IMenuContext:
        nextContext = self

        accept = buttonHandle.get_rotaryEncoderButtonState()
        back = buttonHandle.backButtonCallback()
        
        if self._model.mapNextInputToProfile(Action(ActionType.TOGGLE, [20]), Component(ComponentType.SERVO_MOTOR, 0)):
            return self._parentMenu
        
        if back == 1:
            return self._parentMenu
        
        return nextContext