from typing import Mapping
from Model.Action import Action
from Model.Action import ActionType

from enum import Enum

class StepperState(Enum):
    """Enumeration of state for the servo motor"""
    INIT = 0
    TOGGLE_ON = 1
    RELEASE_ON = 2

class StepperMode(Enum):
    """Mode for the servo motor"""
    FULL_STEP = 0
    HALF_STEP = 1
    STEP_1_4 = 2
    STEP_1_8 = 3
    STEP_1_16 = 4
    STEP_1_32 = 5

class StepperMotor:
    """Class that define one servo motor component"""
    def __init__(self) -> None:
        self._currentStep = 0
        self._currentState = StepperState.INIT
    
    def update(self, action: Action) -> None:
        if self._currentState == StepperState.INIT:
            if action.get_actionType() == ActionType.TOGGLE:
                print("stepper Toggle ON")
                self._currentStep = action.get_actionArguments()[0]
                self._currentState = StepperState.TOGGLE_ON
            
            elif action.get_actionType() == ActionType.RELEASE_ON:
                print("stepper Release ON")
                self._currentStep = action.get_actionArguments()[0]
                self._currentState = StepperState.RELEASE_ON
            
            elif action.get_actionType() == ActionType.STEP:
                print("stepper STEP")
                self._currentStep += action.get_actionArguments()[0]

            elif action.get_actionType() == ActionType.ANALOG:
                print("stepper ANALOG")
                args = action.get_actionArguments()
                # first argument is the type of analog control
                if args[0] == 0:
                    if args[2] >= 0:
                        self._currentStep = round((args[2]/255)*args[1])
                    else:
                        self._currentStep = 0
            
        elif self._currentState == StepperState.TOGGLE_ON:
            if action.get_actionType() == ActionType.TOGGLE:
                print("stepper Toggle OFF")
                self._currentStep = 0
                self._currentState = StepperState.INIT
        
        elif self._currentState == StepperState.RELEASE_ON:
            if action.get_actionType() == ActionType.RELEASE_OFF:
                print("stepper Release OFF")
                self._currentStep = 0
                self._currentState = StepperState.INIT
    
    def getStep(self) -> int:
        return self._currentStep