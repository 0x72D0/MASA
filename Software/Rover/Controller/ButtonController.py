import Pinout

from RPi import GPIO

class ButtonController():
    """Controller that control all the input for the GPIO button."""
    __rotaryEncoderSwState = 0
    __backButtonState = 0

    def __init__(self):
        GPIO.setup(Pinout.ROTARY_ENCODER_SW_PIN, GPIO.IN)
        GPIO.add_event_detect(Pinout.ROTARY_ENCODER_SW_PIN, GPIO.BOTH, callback=ButtonController.rotaryEncoderSwCallback)
        GPIO.setup(Pinout.BACK_BUTTON_PIN, GPIO.IN)
        GPIO.add_event_detect(Pinout.BACK_BUTTON_PIN, GPIO.BOTH, callback=ButtonController.backButtonCallback)

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
        if not GPIO.input(Pinout.ROTARY_ENCODER_SW_PIN):
            ButtonController.__rotaryEncoderSwState = 1

    def backButtonCallback(channel):
        # if there's a falling edge
        if not GPIO.input(Pinout.BACK_BUTTON_PIN):
            ButtonController.__backButtonState = 1
