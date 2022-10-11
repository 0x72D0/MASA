from Controller.CustomBluetoothController import CustomBluetoothController
from Model.ComponentType import ComponentType
from Model.Profile import Profile
from Model.Menu.GraphicPage import GraphicPage
from Model.ServoMotor import ServoMotor

class Model:
    def __init__(self) -> None:
        self.SERVO_NUM = 8

        self._currentProfile = Profile()

        self._servos = [ServoMotor()] * self.SERVO_NUM

    def getServosAngle(self) -> list:
        tempList = []
        for servo in self._servos:
            tempList.append(servo.getAngle())
        return tempList

    
    def update(self):
        self._currentProfile.update()

        while not self._currentProfile.actionIsEmpty():
            mapping = self._currentProfile.get_nextMapping()
            
            if mapping.get_componentType() == ComponentType.SERVO_MOTOR:
                self._servos[mapping.get_componentPosition()].update(mapping.get_action())