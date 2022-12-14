import time
import HardwareMapping

from RPi import GPIO

class ButtonController():
    """Controller that control all the input for the GPIO button."""
    __rotaryEncoderSwState = 0
    __rotaryEncoderLastTime = 0
    __backButtonState = 0
    __backButtonLastTime = 0
    __debouncingSeconds = 0.5

    def __init__(self):
        GPIO.setup(HardwareMapping.ROTARY_ENCODER_SW_PIN, GPIO.IN)
        GPIO.add_event_detect(HardwareMapping.ROTARY_ENCODER_SW_PIN, GPIO.BOTH, callback=ButtonController.rotaryEncoderSwCallback)
        GPIO.setup(HardwareMapping.BACK_BUTTON_PIN, GPIO.IN)
        GPIO.add_event_detect(HardwareMapping.BACK_BUTTON_PIN, GPIO.BOTH, callback=ButtonController.backButtonCallback)

    def get_rotaryEncoderButtonState(self):
        tempState = ButtonController.__rotaryEncoderSwState
        ButtonController.__rotaryEncoderSwState = 0
        return tempState
    
    def get_backButtonState(self):
        tempState = ButtonController.__backButtonState
        ButtonController.__backButtonState = 0
        return tempState

    def rotaryEncoderSwCallback(channel):
        # if there's a falling edge
        if time.time() - ButtonController.__rotaryEncoderLastTime > ButtonController.__debouncingSeconds:
            if GPIO.input(HardwareMapping.ROTARY_ENCODER_SW_PIN):
                ButtonController.__rotaryEncoderSwState = 1
                ButtonController.__rotaryEncoderLastTime = time.time()

    def backButtonCallback(channel):
        # if there's a falling edge
        if time.time() - ButtonController.__backButtonLastTime > ButtonController.__debouncingSeconds:
            if GPIO.input(HardwareMapping.BACK_BUTTON_PIN):
                ButtonController.__backButtonState = 1
                ButtonController.__backButtonLastTime = time.time()
