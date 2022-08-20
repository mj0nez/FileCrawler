from fileswitch.filters import RegexFilter


def main():

    regex = RegexFilter(r"(?<=abc)def", "Matches any characters between a-z or A-Z.")

    print(regex)
    print(regex.evaluate("abcdef"), regex.description())


if __name__ == "__main__":
    main()
