from queue import Queue

from Controller.CustomBluetoothController import CustomBluetoothController
from Model.Action import Action
from Model.ActionType import ActionType
from Model.Component import Component
from Model.ComponentType import ComponentType
from Model.Mapping import Mapping


class Profile:
    def __init__(self) -> None:
        self._mappings = []
        self._controller = CustomBluetoothController()
        self._mappingQueue = Queue()

    def update(self):
        packet = self._controller.readPacket()

        if packet == b'\xaa\x01\x00\xbb\r\n':
            self._mappingQueue.put(Mapping(Action(ActionType.TOGGLE, [20]), b'\xaa\x01\x00\xbb\r\n', Component(ComponentType.SERVO_MOTOR, 0)))
    
    def actionIsEmpty(self) -> bool:
        return self._mappingQueue.empty()
    
    def get_nextMapping(self) -> Mapping:
        return self._mappingQueue.get()
    
