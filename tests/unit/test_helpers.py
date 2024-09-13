from templatr.helpers import DictObjectView


def test_dict_object_view__when_getting_value_that_does_exist_in_dict__returns_from_getattr():
    value = {"simple": "value"}
    sut = DictObjectView(value)

    assert sut.simple == "value"


def test_dict_object_view__when_getting_value_that_does_not_exist_in_dict__returns_none():
    value = {"simple": "value"}
    sut = DictObjectView(value)

    assert sut.dne is None
