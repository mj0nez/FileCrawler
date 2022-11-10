import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional, Protocol


class Filter(Protocol):
    """A Filter implements conditional logic that precedes an action."""

    def evaluate(self, file) -> bool:
        """A Filter implements conditional logic that precedes an action ."""

    def description(self) -> str:
        """Provides a short description of it's evaluation method"""

    def __repr__(self) -> str:
        return f"<FILTER {self.__class__.__name__} >: {self.description()}"


@dataclass(frozen=True)
class ModularFilter(Filter):
    """A Filter which can be parameterized."""

    name: str
    evaluate: Callable[[Any], bool]
    description_: str = ""

    def description(self) -> str:
        return self.description_

    def __repr__(self) -> str:
        description = ": " + self.description_ if self.description_ else ""
        return f"<FILTER {self.name} >{description}"


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


@dataclass(frozen=True)
class FileExtensionFilter(Filter):
    extension: str

    def evaluate(self, file: Path) -> bool:
        return file.suffix == self.extension

    def description(self) -> str:
        return f"Filters all .{self.extension} files."


class AbstractRegexFilter:
    """Filters files with a given regular expressions."""

    def __init__(self, pattern, description) -> None:
        self.__pattern = re.compile(pattern)  # precompile for efficient reuse
        self.__description = f"{description}, Pattern: {pattern}"

    def evaluate(self, file_or_content: str) -> bool:
        if self.__pattern.search(file_or_content):
            return True
        return False

    def description(self) -> str:
        return self.__description


class RegexFileNameFilter(AbstractRegexFilter, Filter):
    def evaluate(self, file: Path) -> bool:
        return super().evaluate(file.stem)


class ContentFilter(Filter):
    """A ContentFilter evaluates a file on a deeper level than it's filename or meta data."""

class RegexContentFilter(AbstractRegexFilter, ContentFilter):
    def evaluate(self, file: str) -> bool:
        return super().evaluate(file)


@dataclass(frozen=True)
class SimpleTxtFileFilter(ContentFilter):
    """Filters a txt file based on it's content"""

    evaluate: Callable
    description: Callable

    def load(self, file, encoding="UTF-8") -> str:

        with open(file, mode="r", encoding=encoding) as f:
            content = f.read()
        return content


@dataclass(frozen=True)
class MultiStageFilter(Filter):
    """Some Filter may combine different logic: e.g. analyzing file name and it's content.

    This is useful, when the logic should be split in different blocks or is
    to complex for one function. In most cases a single filter stage should be
    enough.
    """

    how: Callable[[list], bool]  # any / all
    filters: list[Filter]

    def evaluate(self, file) -> bool:

        # evaluate all filters and return overall assessment
        evaluations = []

        for filter_stage in self.filters:
            # If any was chosen, we could break after the first True value,
            # but then we would have to check an additional conditional every
            # loop iteration. Utilizing the built-ins should be more performant.
            evaluations.append(filter_stage.evaluate(file))

        return self.how(evaluations)


# TODO add FilterFactory
