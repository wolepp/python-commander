#!/usr/bin/env python

import argparse

if __name__ == "__main__":

    description = """
Menadżer plików na wzór Midnight Commandera.

Do działania wymaga pakietu 'urwid'
Instalacja: `pip install urwid`
(lub inaczej, w zależności od używanego menadżera pakietów).

Program interaktywny.
Sterowanie przy pomocy strzałek klawiatury.
Przechodzenie między folderami przy pomocy Enter.

Program oferuje różne operacje na plikach i folderach (w tym ukrytych):
kopiowanie, przenoszenie, zmianę nazwy, kasowanie, tworzenie nowych folderów.

Operacja kasowania wymaga potwierdzenia (kasuje nieodwracalnie, tak jak 'rm').
Można anulować wykonywanie operacji kasowania, tworzenia nowego folderu lub zmiany nazwy przez wciśnięcie Escape.
    """

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    args = parser.parse_args()

    import urwid
    from pymander import PyMander
    pm = PyMander()

    palette = [
        ('columns', 'dark red', 'dark blue'),
        ('pane', 'white', 'light blue'),
        ('filebutton', 'white', 'dark blue'),
        ('filebutton_focus', 'black,bold', 'light blue'),
    ]

    loop = urwid.MainLoop(pm, palette=palette)
    loop.run()
