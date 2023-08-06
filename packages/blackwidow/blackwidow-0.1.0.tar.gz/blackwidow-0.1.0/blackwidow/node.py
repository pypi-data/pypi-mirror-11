import os
import ast
import itertools

from blackwidow.error import BlackWidowIOError, BlackWidowValueError


class Node(object):
    """
    A node in the python project graph.
    Contains a list of outgoing edges.
    """

    def __init__(self, filename, package_root=None):
        if not package_root:
            raise SpiderValueError("No 'package_root' specified.")
        self.filename = filename
        self.package_root = package_root
        self.module = import_path(filename, os.path.dirname(package_root))
        self.edges = imported_modules(filename, package_root=package_root)
        self.imports = list(itertools.chain(*[edge.imports for edge in self.edges]))


class Import(object):
    """
    Standardizes ast.Import and ast.ImportFrom objects into a common format
    """

    def __init__(self, obj, filename, package_root):
        self.raw = obj
        self.imports = []

        if hasattr(obj, 'module') and obj.module != None:
            self.module = obj.module
        elif hasattr(obj, 'level'):
            self.module = import_path(filename, package_root, level=obj.level)
        else:
            self.module = None

        for alias in obj.names:
            self.imports.append(self._absolute_import(alias))

    def _absolute_import(self, alias):
        if not self.module:
            return alias.name
        return '.'.join([self.module, alias.name])


def import_path(filename, package_root, level=None):
    """
    Given a filename within a package, return the import path of the filename
    """
    relative_path = os.path.relpath(filename, package_root)
    path = os.path.splitext(relative_path)[0]
    dirs = path.split(os.path.sep)
    if level != None:
        dirs = dirs[:-level]
    return ".".join(dirs)


def imported_modules(filename, package_root):
    """
    Given a filename, returns a list of modules imported by the file
    """
    try:
        fd = open(filename, 'rt')
        tree = ast.parse(fd.read(), filename=filename)
        fd.close()
    except IOError as e:
        raise SpiderIOError(e)

    imports = []
    for item in tree.body:
        if isinstance(item, (ast.Import, ast.ImportFrom)):
            imports.append(
                Import(item, filename=filename, package_root=package_root)
            )
    return imports
