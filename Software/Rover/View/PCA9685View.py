from smbus2 import SMBus
from Model.Component import Component, ComponentType

from Model.Model import Model

class PCA9685Config():
    """Class that describe the configuration of one component for the PCA9685"""
    def __init__(self, channel: list[int], component: Component):
        self._component = component
        self._channel = channel
    
    def get_component(self) -> Component:
        return self._component
    
    def get_channel(self) -> list[int]:
        return self._channel



class PCA9685View():
    """Class that control the PCA9685."""
    def __init__(self, model: Model, port:int, addr: int, configuration: list[PCA9685Config]):
        self.SERVO_MAX_ANGLE = 90
        self.MOTOR_MAX_SPEED = 100

        self.SERVO_RANGE = 0.5
        self.PERIOD = 20
        self.BYTE_RANGE = 4095

        self._addr = addr
        self._configuration = configuration
        self._model = model
        self._i2cBus = SMBus(port)

        self._currentServoAngle = [0]*self._model.get_servoNum()
        self._currentMotorSpeed = [0]*self._model.get_motorNum()

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
                self._currentServoAngle[config.get_component().get_position()] = self._writeAngle(config.get_channel()[0], self._currentServoAngle[config.get_component().get_position()], angleList[config.get_component().get_position()])
            elif componentType == ComponentType.DC_MOTOR:
                self._currentMotorSpeed[config.get_component().get_position()] = self._writeSpeed(config.get_channel()[0], config.get_channel()[1], self._currentMotorSpeed[config.get_component().get_position()], speedList[config.get_component().get_position()])
 
    def _writeAngle(self, channel: int, currentAngle: int, angle: int) -> int:
        if(currentAngle == angle):
            return currentAngle
        
        print("updating servo on channel: " + str(channel) + "! updating angle: " + str(angle))

        ms = ((angle/self.SERVO_MAX_ANGLE)*(self.SERVO_RANGE))+1.5
        pwm = round(((ms)/(self.PERIOD))*self.BYTE_RANGE)

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

        return angle
    
    def _writeSpeed(self, channel_foward: int, channel_backward: int, currentSpeed: int, speed: int) -> int:
        if(speed == currentSpeed):
            return currentSpeed
        
        print("updating motor on channels: " + str(channel_foward) + "/" + str(channel_backward) + "! updating speed: " + str(speed))

        pwm_foward = 0
        pwm_backward = 0
        if(speed >= 0):
            pwm_foward = round((speed/self.MOTOR_MAX_SPEED)*self.BYTE_RANGE)
        else:
            pwm_backward = round(((-speed)/self.MOTOR_MAX_SPEED)*self.BYTE_RANGE)
        
        byte1 = pwm_foward & 0xFF
        byte2 = pwm_foward >> 8
        byte3 = pwm_backward & 0xFF
        byte4 = pwm_backward >> 8

        self._i2cBus.write_byte_data(self._addr, channel_foward*4+6, 0)
        self._i2cBus.write_byte_data(self._addr, channel_foward*4+7, 0)
        self._i2cBus.write_byte_data(self._addr, channel_foward*4+8, byte1)
        self._i2cBus.write_byte_data(self._addr, channel_foward*4+9, byte2)

        self._i2cBus.write_byte_data(self._addr, channel_backward*4+6, 0)
        self._i2cBus.write_byte_data(self._addr, channel_backward*4+7, 0)
        self._i2cBus.write_byte_data(self._addr, channel_backward*4+8, byte3)
        self._i2cBus.write_byte_data(self._addr, channel_backward*4+9, byte4)
        
        return speed
