from templatr.variable import FormatterData, VariableData


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
