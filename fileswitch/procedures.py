from pathlib import Path
from typing import Protocol


class Procedure(Protocol):
    """A Procedure is an action which should be applied on an file object."""

    def process(self):
        """Definition of procedure(s) to apply if file matches criteria"""

    def description(self) -> str:
        """Provides a short description of it's processing method"""

    def __repr__(self) -> str:
        return f"<PROCEDURE: {self.__class__.__name__}>: {self.description()}"


class LogPrinter(Procedure):
    format_str: str

    def __init__(self, format_str: str) -> None:
        self.format_str = format_str

    def process(self, file: Path):
        print(self.format_str.format(file))

    def description(self):
        return "Prints the file name"
