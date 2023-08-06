import bz2
import gzip
import io
import os
import re
import subprocess

from . import p7z
from ..errors import FileTypeError

EXT_RE = re.compile(r'\.([^\.]+)$')
"""
A regular expression for extracting the final extension of a file.
"""

FILE_OPENERS = {
    'xml': open,
    'gz': gzip.open,
    'bz2': bz2.open,
    '7z': p7z.open
}
"""
Maps extensions to the strategy for opening/decompressing a file
"""

def extract_extension(path):
    """
    Reads a file path and returns the extension or None if the path
    contains no extension.
    """
    filename = os.path.basename(path)
    parts = filename.split(".")
    if len(parts) == 1:
        return None
    else:
        return parts[-1]

def normalize_path(path):
    """
    Verifies that a file exists at a given path and that the file has a
    known extension type.

    :Parameters:
        path : `str` | `file`
            the path to a dump file or a file handle

    """
    path = os.path.expanduser(path)

    # Check if exists and is a file
    if os.path.isdir(path):
        raise IsADirectoryError("Is a directory: {0}".format(path))
    elif not os.path.isfile(path):
        raise FileNotFoundError("No such file or directory: {0}".format(path))

    extension = extract_extension(path)

    if extension not in FILE_OPENERS:
        raise FileTypeError("Extension {0} is not supported."
                            .format(repr(extension)))

    return path, extension


def open(path_or_f):
    """
    Turns a path to a dump file into a file-like object of (decompressed)
    XML data.

    :Parameters:
        path : `str`
            the path to the dump file to read
    """
    if hasattr(path_or_f, "read"):
        return path_or_f
    else:
        path = path_or_f

    path, extension = normalize_path(path)

    open_func = FILE_OPENERS[extension]

    return open_func(path)

class ConcatinatingTextReader(io.TextIOBase):

    def __init__(self, *items):
        self.items = [io.StringIO(i) if isinstance(i, str) else i
                      for i in items]

    def read(self, size=-1):
        return "".join(self._read(size))

    def readline(self):

        if len(self.items) > 0:
            line = self.items[0].readline()
            if line == "": self.items.pop(0)
        else:
            line = ""

        return line

    def _read(self, size):
        if size > 0:
            while len(self.items) > 0:
                byte_vals = self.items[0].read(size)
                yield byte_vals
                if len(byte_vals) < size:
                    size = size - len(byte_vals) # Decrement bytes
                    self.items.pop(0)
                else:
                    break

        else:
            for item in self.items:
                yield item.read()




def concat(*stream_items):
    return ConcatinatingTextReader(*stream_items)
