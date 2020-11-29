#!/usr/bin/env python

import os
import shutil
import sys
import getpass
from pathlib import Path


class Pymmander():
    """File manager"""

    def __init__(self):
        self.root = Path.root
        self.home = Path.home()
        self.currentdir = Path(Path.home(), "test", "src", "aa")
        self.showHidden = False

    def list_current_dir(self):
        listdir = os.listdir(self.currentdir)
        if self.showHidden:
            return listdir
        return list(filter(lambda name: name[0] != '.', listdir))

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
            print("Taki sam plik już istnieje")     #TODO: ma się wypisać w gdzieś w TUI

    def _copydir(self, src, dest):
        src, dest = self.pathify(src, dest)
        if not src.is_dir():
            raise AttributeError("{} nie jest folderem".format(src.name))

        try:
            shutil.copytree(src, dest)
        except FileExistsError:
            print("Taki sam folder już istnieje") #TODO: wypisać w TUI

    def move(self, src, dest):
        src, dest = self.pathify(src, dest)

        if dest.is_file:
            print("{} już istnieje, nadpisać?".format(dest.name))   #TODO: Wybranie opcji

        src = str(src)
        dest = str(dest)
        shutil.move(src, dest)

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

    def disk_usage(self):
        return shutil.disk_usage(self.currentdir)


if __name__ == "__main__":

    pm = Pymmander()
    print(pm.currentdir.name)
    pm.remove("trelelraler")

