from typing import Any, ClassVar, Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict, field_validator

from templatr.exceptions import MissingValue
from templatr.formatter import DefaultFormatter, VariableFormatter, load_formatter


_UNSET = object()


class FormatterData(BaseModel):
    """*Internal class that we use to describe and parse out the value we need to define a formatter for a variable.*

    **Args**
    - **cls (str)**: class of formatter we are trying to load.
    - **args (list)**: arguments for the formatter we are loading.
    - **kwargs (dict[str, Any])**: keyword arguments for the formatter we are loading.
    """

    cls: str
    args: list = []
    kwargs: Dict[str, Any] = {}

    @field_validator("args", mode="before")
    def _default_args(cls, args: Optional[list]):
        """*field validator to default None args to empty list instead.*

        **Args**
        - **args (list, None)**: optional list that will be set to args.

        **Returns**
        - **(list)**: list value to set to args.
        """
        if args is None:
            return []
        return args

    @field_validator("kwargs", mode="before")
    def _default_kwargs(cls, kwargs: Optional[Dict[str, Any]]):
        """*field validator for kwargs to default None to empty dict.*

        **Args**
        - **kwargs (dict, None)**: possibly none kwargs we will be parsing.

        **Returns**
        - **(dict)**: dict to use as kwargs.
        """
        if kwargs is None:
            return {}
        return kwargs


class VariableData(BaseModel):
    """*Data to define a template variable.*

    **Args**
    - **key (str)**: The key you will be using in the template text string.
    - **path (str)**: The path you will be looking at in the data that is seperated by dots e.g. `field.nested.value`
    - **default (str)**: The default value you will use in place of value if we cannot grab value from data.
    - **formatter (FormatterData)**: The formatter data to define how we want to render the value for the variable.
    """

    key: str
    path: Optional[str] = None
    default: Optional[str] = None
    formatter: FormatterData = FormatterData(
        cls=DefaultFormatter.__name__,
        args=[],
        kwargs={},
    )


def _resolve_value(data: Any, path: List[str]):
    """*Resolves the value from an object that will go until it reaches it at the end of the path.*

    **Args**
    - **data (Any)**: The data that will be checked for the path.
    - **path (list[str])**: The path parts to look into on the object.

    **Returns**
    - **(_UNSET)**: Singleton of class representing no value being able to parsed.
    - **(Any)**: Value that we resolved from data.
    """
    current_value = data
    for section in path:
        if isinstance(current_value, dict):
            current_value = current_value.get(section, _UNSET)
            if current_value is _UNSET:
                # value was not set so we can't continue
                return _UNSET
        else:
            # assume it is a generic object
            try:
                current_value = getattr(current_value, section)
            except AttributeError:
                return _UNSET
    # should be left with value we wanted to select from object
    return current_value


class Variable(BaseModel):
    """*Variable to be used in the template.*

    **Args**
    - **key (str)**: Key in the template that the variable references
    - **path (list[str], None)**: Path for variable value from incoming data, if None will default to key.
    - **default (str, None)**: Default value for variable if not able to resolve from data.
    - **formatter (VariableFormatter)**: Formatter that will be used to change the object into something that can be put into your template. defaults to: `DefaultFormatter`
    """

    key: str
    path: Optional[List[str]] = None
    default: Optional[Any] = None
    formatter: VariableFormatter = DefaultFormatter()
    model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("path", mode="before")
    def _split_path(cls, value: Union[None, str, List[str]]):
        """*field validator to split up the path as parts of string based on dot.*

        **Args**
        - **value (str, list[str], None)**: Value we are working against in validator.

        **Returns**
        - **(list[str])**: path for value of variable on data.
        """
        if value is None:
            return value
        elif isinstance(value, str):
            return value.split(".")
        else:
            return value

    def resolve(self, data: Any) -> Any:
        """*Resolves value from data using the given path of the configured variable otherwise defaults to value of given default.*

        **Args**
        - **data (Any)**: the data we are pulling the value from.

        ***Raises***
        - **MissingValue**: When value could not be determined for variable and no default has been set.

        **Returns**
        - **(Any)**: the formatted data that was resolved from the given data.
        """
        # use the path that given but if not set or empty default to key
        value_path = self.path or [self.key]
        value = _resolve_value(data, value_path)
        if value is _UNSET:
            if self.default is None:
                raise MissingValue(self.key, self.path)
            value = self.default

        return self.formatter(value)

    @classmethod
    def from_dict(cls, data: dict):
        """*Creates a variable from a dict definition.*

        **Args**
        - **data (dict)**: dict definition of variable that matches the format in VariableData.

        **Returns**
        - **(Variable)**: Variable parsed from dict.
        """
        data: VariableData = VariableData.model_validate(data)
        formatter_args = data.formatter

        formatter = load_formatter(
            formatter_args.cls,
            formatter_args.args,
            formatter_args.kwargs,
        )

        return cls(
            key=data.key,
            path=data.path,
            default=data.default,
            formatter=formatter,
        )
