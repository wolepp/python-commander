from file import File
import os
import sys
import shutil
import getpass


class Cache():
    """Cache for storing files structure"""

    def __init__(self, root_ref):
        self.root = root_ref

        self.scanroot()
        self.scanhome()
        self.currentdir = self.root

    def scanroot(self):
        self.scandir(self.root)

    def scanhome(self):
        username = getpass.getuser()

    def add(self, name, parent=None):
        if parent is None:
            parent = self.currentdir

        isdir = os.path.isdir(os.path.join(self.currentdir.absolutepath, name))
        self.currentdir.addchild(File(name, parent=parent, isdir=isdir))

    def scandir(self, dir_: File):
        listdir = os.listdir(dir_.absolutepath)
        dir_.addchild(listdir)
