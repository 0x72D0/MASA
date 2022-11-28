import time
from smbus2 import SMBus
from Model.Component import Component, ComponentType

from Model.Model import Model
from Model.StepperMotor import StepperMode

class PCA9535Config():
    """Class that describe the configuration of one component for the PCA9535"""
    def __init__(self, channel: list[int], component: Component):
        self._component = component
        self._channel = channel
    
    def get_component(self) -> Component:
        return self._component
    
    def get_channel(self) -> list[int]:
        return self._channel

class PCA9535View():
    """Class that control the PCA9535."""
    def __init__(self, model: Model, port:int, addr: int, configuration: list[PCA9535Config]):

        self._addr = addr
        self._configuration = configuration
        self._model = model
        self._i2cBus = SMBus(port)

        self._currentStepper = [0*16]

        #set all the io to output
        self._i2cBus.write_byte_data(self._addr, 6, 0b00000000)
        self._i2cBus.write_byte_data(self._addr, 7, 0b00000000)
    
    def update(self):
        stepList = self._model.get_stepperStep()
        
        for config in self._configuration:
            componentType = config.get_component().get_type()

            if componentType == ComponentType.STEPPER:
                self._writeStep(config.get_channel()[0], self._currentStepper[config.get_channel()[0]], stepList[config.get_component().get_position()])
        
    def _writeStep(self, channel_list: list[int], currentStep: int, targetStep: int, mode: StepperMode):

        bit_mask_0 = 0
        bit_mask_1 = 0

        register = (channel_list[0] / 7) + 2

        if currentStep == targetStep:
            return

        elif currentStep < targetStep:


            currentStep += 1
        
        elif currentStep > targetStep:
            

            currentStep -= 1
        
        
        bit_mask_0 = 1 << (channel_list[0] % 7)

        self._i2cBus.write_byte_data(self._addr, register, bit_mask_0)
        time.sleep(0.1)
        self._i2cBus.write_byte_data(self._addr, register, 0)
