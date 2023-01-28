from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable

from fileswitch.stations import Station


@dataclass(frozen=True)
class Route:
    """A route is a path which a file should follow and may be just a function or complex process."""

    action: Callable
    description: str

    def __repr__(self) -> str:
        return f"<ROUTE>: {self.__class__.__name__}>: {self.description}"


def get_console_route() -> Route:
    return Route(lambda x: print(f"File {x} matches filter!"), "Prints the file name.")


def create_transfer_action_from_stations(
    origin: Station, oirign_subpath, destination: Station, destination_subpath
) -> Callable:
    # connects callable which represents the  transfer protocol from origin to
    # destination:
    #
    # e.g.   ftp -> local fs, local fs -> s3, local -> local fs  ...
    pass


class RouteController:
    routes: dict

    def __init__(self) -> None:
        self.routes = defaultdict(dict)

    def create_route_from_station(
        self,
        origin: Station,
        oirign_subpath,
        destination: Station,
        destination_subpath,
        description: str,
    ) -> Route:

        # check if route exists

        # create route
        transfer_callable = create_transfer_action_from_stations(
            origin=origin,
            oirign_subpath=oirign_subpath,
            destination=destination,
            destination_subpath=destination_subpath,
        )
        route = Route(action=transfer_callable, description=description)

        # We assume a route controller overseas all routes from an origin to
        # all connected destinations. Therefore registering the transfer
        # per destination.
        #
        self.routes[destination].append(transfer_callable)

        return route

    def get_stations(self) -> dict:
        # should return a dict with all routes
        pass

    def get_routes_of_station(self, station: Station) -> list[Route]:
        # return all routes of a given station
        pass
