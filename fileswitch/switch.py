from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional, Union

from .filters import Filter
from .providers import ActionProvider
from .errors import MultiRouteException


@dataclass(frozen=True)
class Switch:
    """A Switch is a decision point, where a file may be filtered and given to an action."""

    filter: Filter
    action: Union[Callable, ActionProvider]

    def evaluate(self, file) -> bool:
        """Check if file matches filter"""
        return self.filter.evaluate(file)

    def __repr__(self) -> str:
        return f"<SWITCH>: {self.filter} || {self.action}"


@dataclass
class SwitchController:
    """A controller oversees the switching per file source.

    A SwitchController operates like any departure controller, all incoming
    files are evaluated based on the registered Switches and send on their way,
    by providing the respective action.
    """

    switches: list[Switch] = field(default_factory=list)

    def check_switches(self, file: Path) -> tuple[Switch]:
        """Returns a collection of switches, whose filter match the given file."""
        return tuple(switch for switch in self.switches if switch.evaluate(file))

    def get_actions(self, file: Path) -> tuple[ActionProvider]:
        """Returns a collection of actions, whose filter match the given file."""
        return tuple(switch.action for switch in self.check_switches(file))

    def register_switch(self, switch: Switch) -> None:
        """Adds a switch to the controller."""
        # TODO add a verification, that switches are unique
        self.switches.append(switch)

    def register_switches(self, switches: list[Switch]) -> None:
        """Adds a list of switches to the controller."""
        self.switches.extend(switches)


class SingleRouteController(SwitchController):
    def check_switches(self, file: Path) -> tuple[Switch]:
        """Returns a collection of switches, whose filter match the given file."""
        route = tuple(switch for switch in self.switches if switch.evaluate(file))

        if len(route) > 1:
            raise MultiRouteException(
                f"Multiple Filters {[r.filter for r in route]} match the given file {file}! "
            )

        return route

    def get_actions(self, file: Path) -> Optional[ActionProvider]:

        route = self.check_switches(file)

        if not route:
            return None

        return route[0].action
