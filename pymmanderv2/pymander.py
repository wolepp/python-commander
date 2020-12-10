import urwid
from pane import Pane

LEFT_ARROW = "<<"
RIGHT_ARROW = ">>"

class PyMander(urwid.Frame):
    def __init__(self):
        self.panes = urwid.AttrMap(urwid.Columns([Pane(), Pane()], 2), 'columns')
        self.active_pane = 0
        self.arrow = LEFT_ARROW
        super(PyMander, self).__init__(self.panes)
        self._w = urwid.AttrMap(self, 'pymander')

    def set_active_pane(self, pane_number: int):
        self.active_pane = pane_number
        if pane_number == 0:
            self.arrow = LEFT_ARROW
        elif pane_number == 1:
            self.arrow = RIGHT_ARROW
        
    def keypress(self, size, key):
        key = super(PyMander, self).keypress(size, key)
        if key in ('f8', 'q'):
            raise urwid.ExitMainLoop()
        elif key == 'left':
            self.set_active_pane(0)
        elif key == 'right':
            self.set_active_pane(1)
        else:
            return key
