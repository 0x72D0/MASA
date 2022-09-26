from Model.GraphicPage import GraphicPage
from Controller.ButtonController import ButtonController
from Controller.RotaryEncoderController import RotaryEncoderController

class Menu:
    _currentGraphicPage = GraphicPage.MAIN
    _encoder = RotaryEncoderController()
    _backButton = ButtonController()