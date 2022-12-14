import HardwareMapping
from Controller.encoder import Encoder

class RotaryEncoderController():
    """Control the Rotary Encoder input."""
    def __init__(self):
        self._encoder = Encoder(HardwareMapping.ROTARY_ENCODER_D3_PIN, HardwareMapping.ROTARY_ENCODER_D2_PIN)

    def getValue(self):
        return self._encoder.getValue()
    
    def setValue(self, value):
        return self._encoder.setValue(value)