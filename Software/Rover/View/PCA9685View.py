import HardwareMapping

from smbus2 import SMBus
from Model.Component import Component, ComponentType

from Model.Model import Model

class PCA9685Config():
    """Class that describe the configuration of one component for the PCA9685"""
    def __init__(self, channel: int, component: Component):
        self._component = component
        self._channel = channel
    
    def get_component(self) -> Component:
        return self._component
    
    def get_channel(self) -> int:
        return self._channel



class PCA9685View():
    """Class that control the PCA9685."""
    def __init__(self, model: Model, port:int, addr: int, configuration: list[PCA9685Config]):
        self._addr = addr
        self._configuration = configuration
        self._model = model
        self._i2cBus = SMBus(port)

        #set the prescaler
        self._i2cBus.write_byte_data(self._addr, 254, 121)

        #print(self._i2cBus.read_byte_data(self._addr, 254))

        self._i2cBus.write_byte_data(self._addr, 0, 0b00000001)
    
    def update(self):
        angleList = self._model.get_servosAngle()
        speedList = self._model.get_motorsSpeed()

        for config in self._configuration:
            componentType = config.get_component().get_type()

            if componentType == ComponentType.SERVO_MOTOR:
                self._writeAngle(config.get_channel(), angleList[config.get_component().get_position()])
            elif componentType == ComponentType.DC_MOTOR:
                self._writeSpeed(config.get_channel(), speedList[config.get_component().get_position()])
 
    def _writeAngle(self, channel: int, angle: int):
        ms = (angle/180)*19
        pwm = round(((ms+1)/20)*4095)
        byte1 = pwm & 0xFF
        byte2 = pwm >> 8

        self._i2cBus.write_byte_data(self._addr, channel*4+6, 0)
        self._i2cBus.write_byte_data(self._addr, channel*4+7, 0)
        self._i2cBus.write_byte_data(self._addr, channel*4+8, byte1)
        self._i2cBus.write_byte_data(self._addr, channel*4+9, byte2)

        #print(self._i2cBus.read_byte_data(self._addr, channel*4+6))
        #print(self._i2cBus.read_byte_data(self._addr, channel*4+7))
        #print(self._i2cBus.read_byte_data(self._addr, channel*4+8))
        #print(self._i2cBus.read_byte_data(self._addr, channel*4+9))
    
    def _writeSpeed(self, channel: int, speed: int):
        pass
