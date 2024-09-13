from typing import Any

import pytest
from templatr.exceptions import InvalidFormatter, UnknownFormatter
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
    formatter = load_formatter("tests.unit.test_formatter.CustomFormatter", [], {})
    assert isinstance(formatter, CustomFormatter)


def test_load_formatter__when_given_a_formatter_that_does_not_exist__raises_UnknownFormatter():
    with pytest.raises(UnknownFormatter):
        load_formatter("FakeFormatterLol", [], {})


def test_load_formatter__when_missing_parameters_for_formatter__raises_InvalidFormatter():
    with pytest.raises(InvalidFormatter):
        load_formatter("ListFormatter", [], {})


def test_load_formatter__when_too_many_parameters_for_formatter__raises_InvalidFormatter():
    with pytest.raises(InvalidFormatter):
        load_formatter("ListFormatter", [", "], {"seperator": " "})


def test_load_formatter__when_class_loaded_is_not_formatter__raises_InvalidFormatter():
    with pytest.raises(InvalidFormatter):
        load_formatter("pydantic.BaseModel", [], {})
