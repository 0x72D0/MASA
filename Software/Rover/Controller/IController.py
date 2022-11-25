from Model.ControllerEvent import ControllerEvent


class IController:
    """Interface that all bluetooth controller gonna inherit."""
    def readPacket(self) -> ControllerEvent:
        pass