from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


class Procedure(Protocol):
    """A Procedure is an action which should be applied on an file object."""

    def process(self):
        ...

    def description(self) -> str:
        ...


class AbstractProcedure(metaclass=ABCMeta):
    """A Procedure is an action which should be applied on an file object."""

    @abstractmethod
    def process(self):
        """Definition of procedure(s) to apply if file matches criteria"""

    @abstractmethod
    def description(self) -> str:
        """Provides a short description of it's processing method"""

    def __repr__(self: Procedure) -> str:
        return f"<PROCEDURE: {self.__class__.__name__}>: {self.description()}"


@dataclass
class LogPrinter(AbstractProcedure):
    format_str: str

    def process(self, file: Path):
        print(self.format_str.format(file))

    def description(self):
        return "Prints the file name"
