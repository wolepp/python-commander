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
    def __init__(self, show_hidden):
        self.show_hidden = show_hidden
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
        for file in self.sort_paths(self.fm.ls(self.curdir, self.show_hidden)):
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
            self.curdir.parent, self.button_clicked, "/..", backbutton=True
        )

    def button_clicked(self, filebutton: FileButton):
        if not filebutton.filepath.is_dir():
            return
        self.open_dir(filebutton.filepath)
        self.update_content()

    def update_content(self, show_hidden=None, preserve_focus=False):
        if not show_hidden is None:
            self.show_hidden = show_hidden

        if preserve_focus:
            fp = self.focus_position
        del self.body[0:]
        self.body.append(self.make_parent_button())
        self.body.extend(self.make_filebuttons())
        if preserve_focus:
            while fp >= len(self.body):
                fp -= 1
            self.set_focus(fp)

    def is_back_button_focused(self):
        return self.focus.backbutton

    def open_dir(self, path: Path) -> None:
        self.curdir = path

    def get_focus_filepath(self) -> Path:
        return self.focus.filepath

    def keypress(self, size, key):
        key = super(Pane, self).keypress(size, key)
        return key

if __name__ == "__main__":

    pane = Pane()

    palette = [
        ('pane', 'white', 'light blue'),
        ('filebutton', 'white', 'dark blue'),
        ('filebutton_focus', 'black,bold', 'light blue'),
    ]

    loop = urwid.MainLoop(pane, palette)
    loop.run()