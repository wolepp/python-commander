#!/usr/bin/env

import os
import shutil
import getpass
from pathlib import Path

from typing import Sequence

class FileManager():
    """File manager"""

    def __init__(self):
        pass

    def ls(self, path: Path) -> Sequence[Path]:
        return [path.joinpath(p) for p in os.listdir(path)]

    def _get_copying_path(self, path: Path, copy_counter: int) -> Path:
        if copy_counter == 0:
            new_name = path.name + "_kopia(1)"
        else:
            new_name = path.name[0 : path.name.rfind("(")] + f"({copy_counter+1})"
        return path.parent.joinpath(new_name)

    def copy(self, src: Path, dest: Path, copy_counter=0) -> None:
        if src.is_dir():
            self.copydir(src, dest)
            return
        if not dest.exists():
            shutil.copy(src, dest)
        else:
            copy_dest_path = self._get_copying_path(dest, copy_counter)
            self.copy(src, copy_dest_path, copy_counter+1)

    def copydir(self, src: Path, dest: Path, copy_counter=0) -> None:
        if not dest.exists():
            shutil.copytree(src, dest)
        else:
            copy_dest_path = self._get_copying_path(dest, copy_counter)
            self.copydir(src, copy_dest_path, copy_counter+1)

    def move(self, src: Path, dest: Path, copy_counter=0) -> None:
        if dest.exists() and dest.samefile(src):
            return
        if not dest.exists():
            shutil.move(str(src), str(dest))
        else:
            move_dest_path = self._get_copying_path(dest, copy_counter=0)
            self.move(src, move_dest_path, copy_counter+1)

    def mkdir(self, path: Path, name: str) -> None:
        if path.joinpath(name).exists():
            raise FileExistsError("Plik docelowy już istnieje")
        path.joinpath(name).mkdir(parents=True)

    def rm(self, path: Path) -> None:
        if not path.exists():
            return
        if path.is_dir():
            self.rmdir(path)
        else:
            os.remove(path)

    def rmdir(self, path: Path) -> None:
        shutil.rmtree(path)

    def rename(self, src: Path, name: str) -> None:
        dest = src.parent.joinpath(name)
        if dest.exists() and not dest.samefile(src):
            raise FileExistsError(f"{dest} już istnieje")
        src.rename(src.parent.joinpath(name))

if __name__ == "__main__":
    fm = FileManager()
    p = Path.home().joinpath("test")
    fm.rename(p.joinpath("4_r"), "4_r")

