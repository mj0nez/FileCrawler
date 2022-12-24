from fileswitch.switch import SwitchController
from fs.base import FS
from fs.copy import copy_file_if
from fs.move import move_file
from typing import Union, Callable
from pathlib import Path


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
