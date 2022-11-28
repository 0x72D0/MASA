from Model.Component import Component, ComponentType
from View.PCA9685View import PCA9685Config

# contains all pinout definition

ROTARY_ENCODER_D2_PIN=38
ROTARY_ENCODER_D3_PIN=40
ROTARY_ENCODER_SW_PIN=19

BACK_BUTTON_PIN=23

LCD_RS_PIN=22
LCD_E_PIN=18
LCD_D1_PIN=16
LCD_D2_PIN=11
LCD_D3_PIN=12
LCD_D4_PIN=15

# contains I2C addressing

PCA_0_PORT = 0x01
PCA_0_ADDR = 0x41

# contains PCA9685 configuration

PCA_0_CONFIG = [PCA9685Config(15, Component(ComponentType.SERVO_MOTOR, 0))]