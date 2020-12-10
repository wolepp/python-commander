#!/usr/bin/env python

import urwid
from pymander import PyMander

if __name__ == "__main__":
    
    pm = PyMander()

    palette = [
        ('columns', 'dark red', 'dark blue'),
        ('pane', 'white', 'light blue'),
        ('filebutton', 'white', 'dark blue'),
        ('filebutton_focus', 'black,bold', 'light blue'),
    ]

    loop = urwid.MainLoop(pm, palette=palette)
    loop.run()
