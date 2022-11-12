from Model.Menu.Menu import Menu
from Model.Model import Model
from RPLCD import CharLCD
from RPi import GPIO

import HardwareMapping
from Model.Menu.MenuType import MenuType


class LcdView:
    """Class that control the lcd2004"""
    def __init__(self, menu: Menu) -> None:
        self.COL = 20
        self.ROW = 4

        self._menu = menu
        self._lcd = CharLCD(cols=self.COL, rows=self.ROW, pin_rs=HardwareMapping.LCD_RS_PIN, pin_e=HardwareMapping.LCD_E_PIN, pins_data=[HardwareMapping.LCD_D1_PIN, HardwareMapping.LCD_D2_PIN, HardwareMapping.LCD_D3_PIN, HardwareMapping.LCD_D4_PIN], numbering_mode=GPIO.BOARD)

        self._currentCursorPos = 1
        self._lastSubPage = 0

        self.SELECT_ARROW_CHAR = ( 0b00000, 0b00100, 0b00110, 0b11111, 0b11111, 0b00110, 0b00100, 0b00000 )
        self.UP_ARROW_CHAR = ( 0b00100, 0b01110, 0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00000 )

        self._loadingMenuChar()
        self._lcd.clear()


    def update(self):
        currentMenuType, args = self._menu.get_currentMenuType()
        currentCursor = self._menu.get_currentIndex()

        if self._menu.needScreenRefresh():
            self._lcd.clear()

        if currentMenuType == MenuType.LIST:
            self._drawList(currentCursor, args)
        
        if currentMenuType == MenuType.STILL_MESSAGE:
            self._drawStillMessage(args)
        
        if currentMenuType == MenuType.NUMBER_ARGUMENT:
            self._drawNumberArgument(args)
        
        if currentMenuType == MenuType.INPUT_CHAR:
            self._drawInputChar(args)
        
        if currentMenuType == MenuType.COMPONENT_LIST:
            self._drawComponentList(currentCursor, args)
    
    def _drawList(self, cursorPos, args: list):
        currentSubPage = cursorPos // self.ROW

        if self._lastSubPage != currentSubPage:
            self._lcd.clear()
            self._lastSubPage = currentSubPage

        # manage the case where nothing is in the list
        for i in range((currentSubPage*4+4)-len(args)):
            args.append(u' ')

        self._lcd.cursor_pos = (0,2)
        self._lcd.write_string(args[currentSubPage*4+0])
        self._lcd.cursor_pos = (1,2)
        self._lcd.write_string(args[currentSubPage*4+1])
        self._lcd.cursor_pos = (2,2)
        self._lcd.write_string(args[currentSubPage*4+2])
        self._lcd.cursor_pos = (3,2)
        self._lcd.write_string(args[currentSubPage*4+3])

        if cursorPos != self._currentCursorPos:
            self._drawCursor(cursorPos)
    
    def _drawStillMessage(self, args: list):
        self._lcd.cursor_pos = (1,0)
        self._lcd.write_string(args[0])
    
    def _drawNumberArgument(self, args: list):
        self._lcd.cursor_pos = (1,0)
        self._lcd.write_string(args[0])
        self._lcd.cursor_pos = (2,10)
        self._lcd.write_string(str(args[1]))
    
    def _drawInputChar(self, args: list):
        self._lcd.cursor_pos = (1,0)
        self._lcd.write_string("Input string:")
        self._lcd.cursor_pos = (2,10)
        self._lcd.write_string(args[0])
    
    def _drawCursor(self, position):
        if position >= self.ROW:
            position = position % self.ROW

        self._lcd.cursor_pos = (self._currentCursorPos, 1)
        self._lcd.write_string(u" ")

        self._lcd.cursor_pos = (position, 1)
        self._lcd.write_string(u'\x00')

        self._currentCursorPos = position
    
    def _drawComponentList(self, cursorPos, args: list):
        self._lcd.cursor_pos = (0,0)
        self._lcd.write_string("Choose Component:")
        
        for i in range(args[0]):
            self._lcd.cursor_pos = (1,i*2)
            self._lcd.write_string(" " + str(i))
        
        # drawing cursor
        if cursorPos != self._currentCursorPos:
            self._lcd.cursor_pos = (2, (self._currentCursorPos*2)+1)
            self._lcd.write_string(u" ")

            self._lcd.cursor_pos = (2, (cursorPos*2)+1)
            self._lcd.write_string(u'\x01')

            self._currentCursorPos = cursorPos

    def _loadingMenuChar(self):
        self._lcd.create_char(0, self.SELECT_ARROW_CHAR)
        self._lcd.create_char(1, self.UP_ARROW_CHAR)
    
        