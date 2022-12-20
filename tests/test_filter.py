from pathlib import Path

import pytest
from fileswitch.filters import (
    ContentFilter,
    FileExtensionFilter,
    HelloWorldFilter,
    MatchAny,
    ModularFilter,
    MultiStageFilter,
    MultiStageType,
    NotHelloWorldFilter,
    RegexFileNameFilter,
    AbstractRegexFilter,
    SimpleTxtFileFilter,
)


@pytest.fixture
def files():
    file_1 = Path("file_1.txt")
    file_2 = Path("file_2.txt")
    hello_world_file = Path("Hello World.txt")
    return [file_1, file_2, hello_world_file]


@pytest.mark.usefixtures("files")
def test_hello_world_filter(files):

    file_1, file_2, hello_world_file = files
    hello_world_filter = HelloWorldFilter()
    assert not hello_world_filter.evaluate(file_1)
    assert not hello_world_filter.evaluate(file_2)
    assert hello_world_filter.evaluate(hello_world_file)


@pytest.mark.usefixtures("files")
def test_not_hello_world_filter(files):

    file_1, file_2, hello_world_file = files
    not_hello_world_filter = NotHelloWorldFilter()
    assert not_hello_world_filter.evaluate(file_1)
    assert not_hello_world_filter.evaluate(file_2)
    assert not not_hello_world_filter.evaluate(hello_world_file)


@pytest.mark.usefixtures("files")
def test_match_any(files):

    match_any = MatchAny()
    for f in files:
        assert match_any.evaluate(f)


def test_regex_filter():

    regex_filter = AbstractRegexFilter(
        r"(?<=abc)def", "Matches any characters between a-z or A-Z."
    )

    assert regex_filter.evaluate("abcdef")
    assert not regex_filter.evaluate("1565464")


def test_content_filter():
    scanner = SimpleTxtFileFilter(lambda: True, lambda: "Sample description")
    assert isinstance(scanner, ContentFilter)
    assert scanner.evaluate()
    assert scanner.description() == "Sample description"


@pytest.fixture
def multi_stage_filters_with_exception():
    return [
        NotHelloWorldFilter(),
        ModularFilter(
            name="", evaluate=raise_an_exception, description="A test filter"
        ),
    ]


class TestMultiStageFilter:
    def test_filter_types(self):

        my_filter = MultiStageFilter(how="any", filters=[])
        assert my_filter._evaluate_any == my_filter.evaluate

        with pytest.raises(ValueError):
            MultiStageFilter(how="wrong_stage_type", filters=[])

    def test_any_filter(self):
    any_filter = MultiStageFilter(
        how="any",
        filters=[NotHelloWorldFilter(), RegexFileNameFilter(r"(?<=abc)def", "")],
    )

        assert not any_filter.evaluate(Path("Hello World"))
    assert any_filter.evaluate(Path("156546565"))

    def test_sequential_filter(self):
        sequential_filter = MultiStageFilter(
            how="sequential",
            filters=[NotHelloWorldFilter(), RegexFileNameFilter(r"(?<=abc)def", "")],
        )
        assert not sequential_filter.evaluate(Path("156546565"))
        assert sequential_filter.evaluate(Path("abcdef"))

    def test_filter_breakout(self):

        # just raise an exception - test the test...
        with pytest.raises(Exception):

            error_filter = ModularFilter(name="", evaluate=raise_an_exception)
            error_filter.evaluate("")

    @pytest.mark.usefixtures("multi_stage_filters_with_exception")
    def test_sequential_filter_evaluation(self, multi_stage_filters_with_exception):
        sequential_filter = MultiStageFilter(
            how="sequential", filters=multi_stage_filters_with_exception
        )
        with pytest.raises(Exception):
            # should raise an error
            sequential_filter.evaluate(Path("abcdef"))
        # should work out fine
        assert not sequential_filter.evaluate(Path("Hello World"))

    @pytest.mark.usefixtures("multi_stage_filters_with_exception")
    def test_sequential_filter_evaluation(self, multi_stage_filters_with_exception):
        # the any filter should shortcut the exception
        any_filter = MultiStageFilter(
            how="any", filters=multi_stage_filters_with_exception
        )
        with pytest.raises(Exception):
            # should raise an error
            any_filter.evaluate(Path("Hello World"))
        # should work out fine
        assert any_filter.evaluate(Path("abcdef"))


# TODO  Add proper test for stage types, for sequential break out etc!!


def test_extension_filter():
    txt_filter = FileExtensionFilter(".txt")

    assert txt_filter.evaluate(Path("HelloWorld.txt"))
    assert not txt_filter.evaluate(Path("HelloWorld.log"))


def test_modular_filter():
    my_generic_filter = ModularFilter("Sample", lambda x: True, "Description")

    assert my_generic_filter.evaluate("a")

    def is_greater_five(i) -> bool:
        return i > 5

    greater_five_filter = ModularFilter("GreaterFive", is_greater_five)
