from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Procedure:
    """A Procedure is an action which should be applied on an file object."""

    action: Callable
    description: str

    def __repr__(self) -> str:
        return f"<PROCEDURE: {self.__class__.__name__}>: {self.description}"


def get_print_procedure() -> Procedure:
    return Procedure(
        lambda x: print(f"File {x} matches filter!"), "Prints the file name."
    )
