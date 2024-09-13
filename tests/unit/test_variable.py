import pytest
from templatr.exceptions import MissingValue
from templatr.formatter import DefaultFormatter, ListFormatter
from templatr.variable import FormatterData, Variable, VariableData


def test_formatter_data_default_args__when_given_none_as_args__sets_args_to_empty_list():
    sut = FormatterData(
        cls="Formatter",
        args=None,
    )

    assert sut.args == []


def test_formatter_data_default_args__when_args_unset__sets_args_to_empty_list():
    sut = FormatterData(
        cls="Formatter",
    )

    assert sut.args == []


def test_formatter_data_default_args__when_args_set_to_list__sets_args_to_list():
    sut = FormatterData(
        cls="Formatter",
        args=["first"],
    )

    assert sut.args == ["first"]


def test_formatter_data_default_kwargs__when_kwargs_set_to_none__sets_kwargs_to_empty_dict():
    sut = FormatterData(
        cls="Friends",
        kwargs=None,
    )

    assert sut.kwargs == {}


def test_formatter_data_default_kwargs__when_kwargs_not_set__sets_kwargs_to_empty_dict():
    sut = FormatterData(
        cls="Friends",
    )

    assert sut.kwargs == {}


def test_formatter_data_default_kwargs__when_kwargs_set_to_dict__sets_kwargs_to_dict():
    sut = FormatterData(
        cls="Friends",
        kwargs={"google": ".com"},
    )

    assert sut.kwargs == {"google": ".com"}


def test_variable_data__when_creating_instance__defaults_formatter_to_formatter_name():
    sut = VariableData(
        key="key",
    )

    assert sut.formatter.cls == "DefaultFormatter"
    assert sut.formatter.args == []
    assert sut.formatter.kwargs == {}


def test_variable_data__when_creating_instance__sets_default_to_none():
    sut = VariableData(
        key="key",
    )

    assert sut.default is None


def test_variable_data__when_creating_instance__sets_path_to_none():
    sut = VariableData(
        key="key",
    )

    assert sut.path is None


def test_variable__when_creating_instance__sets_path_to_none():
    sut = Variable(key="key")

    assert sut.path is None


def test_variable__when_creating_instance__sets_default_to_none():
    sut = Variable(key="key")

    assert sut.default is None


def test_variable__when_creating_instance__sets_formatter_to_default_formatter():
    sut = Variable(key="key")

    assert isinstance(sut.formatter, DefaultFormatter)


def test_variable__when_path_set_to_none__sets_path_to_none():
    sut = Variable(
        key="key",
        path=None,
    )

    assert sut.path is None


def test_variable__when_path_set_to_path_array__sets_path_to_array():
    sut = Variable(
        key="key",
        path=["path", "str"],
    )

    assert sut.path == ["path", "str"]


def test_variable__when_path_set_to_str__sets_path_to_string_split_by_dot():
    sut = Variable(
        key="key",
        path="path.str",
    )

    assert sut.path == ["path", "str"]


def test_variable__when_from_dict__given_minimalist_dict__parses_into_variable():
    _input = {"key": "key"}
    sut = Variable.from_dict(_input)

    assert sut.key == "key"


def test_variable__when_from_dict__given_dict_defining_path__parses_into_variable():
    _input = {
        "key": "key",
        "path": "input.path",
    }
    sut = Variable.from_dict(_input)

    assert sut.path == ["input", "path"]


def test_variable__when_from_dict__given_dict_defining_default__parses_into_variable():
    _input = {
        "key": "key",
        "path": "input.path",
        "default": "NOT SET",
    }
    sut = Variable.from_dict(_input)

    assert sut.default == "NOT SET"


def test_variable__when_from_dict__given_dict_defining_minimalist_formatter__parses_into_variable():
    _input = {
        "key": "key",
        "path": "input.path",
        "default": "NOT SET",
        "formatter": {
            "cls": "DefaultFormatter",
        },
    }
    sut = Variable.from_dict(_input)

    assert isinstance(sut.formatter, DefaultFormatter)


def test_variable__when_from_dict__given_dict_defining_configurable_formatter__parses_into_variable():
    _input = {
        "key": "key",
        "path": "input.path",
        "default": "NOT SET",
        "formatter": {
            "cls": "ListFormatter",
            "args": ["\n"],
        },
    }
    sut = Variable.from_dict(_input)

    assert isinstance(sut.formatter, ListFormatter)
    assert sut.formatter.seperator == "\n"


def test_variable__when_resolving_value_for_variable_that_is_given_no_path__uses_key_as_path():
    sut = Variable(key="key")
    _input = {"key": "Whats up"}

    assert sut.resolve(_input) == "Whats up"


def test_variable__when_resolving_value_for_variable_that_simple_path__finds_value():
    sut = Variable(key="key", path="super")
    _input = {"super": "Sonic Racing"}

    assert sut.resolve(_input) == "Sonic Racing"


def test_variable__when_resolving_value_for_variable_that_kind_of_shallow_path__finds_value():
    sut = Variable(key="key", path="super.edit")
    _input = {"super": {"edit": "Sonic Racing"}}

    assert sut.resolve(_input) == "Sonic Racing"


def test_variable__when_resolving_value_for_variable_super_nested_path__finds_value():
    sut = Variable(key="key", path="super.edit.path.in.the.deep")
    _input = {"super": {"edit": {"path": {"in": {"the": {"deep": "Sonic Racing"}}}}}}

    assert sut.resolve(_input) == "Sonic Racing"


def test_variable__when_resolving_path_that_does_not_exist_and_default_set__returns_default():
    sut = Variable(key="key", path="supa", default="NOT SET")
    _input = {"super": "cutie"}

    assert sut.resolve(_input) == "NOT SET"


def test_variable__when_resolving_path_that_does_not_exist_and_default_is_not_set__raises_MissingValue():
    sut = Variable(key="key", path="supa")
    with pytest.raises(MissingValue):
        sut.resolve({"super": "VALUE"})


def test_variable__when_resolving_path_that_does_not_exist_on_object_and_default_is_not_set__raises_MissingValue():
    sut = Variable(key="key", path="supa")

    class Obj:
        def __init__(self) -> None:
            self.super = "Value"

    with pytest.raises(MissingValue):
        sut.resolve(Obj())


def test_variable__when_resolving_path_that_does_not_exist_on_object_and_default_set__returns_default():
    sut = Variable(key="key", path="supa", default="NOT SET")

    class Obj:
        def __init__(self) -> None:
            self.super = "Value"

    assert sut.resolve(Obj()) == "NOT SET"


def test_variable__when_resolving_path_on_object__returns_value():
    sut = Variable(key="key", path="super", default="NOT SET")

    class Obj:
        def __init__(self) -> None:
            self.super = "Value"

    assert sut.resolve(Obj()) == "Value"
