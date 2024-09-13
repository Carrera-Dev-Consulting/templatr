from templatr.formatter import DefaultFormatter, ListFormatter


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
