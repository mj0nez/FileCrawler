from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Protocol, Union
from pathlib import Path


class Filter(Protocol):
    """A Filter implements conditional logic that precedes an action or procedure."""

    def evaluate(self, file) -> bool:
        ...

    def description(self) -> tuple[str, str]:
        ...


class Procedure(Protocol):
    """A Procedure is an action which should be applied on an file object."""

    def process(self):
        ...

    def description(self) -> tuple[str, str]:
        ...


class AbstractFilter(metaclass=ABCMeta):
    """A Filter implements conditional logic that precedes an action or procedure."""
    @abstractmethod
    def evaluate(self, file) -> bool:
        """Evaluate a file object, check if e.g. filename or it's contents matches criteria."""

    @abstractmethod
    def description(self) -> tuple[str, str]:
        """Provides a short description of it's evaluation method"""

class AbstractProcedure(metaclass=ABCMeta):
    """A Procedure is an action which should be applied on an file object."""

    @abstractmethod
    def process(self):
        """Definition of procedure(s) to apply if file matches criteria"""

    @abstractmethod
    def description(self) -> tuple[str, str]:
        """Provides a short description of it's processing method"""


class TransferJob(Filter, Procedure):
    def __repr__(self: Filter) -> str:
        criteria, procedure = self.description()
        return f"<FILTER: {self.__class__.__name__}> evaluation: {criteria}, procedure: {procedure})"


@dataclass
class BatchFilter:
    """A list of filters which should be applied as batch. Usually a batch of filters is used per upstream source."""

    filters: list[Filter]

    def evaluate(self, file: Path) -> list[Filter]:
        """Returns a list of filters, which the given file matches."""
        return [filter for filter in self.filters if filter.evaluate(file)]

    def evaluate_and_process(self, file):
        for filter in self.evaluate(file):
            filter.process(file)


# class TransferJob(Protocol):
#     def transfer(self):
#         """"""
#         ...


file_path_obj = Union[str, Path]


@dataclass
class FilterStream:
    stream: Union[file_path_obj, list[file_path_obj]]


class MySampleFilter(TransferJob):
    def evaluate(self, file: Path) -> bool:
        return "Hello World" in file.stem

    def process(self, file: Path):
        print(f"Hello World is in {file= }")

    def description(self):
        return "Checks if filename contains 'Hello World'", "Prints the file name"


class MySecondFilter(TransferJob):
    def evaluate(self, file: Path) -> bool:
        return "Hello World" not in file.stem

    def process(self, file: Path):
        print(f"{file= } is w/o Hello World")

    def description(self):
        return "Checks if 'Hello World' is not in filename ", "Prints the file name"


class MatchAny(TransferJob):
    def evaluate(self, file: Path) -> bool:
        return True

    def process(self, file: Path):
        print(f"{file= } matches the any filter")

    def description(self):
        return "Matches any file", "Prints the file name"
