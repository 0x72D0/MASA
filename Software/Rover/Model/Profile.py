from queue import Queue
import copy

from Controller.DabbleGamepadBluetoothController import DabbleGamepadBluetoothController
from Model.Action import Action
from Model.Component import Component
from Model.ControllerEvent import EventType
from Model.Mapping import Mapping


class Profile:
    """Class that define one profile."""
    def __init__(self, name: str) -> None:
        self._name = name
        self._mappings = list[Mapping]()
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
    
    def cleanup(self) -> None:
        self._controller.cleanup()

    def update(self) -> None:
        if not self._waiting_for_packet:
            packet = self._controller.readPacket()

            if packet.compareEventType(EventType.EMPTY):
                return
            
            elif packet.compareEventType(EventType.DIGITAL):
                for map in self._mappings:
                    if (not map.isAnalogicInput()) and map.validateInput(str(packet.get_event())):
                        self._mappingQueue.put(map)
            
            elif packet.compareEventType(EventType.ANALOG):
                for map in self._mappings:
                    if map.isAnalogicInput():
                        analogMap = copy.deepcopy(map)
                        analogMap.add_argument(int(packet.get_event()[0]))
                        print(analogMap.get_action().get_actionArguments())
                        self._mappingQueue.put(analogMap)
        
    
    def mapDigitalInputToProfile(self, action: Action, component: Component) -> bool:
        self._waiting_for_packet = True
        packet = self._controller.readPacket()

        if not packet.compareEventType(EventType.DIGITAL):
            return False
        
        # if the mapping already exist, remove it
        for i in range(len(self._mappings)):
            if self._mappings[i].get_componentType() == component.get_type():
                if self._mappings[i].get_componentPosition() == component.get_position():
                    if self._mappings[i].get_action().get_actionType() == action.get_actionType():
                        self._mappings.pop(i)

        self._mappings.append(Mapping(action, str(packet.get_event()), component))
        print("mapping " + str(packet.get_event()) + "to component position: " + str(component.get_position()))

        self._waiting_for_packet = False
        return True
    
    def mapAnalogicInputToProfile(self, action: Action, component: Component) -> bool:
        self._waiting_for_packet = True
        packet = self._controller.readPacket()

        if not packet.compareEventType(EventType.ANALOG):
            return False

        self._mappings.append(Mapping(action, str(packet.get_event()), component))
        print("mapping " + str(packet.get_event()))

        self._waiting_for_packet = False

        return True
    
    def actionIsEmpty(self) -> bool:
        return self._mappingQueue.empty()
    
    def get_nextMapping(self) -> Mapping:
        return self._mappingQueue.get()
    
    def get_name(self) -> str:
        return self._name
    
