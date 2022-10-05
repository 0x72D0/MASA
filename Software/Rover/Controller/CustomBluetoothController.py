import serial

from Controller.IController import IController

class CustomBluetoothController(IController):
    def __init__(self):
        self._serial = serial.Serial("/dev/rfcomm0", timeout=0.1)
    
    def readPacket(self):
        return self._serial.read_until(b'\r\n')