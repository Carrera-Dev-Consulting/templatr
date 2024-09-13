from functools import singledispatch
from typing import IO, Any

from pydantic import BaseModel
from yaml import safe_load

from templatr.helpers import DictClass

from .variable import Variable


class Template(BaseModel):
    variables: list[Variable]
    text: str

    def format(self, data: Any):
        final_values = {
            variable.key: variable.resolve(data) for variable in self.variables
        }

        return self.text.format(final_values)

    @classmethod
    def from_dict(cls, data: dict):
        data = DictClass(data)
        return cls(
            variables=[
                Variable.from_variable_data(variable) for variable in data.variables
            ],
            text=data.text,
        )


@singledispatch
def load_yaml_template(path: Any):
    raise ValueError(f"Unable to load_yaml from source: {path}")


@load_yaml_template.register
def _(path: str):
    with open(path, "r") as fp:
        return Template.from_dict(safe_load(fp))


@load_yaml_template.register
def _(path: IO):
    return Template.from_dict(safe_load(path))


@singledispatch
def load_json_template(path: Any):
    raise ValueError(f"Unable to load_json from source: {path}")


@load_json_template.register
def _(path: str):
    with open(path, "r") as fp:
        return Template.from_dict(safe_load(path))


@load_json_template.register
def _(path: IO):
    return Template.from_dict(safe_load(path))
