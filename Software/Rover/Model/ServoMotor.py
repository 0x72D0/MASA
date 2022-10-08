from typing import Mapping
from Model.Action import Action
from Model.ActionType import ActionType
from Model.ServoState import ServoState


class ServoMotor:
    def __init__(self) -> None:
        self._currentAngle = 0
        self._currentState = ServoState.INIT
    
    def update(self, action: Action) -> None:
        if self._currentState == ServoState.INIT:
            if action.get_actionType() == ActionType.TOGGLE:
                self._currentAngle = action.get_actionArguments()[0]
                self._currentState = ServoState.TOGGLE_ON
        elif self._currentState == ServoState.TOGGLE_ON:
            if action.get_actionType() == ActionType.TOGGLE:
                self._currentAngle = 0
                self._currentState = ServoState.INIT
    
    def getAngle(self):
        return self._currentAngle

