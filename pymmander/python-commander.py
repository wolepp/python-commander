#!/usr/bin/env python

import os 
import shutil
import sys

from cache import Cache
from file import File

class Pymmander():
    """File manager"""

    def __init__(self):
        root = File("/", parent=None, isDir=True)
        self.cache = Cache(root)

        self.scanroot()
        self.scanhome()

    def scanroot(self):
        listdir = os.listdir(self.cache.root.name)


    def scanhome(self):
        pass



if __name__ == "__main__":
    pass


    