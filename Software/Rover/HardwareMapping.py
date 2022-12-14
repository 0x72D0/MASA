from Model.Component import Component, ComponentType
from View.PCA9535View import PCA9535Config
from View.PCA9685View import PCA9685Config

# contains all pinout definition

ROTARY_ENCODER_D2_PIN=40
ROTARY_ENCODER_D3_PIN=38
ROTARY_ENCODER_SW_PIN=19

BACK_BUTTON_PIN=23

LCD_RS_PIN=22 # on the board it's RW
LCD_E_PIN=18 # on the board it's RS
#LCD_RW_PIN=36 # on the board it's E

LCD_D0_PIN=11
LCD_D1_PIN=13
LCD_D2_PIN=15
LCD_D3_PIN=12

# contains I2C addressing

PCA_0_PORT = 0x01
PCA_0_ADDR = 0x70

PCA_1_PORT = 0x01
PCA_1_ADDR = 0x20

# contains PCA9685 configuration

PCA_0_CONFIG = [
    PCA9685Config([9, 8], Component(ComponentType.DC_MOTOR, 0)),
    PCA9685Config([11, 10], Component(ComponentType.DC_MOTOR, 1)),
    PCA9685Config([13, 12], Component(ComponentType.DC_MOTOR, 2)),
    PCA9685Config([15, 14], Component(ComponentType.DC_MOTOR, 3)),
    PCA9685Config([4], Component(ComponentType.SERVO_MOTOR, 0)), 
    PCA9685Config([5], Component(ComponentType.SERVO_MOTOR, 1)), 
    PCA9685Config([6], Component(ComponentType.SERVO_MOTOR, 2)), 
    PCA9685Config([7], Component(ComponentType.SERVO_MOTOR, 3))
    ]

PCA_1_CONFIG = [
    PCA9535Config([11, 12, 8, 9, 10], Component(ComponentType.STEPPER, 0)),
    PCA9535Config([1, 0, 4, 3, 2], Component(ComponentType.STEPPER, 1)),
    ]