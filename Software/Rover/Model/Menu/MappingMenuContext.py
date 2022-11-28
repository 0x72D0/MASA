from Controller.RotaryEncoderController import RotaryEncoderController
from Controller.ButtonController import ButtonController
from Model.Menu.IMenuContext import IMenuContext
from Model.Menu.MenuStack import MenuStack
from Model.Menu.MenuType import MenuType
from Model.Model import Model


class MappingMenuContext(IMenuContext):
    """Menu context that chains multiple state to configure a profile item"""
    def __init__(self, model: Model, chains: list[IMenuContext]) -> None:
        super().__init__(model)
        self._currentChain = 0
        self._menuChains = chains
        self._getBack = False

    def get_menuStructure(self) -> tuple:
        return MenuType.NONE, []
    
    def goBack(self):
        self._getBack = True
    
    def update(self, encoderHandle: RotaryEncoderController, buttonHandle: ButtonController, menuStack: MenuStack) -> None:
        if self._getBack:
            menuStack.pop()
            return

        if self._currentChain == len(self._menuChains):
            menuStack.pop()
            return
        
        menuStack.add(self._menuChains[self._currentChain])
        self._currentChain += 1