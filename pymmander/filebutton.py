import urwid
from pathlib import Path

class FileButton(urwid.Button):
    def __init__(self, file: Path, callback, caption=None, backbutton=False):
        super(FileButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback)
        self.backbutton = backbutton

        self.filepath = file
        if not caption is None:
            self.caption = caption
        else:
            if file.is_dir():
                self.caption = "/" + file.name
            else:
                self.caption = "~" + file.name

        self._w = urwid.AttrMap(
            urwid.SelectableIcon(
                self.caption,
                len(self.caption) + 1),
                'filebutton',
                focus_map='filebutton_focus'
        )
