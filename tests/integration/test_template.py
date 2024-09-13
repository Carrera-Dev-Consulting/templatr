import os

import pytest

from templatr.exceptions import UnsupportedSource
from templatr.formatter import DefaultFormatter, ListFormatter
from templatr.template import load_json_template, load_yaml_template
from templatr.variable import Variable

json_file = "example.json"
yaml_file = "example.yaml"

TEMPLATE = """Hello {name}, This is meant to represent what we can do with this
Everything comes down to what you want to write {name} and be able to change.
Today we can show required variables {age}, and the defaulted ones like {unset}
Here are the reasons this is great:
{reasons}
"""
VARIABLES = [
    Variable(
        key="name",
        path="name",
        formatter=DefaultFormatter(),
        default="Nameless",
    ),
    Variable(
        key="age",
    ),
    Variable(
        key="unset",
        default="NOT SET",
    ),
    Variable(
        key="reasons",
        formatter=ListFormatter("\n"),
    ),
]


def test_load_json_template__when_given_a_file_pointer__loads_template(
    resources_path,
):
    with open(os.path.join(resources_path, json_file), mode="r") as fp:
        template = load_json_template(fp)

    assert template.text == TEMPLATE
    assert template.variables == VARIABLES


def test_load_json_template__when_given_a_path_to_json_file__loads_template(
    resources_path,
):
    template = load_json_template(os.path.join(resources_path, json_file))
    assert template.text == TEMPLATE
    assert template.variables == VARIABLES


def test_load_json_template__when_random_object__raises_UnsupportedSource():
    with pytest.raises(UnsupportedSource):
        load_json_template(object())


def test_load_yaml_template__when_given_a_file_pointer__loads_template(
    resources_path,
):
    with open(os.path.join(resources_path, yaml_file), mode="r") as fp:
        template = load_yaml_template(fp)
    assert template.text == TEMPLATE
    assert template.variables == VARIABLES


def test_load_yaml_template__when_given_a_file_path__loads_template(
    resources_path,
):
    template = load_yaml_template(os.path.join(resources_path, yaml_file))
    assert template.text == TEMPLATE
    assert template.variables == VARIABLES


def test_load_yaml_template__when_unsupported_type__raises_UnsupportedSource():
    with pytest.raises(UnsupportedSource):
        load_yaml_template(object())
