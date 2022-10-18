from enum import Enum
import serial

class com_state(Enum):
    START_OF_FRAME = 0
    MODULE_ID = 1
    FUNCTION_ID = 2
    ARG_NO_1 = 3
    ARG_NO_2 = 4
    ARG_DECODE = 5
    END_OF_FRAME = 6


s = serial.Serial(
  port='/dev/serial0',
  baudrate = 9600
)

state = com_state.START_OF_FRAME
i = 0
j = 0
max_i = 0
max_j = 0

try:
    while True:
        data = s.read(1)

        if data == b'':
            continue
        
        if state == com_state.START_OF_FRAME:
            if data == b'\xff':
                print("-----FRAME START-----")
                state = com_state.MODULE_ID
            else:
                print("error in frame start: " + str(data))

        elif state == com_state.MODULE_ID:
            print("Module ID: " + str(data))
            state = com_state.FUNCTION_ID
        
        elif state == com_state.FUNCTION_ID:
            print("Function ID: " + str(data))
            state = com_state.ARG_NO_1

        elif state == com_state.ARG_NO_1:
            print("Numbers of arguments: " + str(data))
            i = 0
            max_i = int.from_bytes(data, "big")
            state = com_state.ARG_NO_2
        
        elif state == com_state.ARG_NO_2:
            print("Numbers of arguments: " + str(data))
            j = 0
            max_j = int.from_bytes(data, "big")
            state = com_state.ARG_DECODE
        
        elif state == com_state.ARG_DECODE:
            print("Arg_" + str(i+1) + "_" + str(j+1) +": " + str(data))
            j += 1
            if j >= max_j:
                i += 1
            if i >= max_i:
                state = com_state.END_OF_FRAME
        
        elif state == com_state.END_OF_FRAME:
            if data == b'\x00':
                print("-----FRAME END-----")
                state = com_state.START_OF_FRAME
            else:
                print("error in frame end: " + str(data))
        
except Exception as e:
    print(f'Something went wrong: {e}')
    s.close()