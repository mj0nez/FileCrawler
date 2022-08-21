from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Route:
    """A route is a path which a file should follow and may be just a function or complex process."""

    action: Callable
    description: str

    def __repr__(self) -> str:
        return f"<ROUTE>: {self.__class__.__name__}>: {self.description}"


def get_console_route() -> Route:
    return Route(lambda x: print(f"File {x} matches filter!"), "Prints the file name.")
