from smbus2 import SMBus

class ServoMotorView():
    def __init__(self):
        self._addr = 0x41
        self._i2cBus = SMBus(1)

        #set the prescaler
        self._i2cBus.write_byte_data(self._addr, 254, 121)

        print(self._i2cBus.read_byte_data(self._addr, 254))

        self._i2cBus.write_byte_data(self._addr, 0, 0b00000001)

    def write_angle(self, channel, angle):
        ms = (angle/180)*19
        pwm = round(((ms+1)/20)*4095)
        byte1 = pwm & 0xFF
        byte2 = pwm >> 8

        self._i2cBus.write_byte_data(self._addr, channel*4+6, 0)
        self._i2cBus.write_byte_data(self._addr, channel*4+7, 0)
        self._i2cBus.write_byte_data(self._addr, channel*4+8, byte1)
        self._i2cBus.write_byte_data(self._addr, channel*4+9, byte2)

        print(self._i2cBus.read_byte_data(self._addr, channel*4+6))
        print(self._i2cBus.read_byte_data(self._addr, channel*4+7))
        print(self._i2cBus.read_byte_data(self._addr, channel*4+8))
        print(self._i2cBus.read_byte_data(self._addr, channel*4+9))
