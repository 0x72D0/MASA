from Controller.CustomBluetoothController import CustomBluetoothController
from Model.Menu import Menu
from Model.GraphicPage import GraphicPage
from View.ServoMotorView import ServoMotorView

class Model:
    def __init__(self) -> None: 
        self._menu = Menu()
        self._controller = CustomBluetoothController()
        self._servo = ServoMotorView()
        self._test = True
        self._test_channel = 15

    def getCurrentGraphicPage(self) -> GraphicPage:
        return self._menu.getCurrentGraphicPage()
    
    def getCurrentCursor(self) -> int:
        return self._menu.getCurrentIndex()
    
    def updateModel(self):
        self._menu.updateMenu()
        recv = self._controller.readPacket()

        if recv == b'\xaa\x01\x00\xbb\r\n':
            if self._test:
                self._servo.write_angle(self._test_channel, 20)
                self._test = False
            else:
                self._servo.write_angle(self._test_channel, 1)
                self._test = True
            print("receive packet")