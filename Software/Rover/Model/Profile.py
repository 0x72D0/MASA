from queue import Queue

from Controller.CustomBluetoothController import CustomBluetoothController
from Model.Action import Action
from Model.ActionType import ActionType
from Model.Component import Component
from Model.ComponentType import ComponentType
from Model.Mapping import Mapping


class Profile:
    """Class that define one profile."""
    def __init__(self, name) -> None:
        self._name = name
        self._mappings = []
        self._controller = CustomBluetoothController()
        self._mappingQueue = Queue()
        self._waiting_for_packet = False
    
    def __getstate__(self):
        return (self._name, self._mappings)
    
    def __setstate__(self, state):
        self._name, self._mappings = state
        self._controller = CustomBluetoothController()
        self._mappingQueue = Queue()
        self._waiting_for_packet = False


    def update(self):
        packet = 'a'
        if not self._waiting_for_packet:
            while len(packet) != 0:
                packet = self._controller.readPacket()

                for map in self._mappings:
                    if map.validateInput(packet):
                        self._mappingQueue.put(map)
        
    
    def mapNextInputToProfile(self, action: Action, component: Component):
        self._waiting_for_packet = True
        packet = self._controller.readPacket()

        if len(packet) == 0:
            return False
        
        for i in range(len(self._mappings)):
            if self._mappings[i].get_componentType() == component.get_type():
                if self._mappings[i].get_componentPosition() == component.get_position():
                    if self._mappings[i].get_action().get_actionType() == action.get_actionType():
                        self._mappings.pop(i)

        self._mappings.append(Mapping(action, packet, component))
        print("mapping " + str(packet))

        self._waiting_for_packet = False

        return True
    
    def actionIsEmpty(self) -> bool:
        return self._mappingQueue.empty()
    
    def get_nextMapping(self) -> Mapping:
        return self._mappingQueue.get()
    
    def get_name(self) -> str:
        return self._name
    
