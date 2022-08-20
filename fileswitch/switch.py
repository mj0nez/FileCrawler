from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .filters import Filter
from .procedures import Procedure
from .errors import MultiRouteException


@dataclass(frozen=True)
class Switch:
    """A Switch is a decision point, where a file may be filtered and given to a procedure."""

    filter: Filter
    procedure: Procedure

    def evaluate(self, file) -> bool:
        """Check if file matches filter"""
        return self.filter.evaluate(file)

    def __repr__(self) -> str:
        return f"<SWITCH>: {self.filter} || {self.procedure}"


@dataclass
class SwitchController:
    """A controller oversees the switching per file source.

    A SwitchController operates like any departure controller, all incoming
    files are evaluated based on the registered Switches and send on their way,
    by providing the respective procedure.
    """

    switches: list[Switch] = field(default_factory=list)

    def check_route(self, file: Path) -> tuple[Switch]:
        """Returns a collection of switches, whose filter match the given file."""
        return tuple(switch for switch in self.switches if switch.evaluate(file))

    def get_route(self, file: Path) -> tuple[Procedure]:
        """Returns a collection of procedures, whose filter match the given file."""
        return tuple(switch.procedure for switch in self.check_route(file))

    def register_switch(self, switch: Switch) -> None:
        """Adds a switch to the controller."""
        # TODO add a verification, that switches are unique
        self.switches.append(switch)

    def register_switches(self, switches: list[Switch]) -> None:
        """Adds a list of switches to the controller."""
        self.switches.extend(switches)


class SingleRouteController(SwitchController):
    def get_route(self, file: Path) -> Optional[Procedure]:

        route = self.check_route(file)

        if not route:
            return None

        if len(route) > 1:
            raise MultiRouteException(
                f"Multiple Filters {[r.filter for r in route]} match the given file {file}! "
            )
        else:
            return route[0].procedure
