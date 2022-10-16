from Model.Action import Action
from Model.Component import Component
from Model.ComponentType import ComponentType
from Model.Profile import Profile
from Model.ProfileDatabase import ProfileDatabase
from Model.ServoMotor import ServoMotor

class Model:
    """Singleton that define all the model."""
    def __init__(self) -> None:
        self.SERVO_NUM = 8

        self._profileDatabase = ProfileDatabase()
        self._currentProfileName = ""

        self._servos = [ServoMotor()] * self.SERVO_NUM

    def getServosAngle(self) -> list:
        tempList = []
        for servo in self._servos:
            tempList.append(servo.getAngle())
        return tempList
    
    def startNewProfile(self, name: str):
        self._profileDatabase.newProfile(name)

    def mapNextInputToProfile(self, action: Action, component:Component) -> bool:
        profile = self._profileDatabase.get_profile(self._currentProfileName)
        if profile is None:
            return False
        
        return profile.mapNextInputToProfile(action, component)
    
    def setCurrentProfileName(self, name: str):
        self._currentProfileName = name
    
    def get_profileNameList(self) -> list:
        return self._profileDatabase.get_profilesName()
    
    def update(self):
        self._profileDatabase.save_profiles()
        profile = self._profileDatabase.get_profile(self._currentProfileName)
        if profile is not None:
            profile.update()

            while not profile.actionIsEmpty():
                mapping = profile.get_nextMapping()
                
                if mapping.get_componentType() == ComponentType.SERVO_MOTOR:
                    self._servos[mapping.get_componentPosition()].update(mapping.get_action())