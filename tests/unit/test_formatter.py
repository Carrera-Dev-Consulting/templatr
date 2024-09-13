from typing import Any
from templatr.formatter import (
    DefaultFormatter,
    ListFormatter,
    VariableFormatter,
    load_formatter,
)


def test_default_formatter__when_given_any_value__returns_value_as_is():
    sut = DefaultFormatter()
    expected = "value"
    value = sut.format(expected)
    assert value is expected


def test_list_formatter__when_given_list_with_multiple_items__joins_values_with_seperator():
    sut = ListFormatter(seperator=", ")
    value = sut.format([1, 2])
    assert value == "1, 2"


def test_list_formatter__when_given_list_with_single_item__returns_item_as_string():
    sut = ListFormatter(", ")
    value = sut.format([1])
    assert value == "1"


def test_load_formatter__when_given_formatter_in_module__loads_formatter_correctly():
    formatter = load_formatter("DefaultFormatter", [], {})
    assert isinstance(formatter, DefaultFormatter)


def test_load_formatter__when_given_formatter_with_args__loads_formatter_correctly():
    formatter = load_formatter("ListFormatter", [", "], {})
    assert formatter.seperator == ", "


def test_load_formatter__when_given_formatter_with_kwargs__loads_formatter_correctly():
    formatter = load_formatter("ListFormatter", [], {"seperator": ", "})
    assert formatter.seperator == ", "


class CustomFormatter(VariableFormatter):
    def format(self, value: Any) -> Any:
        return f"Custom: {value}"


def test_load_formatter__when_given_custom_formatter__loads_formatter():
    formatter = load_formatter("unit.test_variable.CustomFormatter", [], {})
    assert isinstance(formatter, CustomFormatter)
