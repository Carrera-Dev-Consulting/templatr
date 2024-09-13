from functools import singledispatch
from typing import IO, Any, Dict, List, Optional, TypedDict

from pydantic import BaseModel
from yaml import safe_load

from templatr.exceptions import UnsupportedSource
from templatr.helpers import DictObjectView

from .variable import Variable


class FormatterDict(TypedDict):
    cls: str
    args: list
    kwargs: Dict[str, Any]


class VariableDict(TypedDict):
    key: str
    path: Optional[str]
    default: Optional[str]
    formatter: FormatterDict


class TemplateDict(TypedDict):
    variables: List[VariableDict]
    text: str


class Template(BaseModel):
    """*Template that can be given a dict or object to pull values from.*

    **Args**
    - **variables (list[Variable])**: List of variables used by template.
    - **text (str)**: String text that we are formatting against.
    """

    variables: List[Variable]
    text: str

    def format(self, data: Any) -> str:
        """*Takes in data that will then be applied to the template to create the output string.*

        **Args**
        - **data (Any)**: Source of variables we will be puling from.

        **Returns**
        - **(str)**: String text with data that we formatted into it.
        """
        final_values = {
            variable.key: variable.resolve(data) for variable in self.variables
        }

        return self.text.format(**final_values)

    @classmethod
    def from_dict(cls, data: TemplateDict):
        """*Class method to be able to construct a template from a given dict that matches its structure that will parse variables into proper classes dynamically.*

        **Args**
        - **data (dict)**: template as a dict that defines variables and text to format against.

        **Returns**
        - (Template): The template we were able to create from the given info.
        """
        data = DictObjectView(data)
        return cls(
            variables=[Variable.from_dict(variable) for variable in data.variables],
            text=data.text,
        )


@singledispatch
def load_yaml_template(path: Any) -> Template:
    """*Loads yaml file as template object for you automatically.*

    **Args**
    - **path (str, IO)**: source of yaml content to format and parse into Template object

    ***UnsupportedSource***
        ValueError: Failed to parse yaml into template

    **Returns**
    - **(Template)**: template that was parsed.
    """
    raise UnsupportedSource(type(path))


@load_yaml_template.register
def _(path: str):
    with open(path, "r") as fp:
        return Template.from_dict(safe_load(fp))


@load_yaml_template.register
def _(path: IO):
    return Template.from_dict(safe_load(path))


@singledispatch
def load_json_template(path: Any) -> Template:
    """*Loads json file as template for you automatically.*

    **Args**
    - **path (str, IO)**: Source of json to parse.

    ***Raises***
    - **UnsupportedSource**: Failed to parse json into template.

    **Returns**
    - **(Template)**: template that was parsed.
    """
    raise UnsupportedSource(type(path))


@load_json_template.register
def _(path: str):
    with open(path, "r") as fp:
        return Template.from_dict(safe_load(path))


@load_json_template.register
def _(path: IO):
    return Template.from_dict(safe_load(path))
