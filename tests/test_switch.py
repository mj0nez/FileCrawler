from pathlib import Path

import pytest

from fileswitch.errors import MultiSwitchException
from fileswitch.filters import HelloWorldFilter, MatchAny, NotHelloWorldFilter
from fileswitch.routes import Route, get_console_route
from fileswitch.switch import SingleSwitchController, Switch, SwitchController


@pytest.fixture
def files():
    file_1 = Path("file_1.txt")
    file_2 = Path("file_2.txt")
    hello_world_file = Path("Hello World.txt")
    return [file_1, file_2, hello_world_file]


@pytest.fixture
def hello_world_file():
    return Path("Hello World.txt")


class TestSwitch:
    @pytest.mark.usefixtures("files")
    def test_switch_pass(self, files):
        switch = Switch(filter=MatchAny(), route=get_console_route())
        assert switch
        for f in files:
            assert switch.evaluate(f)

    @pytest.mark.usefixtures("files")
    def test_switch(self, files):
        switch = Switch(filter=HelloWorldFilter(), route=get_console_route())
        assert switch
        for f, truth in zip(files, [False, False, True]):
            assert switch.evaluate(f) == truth


class TestSwitchController:
    @pytest.mark.usefixtures("hello_world_file")
    def test_switch_controller(self, hello_world_file):

        switch = Switch(filter=HelloWorldFilter(), route=get_console_route())

        controller = SwitchController()
        controller.register_switch(switch)

        # check controller evals switch correctly
        matching_switches = controller.check_switches(hello_world_file)
        assert matching_switches and len(matching_switches) == 1

        # add another switch to the controller and check again
        controller.register_switch(
            Switch(filter=MatchAny(), route=get_console_route())
        )
        matching_switches = controller.check_switches(hello_world_file)
        assert matching_switches and len(matching_switches) == 2

    @pytest.mark.usefixtures("hello_world_file")
    def test_switch_controller_w_action_provider(self, hello_world_file):
        hello_switch = Switch(
            filter=HelloWorldFilter(),
            route=Route(lambda: "Hello", "Say's Hello"),
        )

        controller = SwitchController()
        controller.register_switch(hello_switch)
        assert controller.get_routes(hello_world_file)[0].action() == "Hello"

    @pytest.mark.usefixtures("files")
    def test_switch_controller_routing(self, files):

        hello_switch = Switch(filter=HelloWorldFilter(), route=lambda: "Hello")
        not_hello_switch = Switch(
            filter=NotHelloWorldFilter(), route=lambda: "Not Hello"
        )

        controller = SwitchController()
        controller.register_switches([hello_switch, not_hello_switch])

        for f, t in zip(files, ["Not Hello", "Not Hello", "Hello"]):
            assert controller.get_routes(f)[0]() == t

    @pytest.mark.usefixtures("hello_world_file")
    def test_single_route_controller(self, hello_world_file):

        hello_switch = Switch(filter=HelloWorldFilter(), route=lambda: "Hello")
        match_any = Switch(filter=MatchAny(), route=lambda: "Sample ")

        controller = SingleSwitchController()

        # file should trigger switch
        controller.register_switch(hello_switch)
        assert controller.check_switches(hello_world_file)

        # ensure single match
        controller.register_switch(match_any)
        with pytest.raises(MultiSwitchException):
            controller.check_switches(hello_world_file)


def test_hash():
    h1, h2 = HelloWorldFilter(), HelloWorldFilter()
    assert h1 == h2
