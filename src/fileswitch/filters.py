import gzip
import re
import zipfile
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from io import BytesIO, IOBase, StringIO, TextIOBase
from pathlib import Path
from typing import Any, Callable, Optional, Protocol, Union
from uuid import UUID, uuid4

from .utils import Payload


class Filter(Protocol):
    """A Filter implements conditional logic that precedes an action."""

    _uuid: UUID
    _needs_content: bool

    def __init__(self) -> None:
        self._uuid = uuid4()
        self._needs_content = False

    def evaluate(self, file: Union[Path, Payload]) -> bool:
        """A Filter implements conditional logic that precedes an action ."""

    def description(self) -> str:
        """Provides a short description of it's evaluation method"""

    def needs_content(self) -> bool:
        """Indicates if the file content has to be provided before evaluation."""
        return self._needs_content

    def __repr__(self) -> str:
        return f"<FILTER {self.__class__.__name__} >: {self.description()}"


class ModularFilter(Filter):
    """A Filter which can be parameterized."""

    name: str
    evaluate: Callable[[Any], bool]
    description_: str

    def __init__(
        self,
        name: str,
        evaluate: Callable[[Any], bool],
        description: str = "",
        needs_content: bool = False,
    ) -> None:
        self.name = name
        self.evaluate = evaluate
        self.description_ = description
        self._needs_content = needs_content

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

    _needs_content: bool = True


class RegexContentFilter(AbstractRegexFilter, ContentFilter):
    def evaluate(self, file: str) -> bool:
        return super().evaluate(file)


@dataclass(frozen=True)
class SimpleTxtFileFilter(ContentFilter):
    """Filters a txt file based on it's content"""

    evaluate: Callable
    description: Callable


class MultiStageType(str, Enum):
    ANY = "any"
    SEQUENTIAL = "sequential"


class MultiStageFilter(Filter):
    """Some Filter may combine different logic: e.g. analyzing file name and it's content.

    This is useful, when the logic should be split in different blocks or is
    to complex for one function. In most cases a single filter stage should be
    enough.
    """

    how: MultiStageType  # any, all, sequential
    _filters: list[Filter]

    def __init__(self, how: MultiStageType, filters: list[Filter]) -> None:
        self.how = MultiStageFilter
        self._filters = filters

        if how == MultiStageType.ANY:
            self.evaluate = self._evaluate_any
        elif how == MultiStageType.SEQUENTIAL:
            self.evaluate = self._evaluate_sequential
        else:
            raise ValueError

    def check_stages(self, file: Path) -> tuple[Filter]:
        """Returns a collection of filters, which match the given file."""
        return tuple(
            filter for filter in self._filters if filter.evaluate(file)
        )

    def evaluate(self, file) -> bool:
        # The method will be monkey patched on Filter creation.
        pass

    def _evaluate_sequential(self, file) -> bool:

        for filter_stage in self._filters:

            # All filters will be evaluated one after the other.
            # If one filter does not match, we shortcut the evaluation.
            # This allows some kind of pre filtering, e.g.
            # we just want specific .txt files but the providing source also contains .mp3 files.
            # So, instead trying to analyze the mp3-content we shortcut the evaluation.
            if not filter_stage.evaluate(file):
                return False

        # Otherwise we can return a positive result.
        return True

    def _evaluate_any(self, file) -> bool:

        for filter_stage in self._filters:

            # All filters will be evaluated one after the other.
            # If one filter matches, we shortcut the evaluation.
            if filter_stage.evaluate(file):
                return True

        # If no filters matches, the result is negative.
        return False

    def needs_content(self) -> bool:
        return any(f.needs_content() for f in self._filters)


# TODO add FilterFactory
