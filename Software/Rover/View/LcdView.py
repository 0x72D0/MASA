from matplotlib.cbook import ls_mapper
from Model.GraphicPage import GraphicPage
from Model.Model import Model
from RPLCD import CharLCD
from RPi import GPIO

import Pinout


class LcdView:
    def __init__(self, model: Model) -> None:
        self.COL = 20
        self.ROW = 4

        self._model = model
        self._lcd = CharLCD(cols=self.COL, rows=self.ROW, pin_rs=Pinout.LCD_RS_PIN, pin_e=Pinout.LCD_E_PIN, pins_data=[Pinout.LCD_D1_PIN, Pinout.LCD_D2_PIN, Pinout.LCD_D3_PIN, Pinout.LCD_D4_PIN], numbering_mode=GPIO.BOARD)
        self._lcd.clear()

        self._currentCursorPos = 1
        self._lastSubPage = 0

        self.SELECT_ARROW_CHAR = ( 0b00000, 0b00100, 0b00110, 0b11111, 0b11111, 0b00110, 0b00100, 0b00000 )


    def update(self):
        currentGraphicPage = self._model.getCurrentGraphicPage()
        currentCursor = self._model.getCurrentCursor()

        if self._lastSubPage != currentCursor // self.ROW:
            self._lcd.clear()
            self._lastSubPage = currentCursor // self.ROW

        if currentGraphicPage == GraphicPage.MAIN:
            self._drawMainPage(currentCursor)
        
        if currentCursor != self._currentCursorPos:
            self._drawCursor(currentCursor)
    
    def _drawMainPage(self, cursorPos):
        if cursorPos < 4:
            self._lcd.cursor_pos = (0,2)
            self._lcd.write_string(u'Monitor >')
            self._lcd.cursor_pos = (1,2)
            self._lcd.write_string(u'Pairing >')
            self._lcd.cursor_pos = (2,2)
            self._lcd.write_string(u'Controller >')

            self._lcd.cursor_pos = (3,0)
            self._lcd.write_string(u'v')
        
        elif cursorPos < 8:
            self._lcd.cursor_pos = (0,2)
            self._lcd.write_string(u'Test >')

            self._lcd.cursor_pos = (0,0)
            self._lcd.write_string(u'^')
            
    
    def _drawCursor(self, position):
        if position >= self.ROW:
            position = position % 4

        self._loadingMenuChar()
        self._lcd.cursor_pos = (self._currentCursorPos, 1)
        self._lcd.write_string(u" ")

        self._lcd.cursor_pos = (position % 4, 1)
        self._lcd.write_string('\x00')

        self._currentCursorPos = position

    def _loadingMenuChar(self):
        self._lcd.create_char(0, self.SELECT_ARROW_CHAR)
    
        