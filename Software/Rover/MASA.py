# program entrypoint

from Model.Menu.Menu import Menu
from Model.Model import Model
from View.LcdView import LcdView
from View.PCA9685View import PCA9685View
from RPi import GPIO

if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        model = Model()
        menu = Menu(model)
        lcd = LcdView(menu)
        pca9685 = PCA9685View(model)

        while True:
            model.update()
            menu.update()
            lcd.update()
            pca9685.update()
            
    finally:
        GPIO.cleanup()
        model.cleanup()