import urwid
from filemanager import FileManager
from pathlib import Path
from typing import Sequence

from filebutton import FileButton

SORT_DIR_VAL  = "0"
SORT_HID_DIR_VAL = "10"
SORT_FILE_VAL = "20"
SORT_HID_FILE_VAL = "30"

class Pane(urwid.ListBox):
    def __init__(self):
        self.fm = FileManager()
        self.curdir = Path.home()
        self.initialize_body()
        super(Pane, self).__init__(self.body)
        self._w = urwid.AttrWrap(self, 'pane')

    def initialize_body(self):
        content = [self.make_parent_button()]
        content.extend(self.make_filebuttons())
        self.body = urwid.SimpleFocusListWalker(content)

    def make_filebuttons(self):
        filebuttons = []
        for file in self.sort_paths(self.fm.ls(self.curdir)):
            button = FileButton(file, self.button_clicked)
            filebuttons.append(button)
        return filebuttons
        
    def sort_paths(self, paths: Sequence[Path]) -> Sequence[Path]:
        def get_sort_val(path: Path):
            if path.is_dir():
                if path.name[0] == '.':
                    return SORT_HID_DIR_VAL
                else:
                    return SORT_DIR_VAL
            else:
                if path.name[0] == '.':
                    return SORT_HID_FILE_VAL
                else:
                    return SORT_FILE_VAL

        return sorted(paths, key=lambda path: get_sort_val(path) + str(path).lower())

    def make_parent_button(self):
        return FileButton(
            self.curdir.parent, self.button_clicked, "/.."
        )

    def button_clicked(self, filebutton: FileButton):
        if not filebutton.filepath.is_dir():
            return
        self.open_dir(filebutton.filepath)
        self.update_content()

    def update_content(self):
        del self.body[0:]
        self.body.append(self.make_parent_button())
        self.body.extend(self.make_filebuttons())

    def test(self):
        print(self.fm.ls(Path.home()))

    def open_dir(self, path: Path) -> None:
        self.curdir = path

    def keypress(self, size, key):
        key = super(Pane, self).keypress(size, key)
        fp = self.focus_position
        if key in ('f8', 'q'):
            raise urwid.ExitMainLoop()
        # elif key == 'f1':
        #     self.pm.header.set_text("Pokazuje pomoc")
        # elif key == 'f2':
        #     self.copy()
        # elif key == 'f3':
        #     self.move()
        # elif key == 'f4':
        #     self.pm.header.set_text("Tworzę folder")
        # elif key == 'f5':
        #     self.pm.header.set_text("Zmieniam nazwę")
        # elif key == 'f6':
        #     self.remove()
        # elif key == 'f7':
        #     self.pm.switch_hidden()
        # elif key == 'left':
        #     if self.pm.active_pane != 0:
        #         self.pm.switch_active_pane()
        #     return key
        # elif key == 'right':
        #     if self.pm.active_pane != 1:
        #         self.pm.switch_active_pane()
        #     return key
        # else:
        #     return key

if __name__ == "__main__":

    pane = Pane()

    palette = [
        ('pane', 'white', 'light blue'),
        ('filebutton', 'white', 'dark blue'),
        ('filebutton_focus', 'black,bold', 'light blue'),
    ]

    loop = urwid.MainLoop(pane, palette)
    loop.run()