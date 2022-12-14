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

        self.OUTPUT_REGISTER_0 = 2
        self.OUTPUT_REGISTER_1 = 3

        self._addr = addr
        self._configuration = configuration
        self._model = model
        self._i2cBus = SMBus(port)

        self._currentStepper = [0]*self._model.get_stepperNum()

        #set all the io to output
        self._i2cBus.write_byte_data(self._addr, 6, 0b00000000)
        self._i2cBus.write_byte_data(self._addr, 7, 0b00000000)

        print(self._i2cBus.read_byte_data(self._addr, 6))
        print(self._i2cBus.read_byte_data(self._addr, 7))
    
    def update(self):
        stepList = self._model.get_stepperStep()
        
        for config in self._configuration:
            componentType = config.get_component().get_type()

            if componentType == ComponentType.STEPPER:
                self._currentStepper[config.get_component().get_position()] = self._writeStep(config.get_channel(), self._currentStepper[config.get_component().get_position()], stepList[config.get_component().get_position()], StepperMode.FULL_STEP)
        
    def _writeStep(self, channel_list: list[int], currentStep: int, targetStep: int, mode: StepperMode) -> int:
        """Channel 0 is the Step channel / Channel 1 is the DIR channel and Channel 2,3,4 is M0,M1,M2"""
        bit_mask = (self._i2cBus.read_byte_data(self._addr, self.OUTPUT_REGISTER_0) << 8) | self._i2cBus.read_byte_data(self._addr, self.OUTPUT_REGISTER_1)

        if currentStep == targetStep:
            return currentStep

        elif currentStep < targetStep:
            bit_mask = self._clearBit(bit_mask, channel_list[1])
            currentStep += 1
        
        elif currentStep > targetStep:
            bit_mask = self._setBit(bit_mask, channel_list[1])
            currentStep -= 1
        
        self._update_output_registers(bit_mask)
        
        print("updating stepper! currentStep: " + str(currentStep) + " targetStep: " + str(targetStep))
        
        if mode == StepperMode.FULL_STEP:
            bit_mask = self._clearBit(bit_mask, channel_list[2])
            bit_mask = self._clearBit(bit_mask, channel_list[3])
            bit_mask = self._clearBit(bit_mask, channel_list[4])
        elif mode == StepperMode.HALF_STEP:
            bit_mask = self._setBit(bit_mask, channel_list[2])
            bit_mask = self._clearBit(bit_mask, channel_list[3])
            bit_mask = self._clearBit(bit_mask, channel_list[4])
        elif mode == StepperMode.STEP_1_4:
            bit_mask = self._clearBit(bit_mask, channel_list[2])
            bit_mask = self._setBit(bit_mask, channel_list[3])
            bit_mask = self._clearBit(bit_mask, channel_list[4])
        elif mode == StepperMode.STEP_1_8:
            bit_mask = self._setBit(bit_mask, channel_list[2])
            bit_mask = self._setBit(bit_mask, channel_list[3])
            bit_mask = self._clearBit(bit_mask, channel_list[4])
        elif mode == StepperMode.STEP_1_16:
            bit_mask = self._clearBit(bit_mask, channel_list[2])
            bit_mask = self._clearBit(bit_mask, channel_list[3])
            bit_mask = self._setBit(bit_mask, channel_list[4])
        if mode == StepperMode.STEP_1_32:
            bit_mask = self._setBit(bit_mask, channel_list[2])
            bit_mask = self._setBit(bit_mask, channel_list[3])
            bit_mask = self._setBit(bit_mask, channel_list[4])

        bit_mask = self._setBit(bit_mask, channel_list[0])
        self._update_output_registers(bit_mask)
        # TODO: this sleep could be a futur bottleneck, find another way
        time.sleep(0.3)
        bit_mask = self._clearBit(bit_mask, channel_list[0])
        self._update_output_registers(bit_mask)

        return currentStep
    
    def _update_output_registers(self, mask: int) -> None:
        self._i2cBus.write_byte_data(self._addr, self.OUTPUT_REGISTER_0, (mask & 0xFF))
        self._i2cBus.write_byte_data(self._addr, self.OUTPUT_REGISTER_1, ((mask >> 8) & 0xFF))

        print(bin(self._i2cBus.read_byte_data(self._addr, self.OUTPUT_REGISTER_0)))
        print(bin(self._i2cBus.read_byte_data(self._addr, self.OUTPUT_REGISTER_1)))
    
    def _setBit(self, mask: int, position: int) -> int:
        return (mask | (1 << position))
    
    def _clearBit(self, mask: int, position: int) -> int:
        return (mask & ~(1 << position))
