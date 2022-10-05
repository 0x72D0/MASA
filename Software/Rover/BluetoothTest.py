import serial

s = serial.Serial("/dev/rfcomm0")
try:
    while True:
        data = s.read(1)
        if data:
            print(data)
except Exception as e:
    print(f'Something went wrong: {e}')
    s.close()