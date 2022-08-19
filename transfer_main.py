from amenergy.transfer import MatchAny, MySampleFilter, MySecondFilter, BatchFilter

from pathlib import Path

def main():

    file_1 = Path("file_1.txt")
    file_2 = Path("file_2.txt")
    hello_world_file = Path("Hello World.txt")

    files = [file_1, file_2, hello_world_file]

    hello_world_filter = MySampleFilter()
    not_hello_world_filter = MySecondFilter()
    match_any = MatchAny()

    print(hello_world_filter)

    batch_filter = BatchFilter([hello_world_filter, not_hello_world_filter, match_any])

    # execute filter 1 on all files
    for f in files:
        if hello_world_filter.evaluate(f):
            hello_world_filter.process(f)

    # execute a dry run
    for f in files:
        if hello_world_filter.evaluate(f):
            print(f"File '{f}' was matches '{hello_world_filter}'")

    # evaluate a file with a batch filter:
    print(f"for {file_1= } matching filters are {batch_filter.evaluate(file_1)}")

    # for f in files:
    #     print(batch_filter.evaluate(f))


if __name__ == "__main__":
    main()
