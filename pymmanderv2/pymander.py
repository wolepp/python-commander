import urwid
from pane import Pane
from footer import Footer

LEFT_ARROW = "<<"
RIGHT_ARROW = ">>"

class PyMander(urwid.Frame):
    def __init__(self):
        self.panes = urwid.AttrMap(urwid.Columns([Pane(), Pane()], 2), 'columns')
        self.active_pane = 0
        self.arrow = LEFT_ARROW
        super(PyMander, self).__init__(self.panes, footer=urwid.BoxAdapter(Footer(), 2))
        self._w = urwid.AttrMap(self, 'pymander')

    def set_active_pane(self, pane_number: int):
        self.active_pane = pane_number
        if pane_number == 0:
            self.arrow = LEFT_ARROW
        elif pane_number == 1:
            self.arrow = RIGHT_ARROW
        
    def keypress(self, size, key):
        # TODO:
        # obsługa enter przenieść tu z footera - działanie zależne od focusu
        key = super(PyMander, self).keypress(size, key)
        if key == 'left':
            self.set_active_pane(0)
        elif key == 'right':
            self.set_active_pane(1)
        elif key == 'f2':
            # copy
            self.footer.set_edit("asdf")
        elif key == 'f3':
            # move
            pass
        elif key == 'f4':
            # mkdir
            pass
        elif key == 'f5':
            # rename
            self.set_focus('body')
        elif key == 'f6':
            # remove
            self.set_focus('footer')
            pass
        elif key == 'f7':
            # switch hidden files
            text = self.footer.original_widget.get_edit_text()
            self.footer.original_widget.top_w.original_widget.set_caption(text)
        elif key == 'enter':
            # TODO: F7 Działa, enter nie działa, bo Edit go obsługuje
            if self.get_focus == 'footer':
                text = self.footer.original_widget.get_edit_text()
                self.footer.original_widget.top_w.original_widget.set_caption(text)
            else: # 'body'
                text = self.footer.original_widget.get_edit_text()
                self.footer.original_widget.top_w.original_widget.set_caption(text)
        elif key in ('f8', 'q'):
            raise urwid.ExitMainLoop()
        else:
            return key
