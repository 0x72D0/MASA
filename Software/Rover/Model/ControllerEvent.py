from enum import Enum


class EventType(Enum):
    EMPTY = 0
    DIGITAL = 1
    ANALOG = 2

class ControllerEvent:

    def __init__(self, eventType: EventType, event: bytes) -> None:
        self.eventType = eventType
        self.event = event

    def compareEvent(self, event: bytes) -> bool:
        return self.event == event
    
    def compareEventType(self, eventType: EventType) -> bool:
        return self.eventType == eventType
    
    def get_event(self) -> bytes:
        return self.event