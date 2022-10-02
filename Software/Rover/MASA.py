from Model.Model import Model
from View.LcdView import LcdView
from RPi import GPIO

if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        model = Model()
        lcd = LcdView(model)

        while True:
            lcd.update_lcd_screen()
            model.updateModel()
    finally:
        GPIO.cleanup()