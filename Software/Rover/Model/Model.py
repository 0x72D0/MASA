from Model.Menu import Menu
from Model.GraphicPage import GraphicPage

class Model:
    def __init__(self) -> None: 
        self._menu = Menu()

    def getCurrentGraphicPage(self) -> GraphicPage:
        return self._menu.getCurrentGraphicPage()
    
    def getCurrentCursor(self) -> int:
        return self._menu.getCurrentIndex()
    
    def updateModel(self):
        self._menu.updateMenu()