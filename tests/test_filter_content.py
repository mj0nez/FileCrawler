from fileswitch.filters import (
    ContentFilter,
    SimpleTxtFileFilter,
)


def main():

    scanner = SimpleTxtFileFilter(lambda: True, lambda: "Sample description")
    print(isinstance(scanner, ContentFilter), scanner.evaluate(), scanner.description())


if __name__ == "__main__":
    main()
