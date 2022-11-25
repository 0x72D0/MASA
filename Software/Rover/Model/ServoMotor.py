from typing import Mapping
from Model.Action import Action
from Model.Action import ActionType

from enum import Enum

class ServoState(Enum):
    """Enumeration of state for the servo motor"""
    INIT = 0
    TOGGLE_ON = 1
    RELEASE_ON = 2

class ServoMotor:
    """Class that define one servo motor component"""
    def __init__(self) -> None:
        self._currentAngle = 0
        self._currentState = ServoState.INIT
    
    def update(self, action: Action) -> None:
        if self._currentState == ServoState.INIT:
            if action.get_actionType() == ActionType.TOGGLE:
                print("servo Toggle ON")
                self._currentAngle = action.get_actionArguments()[0]
                self._currentState = ServoState.TOGGLE_ON
            
            elif action.get_actionType() == ActionType.RELEASE_ON:
                print("servo Release ON")
                self._currentAngle = action.get_actionArguments()[0]
                self._currentState = ServoState.RELEASE_ON
            
            elif action.get_actionType() == ActionType.STEP:
                print("servo STEP")
                self._currentAngle += action.get_actionArguments()[0]

            elif action.get_actionType() == ActionType.ANALOG:
                print("servo ANALOG")
                args = action.get_actionArguments()
                # first argument is the type of analog control
                if args[0] == 0:
                    if args[2] >= 0:
                        self._currentAngle = (args[2]/255)*args[1]
                    else:
                        self._currentAngle = 0
            
        elif self._currentState == ServoState.TOGGLE_ON:
            if action.get_actionType() == ActionType.TOGGLE:
                print("servo Toggle OFF")
                self._currentAngle = 0
                self._currentState = ServoState.INIT
        
        elif self._currentState == ServoState.RELEASE_ON:
            if action.get_actionType() == ActionType.RELEASE_OFF:
                print("servo Release OFF")
                self._currentAngle = 0
                self._currentState = ServoState.INIT
    
    def getAngle(self) -> int:
        return self._currentAngle

