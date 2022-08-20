from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ActionProvider:
    """Provides an action which follows an conditional evaluation, implemented by a switch."""

    action: Callable
    description: str

    def __repr__(self) -> str:
        return f"<ACTION>: {self.__class__.__name__}>: {self.description}"


def get_print_action() -> ActionProvider:
    return ActionProvider(
        lambda x: print(f"File {x} matches filter!"), "Prints the file name."
    )
