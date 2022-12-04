from Model.Component import Component, ComponentType
from Software.Rover.View.PCA9535View import PCA9535Config
from View.PCA9685View import PCA9685Config

# TODO: verify with yoann version

# contains all pinout definition

ROTARY_ENCODER_D2_PIN=17
ROTARY_ENCODER_D3_PIN=15
ROTARY_ENCODER_SW_PIN=21

BACK_BUTTON_PIN=31

LCD_RS_PIN=39
LCD_E_PIN=37
LCD_RW_PIN=35

LCD_D1_PIN=12
LCD_D2_PIN=14
LCD_D3_PIN=16
LCD_D4_PIN=30

# contains I2C addressing

PCA_0_PORT = 0x01
PCA_0_ADDR = 0x41

PCA_1_PORT = 0x01
PCA_1_ADDR = 0x41

# contains PCA9685 configuration

PCA_0_CONFIG = [
    PCA9685Config([5,4], Component(ComponentType.DC_MOTOR, 0)),
    PCA9685Config([3,2], Component(ComponentType.DC_MOTOR, 1)),
    PCA9685Config([1,0], Component(ComponentType.DC_MOTOR, 2)),
    PCA9685Config([7,6], Component(ComponentType.DC_MOTOR, 3)),
    PCA9685Config([8], Component(ComponentType.SERVO_MOTOR, 0)), 
    PCA9685Config([9], Component(ComponentType.SERVO_MOTOR, 1)), 
    PCA9685Config([10], Component(ComponentType.SERVO_MOTOR, 2)), 
    PCA9685Config([11], Component(ComponentType.SERVO_MOTOR, 3))
    ]

PCA_1_CONFIG = [
    PCA9535Config([0,1,2,3,4], Component(ComponentType.STEPPER, 0)),
    PCA9535Config([8,9,10,11,12], Component(ComponentType.STEPPER, 1)),
    ]