from pathlib import Path

import gzip
import zipfile
from pathlib import Path
from typing import Union, Any
import py7zr

# currently three types of filter input are considered:
# a path like object -> Path
# a preloaded content as Text or String
#
Payload = Union[
    str, bytes, Any
]  # file payloads which may be evaluated by content filters
CompressedArchive = Union[
    py7zr.SevenZipFile, gzip.GzipFile, zipfile.ZipFile
]  # archives to decompress

class FileCargo:
    """A file to route."""

    path: Path
    payload: Payload
