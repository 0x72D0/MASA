import serial

from Controller.IController import IController

class CustomBluetoothController(IController):
    """Controller that implement a custom bluetooth controller."""
    def __getstate__(self):
        pass

    def __setstate__(self):
        self._serial = serial.Serial("/dev/rfcomm0", timeout=0.1)

    def __init__(self):
        self._serial = serial.Serial("/dev/rfcomm0", timeout=0.1)
    
    def readPacket(self):
        return self._serial.read_until(b'\r\n')