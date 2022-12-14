from Model.Component import ComponentType
from Model.Menu.Menu import Menu
from Model.Model import Model
from RPLCD import CharLCD
from RPi import GPIO

import copy
import HardwareMapping
from Model.Menu.MenuType import MenuType


class LcdView:
    """Class that control the lcd2004"""
    def __init__(self, menu: Menu) -> None:
        self.DEBUG_TERMINAL = True

        self.COL = 20
        self.ROW = 4

        self._menu = menu
        self._lcd = CharLCD(cols=self.COL, rows=self.ROW, pin_rs=HardwareMapping.LCD_RS_PIN, pin_e=HardwareMapping.LCD_E_PIN, pins_data=[HardwareMapping.LCD_D0_PIN, HardwareMapping.LCD_D1_PIN, HardwareMapping.LCD_D2_PIN, HardwareMapping.LCD_D3_PIN], numbering_mode=GPIO.BOARD)

        self._lcd.clear()
        self._lcd_write_string("Test")
        self._currentCursorPos = 1
        self._lastSubPage = 0

        # keep last variable to know if we need refreshing.
        self._lastArg = []
        self._lastCursorPos = 0
        self._lastMenuType = MenuType.NONE

        self.SELECT_ARROW_CHAR = ( 0b00000, 0b00100, 0b00110, 0b11111, 0b11111, 0b00110, 0b00100, 0b00000 )
        self.UP_ARROW_CHAR = ( 0b00100, 0b01110, 0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00000 )
        self.CHECK_MARK = ( 0b00000, 0b00000, 0b00000, 0b00000, 0b00001, 0b00010, 0b10100, 0b01000 )

        self._loadingMenuChar()
        self._lcd.clear()


    def update(self):
        currentMenuType, args = self._menu.get_currentMenuType()
        currentCursor = self._menu.get_currentIndex()

        if(self._compare_two_args(self._lastArg, args) and self._lastMenuType == currentMenuType and self._lastCursorPos == currentCursor):
            return
        
        self._lastArg = args
        self._lastMenuType = currentMenuType
        self._lastCursorPos = currentCursor

        if self._menu.needScreenRefresh():
            self._lcd.clear()
        
        if currentMenuType == MenuType.NONE:
            return

        elif currentMenuType == MenuType.LIST:
            self._drawList(currentCursor, args)
        
        elif currentMenuType == MenuType.STILL_MESSAGE:
            self._drawStillMessage(args)
        
        elif currentMenuType == MenuType.NUMBER_ARGUMENT:
            self._drawNumberArgument(args)
        
        elif currentMenuType == MenuType.INPUT_CHAR:
            self._drawInputChar(args)
        
        elif currentMenuType == MenuType.COMPONENT_LIST:
            self._drawComponentList(currentCursor, args)
        
        elif currentMenuType == MenuType.MONITOR:
            self._drawMonitor(args)
        
        else:
            raise(NotImplementedError("LCD Menu type not implemented yet"))
    
    def _drawList(self, cursorPos, args: list[str]):
        currentSubPage = cursorPos // self.ROW

        if self._lastSubPage != currentSubPage:
            self._lcd.clear()
            self._lastSubPage = currentSubPage

        # manage the case where nothing is in the list
        print_args = copy.deepcopy(args)
        for i in range((currentSubPage*4+4)-len(args)):
            print_args.append(u' ')

        self._lcd.cursor_pos = (0,2)
        self._lcd_write_string(print_args[currentSubPage*4+0])
        self._lcd.cursor_pos = (1,2)
        self._lcd_write_string(print_args[currentSubPage*4+1])
        self._lcd.cursor_pos = (2,2)
        self._lcd_write_string(print_args[currentSubPage*4+2])
        self._lcd.cursor_pos = (3,2)
        self._lcd_write_string(print_args[currentSubPage*4+3])

        if cursorPos != self._currentCursorPos:
            self._drawCursor(cursorPos)
    
    def _drawStillMessage(self, args: list[str]):
        self._lcd.cursor_pos = (1,0)
        self._lcd_write_string(args[0])
    
    def _drawNumberArgument(self, args: list[str]):
        self._lcd.cursor_pos = (1,0)
        self._lcd_write_string(args[0])
        self._lcd.cursor_pos = (2,10)
        self._lcd_write_string(str(args[1]))
    
    def _drawInputChar(self, args: list[str]):
        self._lcd.cursor_pos = (1,0)
        self._lcd_write_string("Input string:")
        
        self._lcd.cursor_pos = (2,10)
        self._lcd_write_string(args[0])
    
    def _drawCursor(self, position: int):
        if position >= self.ROW:
            position = position % self.ROW

        self._lcd.cursor_pos = (self._currentCursorPos, 1)
        self._lcd_write_string(u" ")

        self._lcd.cursor_pos = (position, 1)
        self._lcd_write_string(u'\x00')

        self._currentCursorPos = position
        self._debug_string("current Cursor Position: " + str(self._currentCursorPos))
    
    def _drawComponentList(self, cursorPos, args: list[int]):
        self._lcd.cursor_pos = (0,0)
        self._lcd_write_string("Choose Component:")
        
        for i in range(args[0]):
            self._lcd.cursor_pos = (1,i*2)
            self._lcd_write_string(" " + str(i))
        
        # drawing cursor
        if cursorPos != self._currentCursorPos:
            self._lcd.cursor_pos = (2, (self._currentCursorPos*2)+1)
            self._lcd_write_string(u" ")

            self._lcd.cursor_pos = (2, (cursorPos*2)+1)
            self._lcd_write_string(u'\x01')

            self._currentCursorPos = cursorPos
            self._debug_string("current Cursor Position: " + str(self._currentCursorPos))
    
    def _drawMonitor(self, args: list[ComponentType, int]):
        if(len(args) >= 3):
            self._lcd.cursor_pos = (0,0)
            self._lcd_write_string(self._writeMonitorString(args[0], args[1], args[2]))
        if(len(args) >= 6):
            self._lcd.cursor_pos = (1,0)
            self._lcd_write_string(self._writeMonitorString(args[3], args[4], args[5]))
        if(len(args) >= 9):
            self._lcd.cursor_pos = (2,0)
            self._lcd_write_string(self._writeMonitorString(args[6], args[7], args[8]))
        if(len(args) >= 12):
            self._lcd.cursor_pos = (3,0)
            self._lcd_write_string(self._writeMonitorString(args[9], args[10], args[11]))

    def _writeMonitorString(self, componentType: ComponentType, position: int , data: int) -> str:
        if componentType == ComponentType.SERVO_MOTOR:
            return "servo " + str(position) + ": " + str(data).rjust(3, "0") + " deg"
        if componentType == ComponentType.DC_MOTOR:
            return "motor " + str(position) + ": " + str(data).rjust(3, "0") + " %"
        if componentType == ComponentType.STEPPER:
            return "stepper " + str(position) + ": " + str(data).rjust(3, "0") + " step"

    def _loadingMenuChar(self):

        # Only 8 char can be loaded
        self._lcd.create_char(0, self.SELECT_ARROW_CHAR)
        self._lcd.create_char(1, self.UP_ARROW_CHAR)
        self._lcd.create_char(2, self.CHECK_MARK)
    
    def _lcd_write_string(self, string: str):
        self._debug_string(string)
        self._lcd.write_string(string)
    
    def _debug_string(self, string: str):
        if self.DEBUG_TERMINAL:
            print(string)
    
    def _compare_two_args(self, args1: list, args2: list):
        if len(args1) != len(args2):
            return False
        
        for i in range(len(args1)):
            if(type(args1[i]) != type(args2[i])):
                return False
            
            if(type(args1[i]) is str):
                if(args1[i] != args2[i]):
                    return False
            
            elif(type(args1[i] is int)):
                if(args1[i] != args2[i]):
                    return False
            
            else:
                print("LCDView._compare_two_args: unknow args: " + str(type(args1)))
                print("refreshing screen!")
                return False
        
        return True