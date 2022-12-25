from fileswitch.switch import SwitchController
from typing import Union, Callable
from pathlib import Path
from enum import Enum

from fs.base import FS
from fs.copy import copy_file_if, _copy_is_necessary
from fs.move import move_file
from fs._pathcompat import commonpath
from fs.copy import copy_dir, copy_file
from fs.errors import FSError
from fs.opener import manage_fs
from fs.osfs import OSFS
from fs.path import frombase


class Operator:
    # fetches the files & their content, talks to a SwitchController which informs if he needs the file content
    # and then executes the transfer protocol / the method ...
    # _stations<
    controller: SwitchController
    # def register_station(self, station):
    #     self.

    # TODO this method should not be part of the filter class.
    # Data Source should implement this and the overall process should provide it to the filter.
    def load(self, file, encoding="UTF-8") -> str:

        with open(file, mode="r", encoding=encoding) as f:
            content = f.read()
        return content


# COPY_FILE_IF_EXISTS_DEFAULT = "not_exists"
COPY_FILE_IF_EXISTS_DEFAULT = "always"


class TransferCondition(str, Enum):
    always = "always"
    newer = "newer"
    older = "older"
    exists = "exists"
    not_exists = "not_exists"

    @classmethod
    def get_all(cls) -> dict:
        """Returns a dict of all implemented conditions."""
        return {k: v for k, v in cls.__members__.items()}


def do_transfer_if(
    condition: str,
    src_fs: FS,
    src_path: str,
    dst_fs: FS,
    dst_path: str,
):

    return _copy_is_necessary(
        src_fs=src_fs,
        src_path=src_path,
        dst_fs=dst_fs,
        dst_path=dst_path,
        condition=condition,
    )


# This should
def copy_file_to_dst(
    src_fs: Union[FS, str],
    dst_fs: Union[FS, str],
    file_name: str,
    file_name_modifier: Callable[[Path], str] = None,
    condition: Union[FS, str] = None,
    preserve_time: bool = True,
):
    condition = condition or COPY_FILE_IF_EXISTS_DEFAULT

    if file_name_modifier:
        file_name_dst = file_name_modifier(file_name)
    else:
        file_name_dst = file_name

    return copy_file_if(
        src_fs=src_fs,
        src_path=file_name,
        dst_fs=dst_fs,
        dst_path=file_name_dst,
        condition=condition,
        preserve_time=preserve_time,
    )


def move_file(
    src_fs: FS,
    src_path: Path,
    dst_fs: FS,
    dst_path: Path,
    preserve_time: bool = False,
    cleanup_dst_on_error: bool = True,
):
    """Move a file from one filesystem to another.

    Parameters
    ----------
    src_fs : FS
        Source filesystem (instance or URL).
    src_path : Path
        Path to a file on ``src_fs``.
    dst_fs : FS
        Destination filesystem (instance or URL).
    dst_path : Path
        Path to a file on ``dst_fs``.
    preserve_time : bool, optional
        If `True`, try to preserve mtime of the resources, by default False
    cleanup_dst_on_error : bool, optional
        If `True`, tries to delete the file copied to ``dst_fs`` if deleting the file from ``src_fs`` fails, by default True
    """
    with manage_fs(src_fs, writeable=True) as _src_fs:
        with manage_fs(dst_fs, writeable=True, create=True) as _dst_fs:
            _move_internal(
                src_fs=_src_fs,
                src_path=src_path,
                dst_fs=_dst_fs,
                dst_path=dst_path,
                preserve_time=preserve_time,
                cleanup_dst_on_error=cleanup_dst_on_error,
            )


def _move_internal(
    src_fs: FS,
    src_path: Path,
    dst_fs: FS,
    dst_path: Path,
    preserve_time: bool,
    cleanup_dst_on_error: bool,
):

    if src_fs is dst_fs:
        # Same filesystem, may be optimized
        print("Same Filesystem")
        src_fs.move(src_path, dst_path, overwrite=True, preserve_time=preserve_time)
        return

    if src_fs.hassyspath(src_path) and dst_fs.hassyspath(dst_path):
        # if both filesystems have a syspath we create a new OSFS from a
        # common parent folder and use it to move the file.
        print("has common path")
        try:
            src_syspath = src_fs.getsyspath(src_path)
            dst_syspath = dst_fs.getsyspath(dst_path)
            common = commonpath([src_syspath, dst_syspath])
            if common:
                rel_src = frombase(common, src_syspath)
                rel_dst = frombase(common, dst_syspath)
                with src_fs.lock(), dst_fs.lock():
                    with OSFS(common) as base:
                        base.move(rel_src, rel_dst, preserve_time=preserve_time)
                        return  # optimization worked, exit early
        except ValueError:
            # This is raised if we cannot find a common base folder.
            # In this case just fall through to the standard method.
            pass

    # Standard copy and delete
    with src_fs.lock(), dst_fs.lock():
        copy_file(
            src_fs,
            src_path,
            dst_fs,
            dst_path,
            preserve_time=preserve_time,
        )
        try:
            src_fs.remove(src_path)
        except FSError as e:
            # if the source cannot be removed we delete the copy on the
            # destination
            if cleanup_dst_on_error:
                dst_fs.remove(dst_path)
            raise e
