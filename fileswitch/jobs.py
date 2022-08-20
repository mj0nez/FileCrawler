from dataclasses import dataclass
from typing import Protocol, Union
from pathlib import Path

from .filters import Filter
from .procedures import Procedure


class Job(Filter, Procedure):
    def __repr__(self: Filter) -> str:
        criteria, procedure = self.description()
        return f"<FILTERJOB: {self.__class__.__name__}> evaluation: {criteria}, procedure: {procedure})"





# class TransferJob(Protocol):
#     def transfer(self):
#         """"""
#         ...


file_path_obj = Union[str, Path]


@dataclass
class FilterStream:
    stream: Union[file_path_obj, list[file_path_obj]]
