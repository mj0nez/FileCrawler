from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Protocol, Union

from edipy import EDIenergy


class Filter(Protocol):
    """A Filter implements conditional logic that precedes an action or procedure."""

    def evaluate(self, file) -> bool:
        ...

    def description(self) -> str:
        ...


class AbstractFilter(metaclass=ABCMeta):
    """A Filter implements conditional logic that precedes an action or procedure."""

    @abstractmethod
    def evaluate(self, file) -> bool:
        """Evaluate a file object, check if e.g. filename or it's contents matches criteria."""

    @abstractmethod
    def description(self) -> str:
        """Provides a short description of it's evaluation method"""

    def __repr__(self: Filter) -> str:
        return f"<FILTER {self.__class__.__name__} >: {self.description()}"


class HelloWorldFilter(AbstractFilter):
    def evaluate(self, file: Path) -> bool:
        return "Hello World" in file.stem

    def description(self):
        return "Checks if filename contains 'Hello World'"


class NotHelloWorldFilter(AbstractFilter):
    def evaluate(self, file: Path) -> bool:
        return "Hello World" not in file.stem

    def description(self):
        return "Checks if 'Hello World' is not in filename "


class MatchAny(AbstractFilter):
    def evaluate(self, *args) -> bool:
        return True

    def description(self):
        return "Matches any file"


@dataclass(frozen=True)
class RegexFilter(AbstractFilter):
    _pattern: re.Pattern
    _description: str

    def __init__(self, pattern, description) -> None:
        self._pattern = re.compile(pattern)  # precompile for efficient reuse
        self._description = f"{description}, Pattern: {pattern}"

    def evaluate(self, file) -> bool:
        return self._pattern.match(file)

    def description(self) -> str:
        return self._description


class ContentFilter(AbstractFilter):
    """A ContentFilter evaluates a file on a deeper level than it's filename or meta data."""

    @abstractmethod
    def load(self, file) -> Any:
        """To evaluate a file we first must load it's content."""


class SimpleTxtFileFilter(ContentFilter):
    def load(self, file) -> str:
        with open(file, mode="r") as f:
            content = f.read()

        return content

    def evaluate(self, file) -> bool:
        return "Hello World" in self.load(file)

    def description(self) -> str:
        pass


class EdiFileFilter(ContentFilter):
    def load(self, file) -> str:
        pass


@dataclass
class FilterBatch:
    """A list of filters which should be applied as batch. Usually a batch of filters is used per upstream source."""

    filters: list[Filter]

    def evaluate(self, file: Path) -> list[Filter]:
        """Returns a list of filters, which the given file matches."""
        return [filter for filter in self.filters if filter.evaluate(file)]

    def evaluate_and_process(self, file):
        for filter in self.evaluate(file):
            filter.process(file)
