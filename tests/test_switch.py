from fileswitch.filters import (
    HelloWorldFilter,
    MatchAny,
    NotHelloWorldFilter,
)
from fileswitch.errors import MultiSwitchException
from fileswitch.providers import ActionProvider, get_print_action
from fileswitch.switch import SingleSwitchController, Switch, SwitchController

from pathlib import Path
import pytest


@pytest.fixture
def files():
    file_1 = Path("file_1.txt")
    file_2 = Path("file_2.txt")
    hello_world_file = Path("Hello World.txt")
    return [file_1, file_2, hello_world_file]


@pytest.fixture
def hello_world_file():
    return Path("Hello World.txt")


@pytest.mark.usefixtures("files")
def test_switch_pass(files):
    switch = Switch(filter=MatchAny(), action=get_print_action())
    assert switch
    for f in files:
        assert switch.evaluate(f)


@pytest.mark.usefixtures("files")
def test_switch(files):
    switch = Switch(filter=HelloWorldFilter(), action=get_print_action())
    assert switch
    for f, truth in zip(files, [False, False, True]):
        assert switch.evaluate(f) == truth


@pytest.mark.usefixtures("hello_world_file")
def test_switch_controller(hello_world_file):

    switch = Switch(filter=HelloWorldFilter(), action=get_print_action())

    controller = SwitchController()
    controller.register_switch(switch)

    # check controller evals switch correctly
    matching_switches = controller.check_switches(hello_world_file)
    assert matching_switches and len(matching_switches) == 1

    # add another switch to the controller and check again
    controller.register_switch(Switch(filter=MatchAny(), action=get_print_action()))
    matching_switches = controller.check_switches(hello_world_file)
    assert matching_switches and len(matching_switches) == 2


@pytest.mark.usefixtures("hello_world_file")
def test_switch_controller_w_action_provider(hello_world_file):
    hello_switch = Switch(
        filter=HelloWorldFilter(), action=ActionProvider(lambda: "Hello", "Say's Hello")
    )

    controller = SwitchController()
    controller.register_switch(hello_switch)
    assert controller.get_actions(hello_world_file)[0].action() == "Hello"


@pytest.mark.usefixtures("files")
def test_switch_controller_routing(files):

    hello_switch = Switch(filter=HelloWorldFilter(), action=lambda: "Hello")
    not_hello_switch = Switch(filter=NotHelloWorldFilter(), action=lambda: "Not Hello")

    controller = SwitchController()
    controller.register_switches([hello_switch, not_hello_switch])

    for f, t in zip(files, ["Not Hello", "Not Hello", "Hello"]):
        assert controller.get_actions(f)[0]() == t


@pytest.mark.usefixtures("hello_world_file")
def test_single_route_controller(hello_world_file):

    hello_switch = Switch(filter=HelloWorldFilter(), action=lambda: "Hello")
    match_any = Switch(filter=MatchAny(), action=lambda: "Any")

    controller = SingleSwitchController()

    # file should trigger switch
    controller.register_switch(hello_switch)
    assert controller.check_switches(hello_world_file)

    # ensure single match
    controller.register_switch(match_any)
    with pytest.raises(MultiSwitchException):
        controller.check_switches(hello_world_file)
