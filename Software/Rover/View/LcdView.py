from matplotlib.cbook import ls_mapper
from Model.Menu.GraphicPage import GraphicPage
from Model.Menu.Menu import Menu
from Model.Model import Model
from RPLCD import CharLCD
from RPi import GPIO

import Pinout
from Model.Menu.MenuType import MenuType


class LcdView:
    def __init__(self, menu: Menu) -> None:
        self.COL = 20
        self.ROW = 4

        self._menu = menu
        self._lcd = CharLCD(cols=self.COL, rows=self.ROW, pin_rs=Pinout.LCD_RS_PIN, pin_e=Pinout.LCD_E_PIN, pins_data=[Pinout.LCD_D1_PIN, Pinout.LCD_D2_PIN, Pinout.LCD_D3_PIN, Pinout.LCD_D4_PIN], numbering_mode=GPIO.BOARD)
        self._lcd.clear()

        self._currentCursorPos = 1
        self._lastSubPage = 0
        self._lastGraphicPage = None

        self.SELECT_ARROW_CHAR = ( 0b00000, 0b00100, 0b00110, 0b11111, 0b11111, 0b00110, 0b00100, 0b00000 )


    def update(self):
        currentMenuType, args = self._menu.get_currentMenuType()
        currentCursor = self._menu.get_currentIndex()
        currentGraphicPage = self._menu.get_currentGraphicPage()

        if self._lastGraphicPage != currentGraphicPage:
            self._lcd.clear()
            self._lastGraphicPage = currentGraphicPage

        if self._lastSubPage != currentCursor // self.ROW:
            self._lcd.clear()
            self._lastSubPage = currentCursor // self.ROW

        if currentMenuType == MenuType.LIST:
            self._drawList(currentCursor, args)
        
        if currentCursor != self._currentCursorPos:
            self._drawCursor(currentCursor)
    
    def _drawList(self, cursorPos, args: list):
        menuToDraw = cursorPos // 4

        # manage the case where nothing is in the list
        for i in range((menuToDraw*4+4)-len(args)):
            args.append(u' ')

        self._lcd.cursor_pos = (0,2)
        self._lcd.write_string(args[menuToDraw*4+0])
        self._lcd.cursor_pos = (1,2)
        self._lcd.write_string(args[menuToDraw*4+1])
        self._lcd.cursor_pos = (2,2)
        self._lcd.write_string(args[menuToDraw*4+2])
        self._lcd.cursor_pos = (3,2)
        self._lcd.write_string(args[menuToDraw*4+3])
    
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
    
        