import urwid

class FileButton(urwid.Button):
    def __init__(self, file=None, callback=None):
        super(FileButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback)
        if isinstance(file, str):
            self.caption = file
        else:
            self.file = file
            if file.is_dir():
                self.caption = "/"+file.name
            else:
                self.caption = "~"+file.name
        cur_pos = len(self.caption) + 1 # chowa kursor
        self._w = urwid.AttrMap(urwid.SelectableIcon(self.caption, cur_pos), 'file', focus_map='focus')
    
class Pane(urwid.ListBox):
    def __init__(self, name, path, pm, removing=False):
        self.name = name
        self.pm = pm
        self.currentdir = path
        self.removing = removing
        content = [
            FileButton("/..", self.parentdir_clicked)
        ]
        for f in self.pm.list_dir(self.currentdir):
            button = FileButton(f, self.filebutton_clicked)
            content.append(button)
        self.body = urwid.SimpleFocusListWalker(content)
        super(Pane, self).__init__(self.body)
        self._w = urwid.AttrMap(self, 'pane')

    def filebutton_clicked(self, filebutton):
        file = filebutton.file
        if file.is_dir():
            self.currentdir = file
            self.pm.header.set_text(filebutton.caption)
            self.update_content()

    def parentdir_clicked(self, filebutton):
        self.currentdir = self.currentdir.parent
        self.update_content()

    def update_header(self):
        self.pm.header.set_text(str(self.currentdir))

    def update_content(self):
        self.update_header()
        del self.body[1:]
        for f in self.pm.list_dir(self.currentdir):
            button = FileButton(f, self.filebutton_clicked)
            self.body.append(button)

    def copy(self):
        other_pane = self.pm.get_other_pane(self.name)
        src = self.focus.file
        dest = other_pane.currentdir
        self.pm.copy(src, dest)
        other_pane.update_content()
        self.update_content()

    def move(self):
        other_pane = self.pm.get_other_pane(self.name)
        src = self.focus.file
        dest = other_pane.currentdir
        self.pm.move(src, dest)
        other_pane.update_content()
        self.update_content()

    def remove(self):
        """Funkcja kasuje poprawnie, jest zakomentowana „w razie czego”"""
        src = self.focus.file
        if self.removing:
            self.pm.remove(src)
            self.update_content()
        else:
            self.pm.header.set_text("Usunięto by '{}'".format(src.name)) 

    def keypress(self, size, key):
        key = super(Pane, self).keypress(size, key)
        fp = self.focus_position
        if key in ('f8', 'q'):
            raise urwid.ExitMainLoop()
        elif key == 'f1':
            self.pm.header.set_text("Pokazuje pomoc")
        elif key == 'f2':
            self.copy()
        elif key == 'f3':
            self.move()
        elif key == 'f4':
            self.pm.header.set_text("Tworzę folder")
        elif key == 'f5':
            self.pm.header.set_text("Zmieniam nazwę")
        elif key == 'f6':
            self.remove()
        elif key == 'f7':
            self.pm.switch_hidden()
        elif key == 'left':
            if self.pm.active_pane != 0:
                self.pm.switch_active_pane()
            return key
        elif key == 'right':
            if self.pm.active_pane != 1:
                self.pm.switch_active_pane()
            return key
        else:
            return key
