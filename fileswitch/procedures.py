from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Procedure:
    """A Procedure is an action which should be applied on an file object."""

    action: Callable
    description: str

    def __repr__(self) -> str:
        return f"<PROCEDURE: {self.__class__.__name__}>: {self.description}"
