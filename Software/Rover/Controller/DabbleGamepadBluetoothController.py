from enum import Enum
import serial

from Controller.IController import IController
from Model.ControllerEvent import ControllerEvent, EventType

class com_state(Enum):
    START_OF_FRAME = 0
    MODULE_ID = 1
    FUNCTION_ID = 2
    ARG_NO_1 = 3
    ARG_NO_2 = 4
    ARG_DECODE = 5
    END_OF_FRAME = 6

class DabbleGamepadBluetoothController(IController):
    """Controller that implement a custom bluetooth controller."""
    def __getstate__(self):
        pass

    def __setstate__(self):
        self._serial = serial.Serial(port='/dev/serial0', baudrate = 9600, timeout=0.1)
        self._state = com_state.START_OF_FRAME
        self._i = 0
        self._j = 0
        self._max_i = 0
        self._max_j = 0
        self._packet = bytearray()
        self._lastByteArray = bytearray()

    def __init__(self):
        self._serial = serial.Serial(port='/dev/serial0', baudrate = 9600, timeout=0.1)
        self._state = com_state.START_OF_FRAME
        self._i = 0
        self._j = 0
        self._max_i = 0
        self._max_j = 0
        self._packet = bytearray()
        self._lastByteArray = bytearray()
    
    def cleanup(self) -> None:
        self._serial.close()
    
    def translate_packet(self) -> ControllerEvent:
        byteArray = bytearray()

        # if it was a digital input, detect it.
        byteArray.append(self._packet[-2])

        if(self._lastByteArray != byteArray):
            self._lastByteArray = byteArray
            return ControllerEvent(EventType.DIGITAL, bytes(byteArray))
        
        # if not it's a analogic input
        byteArray.clear()    
        intensity = self._packet[-1] & 0x07
        rotation = self._packet[-1] >> 3

        if(rotation >= 0b00100 and rotation <= 0b01000):
            byteArray.append(int(((intensity/0x07)*127)+128))
        elif(rotation >= 0b10000 and rotation <= 0b10100):
            byteArray.append(int(127-((intensity/0x06)*127)))
        elif(rotation == 0 and intensity == 0):
            byteArray.append(128)
        else:
            byteArray.append(0)
        
        return ControllerEvent(EventType.ANALOG, bytes(byteArray))
    
    def readPacket(self) -> ControllerEvent:
        data = "a"

        while data != b'':
            data = self._serial.read(1)

            if self._state == com_state.START_OF_FRAME:
                if data == b'\xff':
                    print("-----FRAME START-----")
                    self._state = com_state.MODULE_ID
                    self._packet.clear()

            elif self._state == com_state.MODULE_ID:
                print("Module ID: " + str(data))
                self._packet.append(data[0])
                self._state = com_state.FUNCTION_ID
            
            elif self._state == com_state.FUNCTION_ID:
                print("Function ID: " + str(data))
                self._packet.append(data[0])
                self._state = com_state.ARG_NO_1

            elif self._state == com_state.ARG_NO_1:
                print("Numbers of arguments: " + str(data))
                self._packet.append(data[0])
                self._i = 0
                self._max_i = int.from_bytes(data, "big")
                self._state = com_state.ARG_NO_2
            
            elif self._state == com_state.ARG_NO_2:
                print("Numbers of arguments: " + str(data))
                self._packet.append(data[0])
                self._j = 0
                self._max_j = int.from_bytes(data, "big")
                self._state = com_state.ARG_DECODE
            
            elif self._state == com_state.ARG_DECODE:
                print("Arg_" + str(self._i+1) + "_" + str(self._j+1) +": " + str(data))
                self._packet.append(data[0])
                self._j += 1
                if self._j >= self._max_j:
                    self._i += 1
                if self._i >= self._max_i:
                    self._state = com_state.END_OF_FRAME
            
            elif self._state == com_state.END_OF_FRAME:
                if data == b'\x00':
                    print("-----FRAME END-----")
                    self._state = com_state.START_OF_FRAME
                    return self.translate_packet()
                else:
                    print("error in frame end: " + str(data))
                    self._state = com_state.START_OF_FRAME
            
        return ControllerEvent(EventType.EMPTY, b'')