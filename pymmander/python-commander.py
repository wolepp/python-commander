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


    def open_dir(self, name):
        path = self.pathify(name)
        if not Path.is_dir(path):
            print("{} is not a directory".format(name))
        else:
            self.currentdir = path

    def open_parentdir(self):
        self.currentdir = self.currentdir.parent

    def copy(self, src, dest):
        src, dest = self.pathify(src, dest)
        if src.is_dir():
            self.copydir(src, dest)
            return

        try:
            shutil.copy(src, dest)
        except shutil.SameFileError:
            print("Taki sam plik już istnieje")

    def copydir(self, src, dest):
        try:
            shutil.copytree(src, dest)
        except FileExistsError:
            print("Taki sam folder już istnieje")

    def move(self, src, dest):
        shutil.move(src, dest)

    def mkdir(self, path):
        pass

    def remove(self, path):
        pass

    def rename(self, old, new):
        pass

    def switch_hidden(self):
        self.showHidden = not self.showHidden


if __name__ == "__main__":

    pm = Pymmander()
    listdir = pm.list_current_dir()
    print(listdir)
    pm.copy('ab', 'abcd')
