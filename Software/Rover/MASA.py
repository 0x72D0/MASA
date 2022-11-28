# program entrypoint

import HardwareMapping

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
        pca9685_0 = PCA9685View(model, HardwareMapping.PCA_0_PORT, HardwareMapping.PCA_0_ADDR, HardwareMapping.PCA_0_CONFIG)

        while True:
            model.update()
            menu.update()
            lcd.update()
            pca9685_0.update()
            
    finally:
        GPIO.cleanup()
        model.cleanup()