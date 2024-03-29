#!/usr/bin/env python

import os
import shutil
import sys
import getpass
import argparse
from pathlib import Path


palette = [
    ('body', 'white', 'dark blue'),
    ('pane', 'white', 'light blue'),
    ('file', 'white', 'dark blue'),
    ('focus', 'black,bold', 'light blue'),
    ('header', 'light blue', 'black'),
    ('footer', 'light blue', 'black'),
]


class Pymmander():
    """File manager"""

    def __init__(self, removing=False):
        self.root = Path.root
        self.home = Path.home()
        self.currentdir = Path(Path.home())
        self.showHidden = False
        self.removing = removing
        # UI Settings
        self.active_pane = 0
        self.arr = ">>"
        self.hid = "show"
        self.text_header = str(self.currentdir)
        self.header = urwid.AttrWrap(urwid.Text(self.text_header), 'header')
        self.text_footer = self.get_text_footer()
        self.footer = urwid.AttrWrap(urwid.Text(self.text_footer), 'footer')
        self.panes = urwid.Columns(
            [widgets_old.Pane("a", self.currentdir, self, self.removing),
            widgets_old.Pane("b", self.currentdir, self, self.removing)
            ], 3)
        self.top = urwid.AttrMap(urwid.Frame(self.panes, header=self.header, footer=self.footer), 'body')

    def get_text_footer(self):
        return "F2 Copy {} | F3 Move {} | F4 Mkdir | F5 Rename | F6 Remove | F7 {} hidden files | F8/q Quit".format(self.arr, self.arr, self.hid)

    def list_current_dir(self):
        self.list_dir(self.currentdir)
    
    def list_dir(self, path, only_names=False):
        listdir = os.listdir(path)
        if only_names:
            if self.showHidden:
                return listdir
            return list(filter(lambda fname: fname[0] != '.', listdir))

        paths = [path.joinpath(el) for el in listdir]
        if self.showHidden:
            return paths
        return list(filter(lambda path: path.name[0] != '.', paths))

    def switch_active_pane(self):
        if self.active_pane == 0:
            self.active_pane = 1
            self.arr = '<<'
        else:
            self.active_pane = 0
            self.arr = '>>'
        self.header.set_text(str(self.panes[self.active_pane].currentdir))
        self.update_footer()

    def update_footer(self):
        self.text_footer = self.get_text_footer()
        self.footer.set_text(self.text_footer)

    def pathify(self, *names, basedir=None):
        if basedir is None:
            basedir = self.currentdir

        pathified = []
        for name in names:
            if isinstance(name, Path):
                pathified.append(name)
            else:
                pathified.append(Path(self.currentdir, name))
        if len(pathified) == 1:
            return pathified[0]
        return pathified

    def get_other_pane(self, name):
        if name == 'a':
            return self.panes[1]
        elif name == 'b':
            return self.panes[0]
        return None

    def open_dir(self, path):
        path = self.pathify(path)
        if not Path.is_dir(path):
            print("{} nie jest folderem".format(path.name))
        else:
            self.currentdir = path

    def open_parentdir(self):
        self.currentdir = self.currentdir.parent

    def open_home(self):
        self.currentdir = self.home

    def copy(self, src, dest):
        src, dest = self.pathify(src, dest)
        if src.is_dir():
            self._copydir(src, dest)
            return

        try:
            shutil.copy(src, dest)
        except shutil.SameFileError:
            pass

    def _copydir(self, src, dest):
        src, dest = self.pathify(src, dest)
        if not src.is_dir():
            raise AttributeError("{} nie jest folderem".format(src.name))

        try:
            shutil.copytree(src, dest)
        except FileExistsError:
            pass

    def move(self, src, dest):
        src, dest = self.pathify(src, dest)

        src = str(src)
        dest = str(dest)
        try:
            shutil.move(src, dest)
        except shutil.Error:
            pass

    def mkdir(self, name):
        try:
            pm.currentdir.joinpath(name).mkdir()
        except FileExistsError:
            print("{} już istnieje".format(name)) # TODO: wypisać w TUI

    def remove(self, name):
        path = self.pathify(name)

        if path.is_dir():
            shutil.rmtree(path)
        else:
            os.remove(path)

    def rename(self, old, new):
        old, new = self.pathify(old, new)

        if new.exists():
            print("{} już istnieje".format(new.name))
        else:
            old.rename(new)
        

    def switch_hidden(self):
        self.showHidden = not self.showHidden
        if self.showHidden:
            self.hid = "hide"
        else:
            self.hid = "show"
        for (pane, opt) in self.panes.contents:
            pane.update_content()
        self.update_footer()

    def disk_usage(self):
        return shutil.disk_usage(self.currentdir)


if __name__ == "__main__":

    description = """
Menadżer plików na wzór Midnight Commandera.

Do działania wymaga pakietu 'urwid'
Instalacja: `pip install urwid`
(lub inaczej, w zależności od używanego menadżera pakietów).

UWAGA: Funkcja kasowania jest domyślnie nieaktywna, uruchamia
się ją opcją '-r', '--removing'

W tej wersji nie są jeszcze zaimplementowane funkcje
zmiany nazwy pliku oraz tworzenia folderu
    """

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-r', '--removing', help="aktywuje kasowanie plików",
        action='store_true')
    args = parser.parse_args()


    import urwid
    import widgets_old

    if args.removing:
        pm = Pymmander(removing=True)
    else:
        pm = Pymmander()
    loop = urwid.MainLoop(pm.top, palette)
    loop.run()

