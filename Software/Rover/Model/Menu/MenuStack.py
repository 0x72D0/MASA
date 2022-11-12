from collections import deque


class MenuStack:

    def __init__(self, initial_menu) -> None:
        self._needScreenRefresh = False
        self._stack = deque()
        self._stack.append(initial_menu)
    
    def add(self, context):
        self._needScreenRefresh = True
        self._stack.append(context)
    
    def pop(self):
        self._needScreenRefresh = True
        self._stack.pop()
        self._stack[-1].go_back()
    
    def needScreenRefresh(self):
        temp = self._needScreenRefresh
        self._needScreenRefresh = False
        return temp
    
    def get_top(self):
        return self._stack[-1]
