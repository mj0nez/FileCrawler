from __future__ import annotations
from dataclasses import dataclass

from pathlib import Path
from typing import Callable, Union
from fs.base import FS
from functools import partial


@dataclass
class Station:
    """A file source or destination."""

    name: str
    path: str
    file_system: FS

    def __eq__(self, other: Station) -> bool:
        return self.path == other.path

    def create_substation(self, sub_path: str) -> Station:

        sub_fs = self.file_system.opendir(path=sub_path)
        # return Station(opener=sub_fs.)

    # TODO how should we implement a sub station protocol ?!


class LocalStation(Station):
    """On the current system."""


class LocalFileStation(LocalStation):
    """Path on the local file system."""

    dir_path: Path  # may be the full path or a root dir


class RemoteStation(Station):
    """Provided externally."""


class FTPStation(RemoteStation):
    """FTP Server."""

    server: str  # IP or server name
    port: int
    user: str
    password: str
    key_file: Union[str, Path]

    def __init__(
        self,
        sever: str,
        port: int,
        user: str,
        password: str,
        key_file: Union[str, Path],
    ) -> None:
        super().__init__()


class SFTPStation(FTPStation):
    """SFTP Server of partner."""


def create_station(station_type: str):
    pass
