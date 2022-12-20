from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional, Union

from .filters import Filter
from .routes import Route
from .errors import MultiSwitchException


@dataclass(frozen=True)
class Switch:
    """Switches set the route for files, if they match the filters criteria."""

    filter: Filter
    route: Union[Callable, Route]

    def evaluate(self, file) -> bool:
        """Check if file matches filter"""
        return self.filter.evaluate(file)

    def __repr__(self) -> str:
        return f"<SWITCH>: {self.filter} || {self.route}"

    def needs_content(self) -> bool:
        """Indicating if the filter requires the content of the file."""
        return self.filter.needs_content()


@dataclass
class SwitchController:
    """A controller oversees the switching per file source.

    A SwitchController operates like any departure controller, all incoming
    files are evaluated based on the registered Switches and provided by their
    corresponding routes or None.
    """

    _switches: list[Switch] = field(default_factory=list)
    _needs_content: bool = False

    def check_switches(self, file: Path) -> tuple[Switch]:
        """Returns a collection of switches, whose filter match the given file."""
        return tuple(switch for switch in self.switches if switch.evaluate(file))

    def get_routes(self, file: Path) -> tuple[Route]:
        """Returns a collection of routes, by evaluating the registered switches."""
        return tuple(switch.route for switch in self.check_switches(file))

    def register_switch(self, switch: Switch) -> None:
        """Adds a switch to the controller."""
        # TODO add a verification, that switches are unique
        self._switches.append(switch)

        # Some filters evaluate on the content level and therefore require
        # preloaded files. To allow the handler to preload the file or just
        # use the files name/meta information we set this property.
        self._needs_content = self._needs_content or switch.needs_content()

    def register_switches(self, switches: list[Switch]) -> None:
        """Adds a list of switches to the controller."""
        for switch in switches:
            self.register_switch(switch)

    def needs_content(self) -> bool:
        """Indicates if the used filters require the preloaded content."""
        return self._needs_content  # a func, to provide a consistent interface


class SingleSwitchController(SwitchController):
    """Allows only one Switch per file.

    Usually, only one Switch should be triggered by a file, but some Filters
    may be too greedy. To avoid unexpected behavior the
    SingeSwitchController raises an exception if multiple Switches were triggered.

    """

    def check_switches(self, file: Path) -> Switch:
        """Gets matching switches from registered list of Switches.

        Parameters
        ----------
        file : Path
            to evaluate

        Returns
        -------
        Switch
            triggered by the evaluated file

        Raises
        ------
        MultiSwitchException
            if more than one Switch was triggered
        """
        route = tuple(switch for switch in self._switches if switch.evaluate(file))

        if len(route) > 1:
            raise MultiSwitchException(
                f"Multiple Filters {[r.filter for r in route]} match the given file {file}! "
            )

        return route[0]

    def get_routes(self, file: Path) -> Optional[Route]:

        route = self.check_switches(file)

        if not route:
            return None

        return route.route
