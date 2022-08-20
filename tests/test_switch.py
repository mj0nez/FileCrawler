from fileswitch.filters import (
    MatchAny,
    HelloWorldFilter,
    NotHelloWorldFilter,
)
from fileswitch.procedures import LogPrinter, Procedure

from fileswitch.switch import SingleRouteController, Switch, SwitchController

from pathlib import Path


def main():

    file_1 = Path("file_1.txt")
    file_2 = Path("file_2.txt")
    hello_world_file = Path("Hello World.txt")

    files = [file_1, file_2, hello_world_file]

    filter = HelloWorldFilter()

    procedure = Procedure(
        lambda x: print(f"File {x} matches filter!"), "Prints the file name."
    )

    hello_world_switch = Switch(filter=filter, procedure=procedure)

    print(hello_world_switch)
    print(hello_world_switch.evaluate(hello_world_file))

    controller = SwitchController()

    controller.register_switch(hello_world_switch)

    print(controller.check_switches(hello_world_file))

    for procedure in controller.get_procedures(hello_world_file):
        procedure.action(hello_world_file)

    single_controller = SingleRouteController()
    # not_hello_world_filter = NotHelloWorldFilter()
    # match_any = MatchAny()

    # batch_filter = SwitchController(
    #     [hello_world_filter, not_hello_world_filter, match_any]
    # )

    # # check filter 1 on all files
    # for f in files:
    #     print(f"'{f}' : matches Hello World:\t{hello_world_filter.evaluate(f)}")
    # # print("\n")

    # # execute a dry run
    # for f in files:
    #     if hello_world_filter.evaluate(f):
    #         print(f"File '{f}' was matches '{hello_world_filter}'")

    # # evaluate a file with a batch filter:
    # print(f"for {file_1= } matching filters are {batch_filter.evaluate(file_1)}")

    # for f in files:
    #     print(batch_filter.evaluate(f))


if __name__ == "__main__":
    main()
