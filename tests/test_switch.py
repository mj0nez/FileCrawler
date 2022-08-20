from fileswitch.filters import (
    HelloWorldFilter,
    MatchAny,
    NotHelloWorldFilter,
)
from fileswitch.providers import ActionProvider, get_print_action

from fileswitch.switch import SingleRouteController, Switch, SwitchController

from pathlib import Path
import pytest


@pytest.fixture
def files():
    file_1 = Path("file_1.txt")
    file_2 = Path("file_2.txt")
    hello_world_file = Path("Hello World.txt")
    return [file_1, file_2, hello_world_file]


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


@pytest.mark.usefixtures("files")
def test_switch_controller(files):

    switch = Switch(filter=HelloWorldFilter(), action=get_print_action())

    controller = SwitchController()
    controller.register_switch(switch)

    # check controller evals switch correctly
    matching_switches = controller.check_switches(files[-1])
    assert matching_switches and len(matching_switches) == 1

    # add another switch to the controller and check again
    controller.register_switch(Switch(filter=MatchAny(), action=get_print_action()))
    matching_switches = controller.check_switches(files[-1])
    assert matching_switches and len(matching_switches) == 2

    # for procedure in controller.get_procedures(hello_world_file):
    #     procedure.action(hello_world_file)


def main():

    single_controller = SingleRouteController()


if __name__ == "__main__":
    main()
