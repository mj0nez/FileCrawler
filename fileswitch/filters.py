import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Protocol

from edipy import EDIenergy
from edipy.core.parser import SparseParser


class Filter(Protocol):
    """A Filter implements conditional logic that precedes an action or procedure."""

    def evaluate(self, file) -> bool:
        """A Filter implements conditional logic that precedes an action or procedure."""

    def description(self) -> str:
        """Provides a short description of it's evaluation method"""

    def __repr__(self) -> str:
        return f"<FILTER {self.__class__.__name__} >: {self.description()}"


class HelloWorldFilter(Filter):
    """Filters files with Hello world in stem."""

    def evaluate(self, file: Path) -> bool:
        return "Hello World" in file.stem

    def description(self):
        return "Checks if filename contains 'Hello World'"


class NotHelloWorldFilter(Filter):
    """Filters files without Hello world in stem."""

    def evaluate(self, file: Path) -> bool:
        return "Hello World" not in file.stem

    def description(self):
        return "Checks if 'Hello World' is not in filename "


class MatchAny(Filter):
    """Filters any file."""

    def evaluate(self, *args) -> bool:
        return True

    def description(self):
        return "Matches any file"


class RegexFilter(Filter):
    """Filters files names with a given regular expressions."""

    def __init__(self, pattern, description) -> None:
        self.__pattern = re.compile(pattern)  # precompile for efficient reuse
        self.__description = f"{description}, Pattern: {pattern}"

    def evaluate(self, file) -> bool:
        if self.__pattern.search(file):
            return True
        return False

    def description(self) -> str:
        return self.__description


class ContentFilter(Filter):
    """A ContentFilter evaluates a file on a deeper level than it's filename or meta data."""

    def load(self, file) -> Any:
        """To evaluate a file we first must load it's content."""


@dataclass(frozen=True)
class SimpleTxtFileFilter(ContentFilter):
    """Filters a txt file based on it's content"""

    evaluate: Callable
    description: Callable

    def load(self, file, encoding="UTF-8") -> str:

        with open(file, mode="r", encoding=encoding) as f:
            content = f.read()
        return content


class EdiFileFilter(ContentFilter):
    """Filters EDIfact files depending on their content."""

    def load(self, file) -> EDIenergy:
        return EDIenergy.from_file(file, parser_class=SparseParser)


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
