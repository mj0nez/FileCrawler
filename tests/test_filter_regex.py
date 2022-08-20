from filter.filters import (
    ContentFilter,
)
from filter.filters import SimpleTxtFileFilter, RegexFilter


def main():

    regex = RegexFilter(r"(?<=abc)def", "Matches any characters between a-z or A-Z.")

    print(regex)
    print(regex.evaluate("abcdef"), regex.description())

    scanner = SimpleTxtFileFilter(lambda: True, lambda: "Sample description")
    print(isinstance(scanner, ContentFilter), scanner.evaluate(), scanner.description())


if __name__ == "__main__":
    main()
