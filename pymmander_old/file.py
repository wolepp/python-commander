from os import path


class File():
    """Represents file"""

    def __init__(self, name, parent, isdir=False, children=None):
        self.name = name
        self.parent = parent
        self.isdir = isdir

        if children is None:
            self.children = []
        else:
            self.children = children

        self.absolutepath = path.join(parent.absolutepath, name)

    def addchild(self, child):
        """child can be a File or a sequence of Files"""

        if isinstance(child, (list, tuple)):
            self.children.extend(child)
        else:
            self.children.append(child)
