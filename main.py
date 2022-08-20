from filter.filters import (
    ContentFilter,
    MatchAny,
    HelloWorldFilter,
    NotHelloWorldFilter,
    FilterBatch,
)
from filter.procedures import LogPrinter
from pathlib import Path


def main():

    file_1 = Path("file_1.txt")
    file_2 = Path("file_2.txt")
    hello_world_file = Path("Hello World.txt")

    files = [file_1, file_2, hello_world_file]

    hello_world_filter = HelloWorldFilter()
    not_hello_world_filter = NotHelloWorldFilter()
    match_any = MatchAny()

    print(hello_world_filter)

    batch_filter = FilterBatch([hello_world_filter, not_hello_world_filter, match_any])

    # check filter 1 on all files
    for f in files:
        print(f"'{f}' : matches Hello World:\t{hello_world_filter.evaluate(f)}")
    # print("\n")

    # execute a dry run
    for f in files:
        if hello_world_filter.evaluate(f):
            print(f"File '{f}' was matches '{hello_world_filter}'")

    # evaluate a file with a batch filter:
    print(f"for {file_1= } matching filters are {batch_filter.evaluate(file_1)}")

    # for f in files:
    #     print(batch_filter.evaluate(f))

    from filter.filters import SimpleTxtScanner

    scanner = SimpleTxtScanner()
    print(isinstance(scanner, ContentFilter))


if __name__ == "__main__":
    main()
