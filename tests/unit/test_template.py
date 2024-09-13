from templatr.template import Template
from templatr.variable import Variable


def test_template__when_given_a_template_with_no_variables__formats_data_as_expected():
    sut = Template(text="BASIC", variables=[])
    result = sut.format({})
    assert result == "BASIC"


def test_template__when_given_template_with_single_variable__formats_variable_into_output():
    sut = Template(
        variables=[
            Variable(
                key="NAME",
                path=["name"],
            )
        ],
        text="Hello {NAME}!",
    )
    result = sut.format({"name": "Jeffery"})
    assert result == "Hello Jeffery!"


def test_template__when_given_template_that_uses_variable_multiple_times__uses_same_value_each_time():
    sut = Template(
        variables=[
            Variable(
                key="NAME",
                path=["name"],
            )
        ],
        text="Hello {NAME}!, We are gonna die {NAME}",
    )
    result = sut.format({"name": "Jeffery"})
    assert result == "Hello Jeffery!, We are gonna die Jeffery"


def test_template__when_given_template_that_uses_multiple_variables__uses_each_variable():
    sut = Template(
        variables=[
            Variable(
                key="NAME",
                path=["name"],
            ),
            Variable(
                key="AGE",
                path=["age"],
            ),
        ],
        text="Hello {NAME}!, We are gonna die {AGE}",
    )
    result = sut.format({"name": "Jeffery", "age": 20})
    assert result == "Hello Jeffery!, We are gonna die 20"


def test_template__when_given_template_with_mutliple_variables__uses_them_in_the_order_of_the_variable_names():
    sut = Template(
        variables=[
            Variable(
                key="NAME",
                path=["name"],
            ),
            Variable(
                key="AGE",
                path=["age"],
            ),
        ],
        text="{AGE}, {NAME}",
    )
    result = sut.format({"name": "Billy", "age": 22})

    assert result == "22, Billy"
