from matplotlib.cbook import ls_mapper
from Model.GraphicPage import GraphicPage
from Model.Model import Model
from RPLCD import CharLCD
from RPi import GPIO


class LcdView:
    def __init__(self, model: Model) -> None:
        self._model = model
        self._lcd = CharLCD(cols=16, rows=2, pin_rs=22, pin_e=18, pins_data=[16, 11, 12, 15], numbering_mode=GPIO.BOARD)

        self.SELECT_ARROW_CHAR = ( 0b00000, 0b00100, 0b00110, 0b11111, 0b11111, 0b00110, 0b00100, 0b00000 )


    def update_lcd_screen(self):
        currentGraphicPage = self._model.getCurrentGraphicPage()

        if currentGraphicPage == GraphicPage.MAIN:
            self._drawMainPage()
        
        self._drawCursor()
    
    def _drawMainPage(self):
        self._lcd.cursor_pos = (0,1)
        self._lcd.write_string(u'Monitor >')
        self._lcd.cursor_pos = (1,1)
        self._lcd.write_string(u'Controller >')
    
    def _drawCursor(self):
        self._loadingMenuChar()
        self._lcd.cursor_pos = (0,0)
        self._lcd.write_string('\x00')

    def _loadingMenuChar(self):
        self._lcd.create_char(0, self.SELECT_ARROW_CHAR)
    
        