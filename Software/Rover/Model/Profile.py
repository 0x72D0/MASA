from queue import Queue

from Controller.DabbleGamepadBluetoothController import DabbleGamepadBluetoothController
from Model.Action import Action
from Model.Component import Component
from Model.Mapping import Mapping


class Profile:
    """Class that define one profile."""
    def __init__(self, name) -> None:
        self._name = name
        self._mappings = []
        self._controller = DabbleGamepadBluetoothController()
        self._mappingQueue = Queue()
        self._waiting_for_packet = False
    
    def __getstate__(self):
        return (self._name, self._mappings)
    
    def __setstate__(self, state):
        self._name, self._mappings = state
        self._controller = DabbleGamepadBluetoothController()
        self._mappingQueue = Queue()
        self._waiting_for_packet = False
    
    def cleanup(self):
        self._controller.cleanup()

    def update(self):
        packet = 'a'
        if not self._waiting_for_packet:
            packet = self._controller.readPacket()
            while len(packet) != 0:

                for map in self._mappings:
                    if map.validateInput(packet):
                        self._mappingQueue.put(map)
                
                packet = self._controller.readPacket()
        
    
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
    
