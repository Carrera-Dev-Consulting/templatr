from typing import Any, ClassVar, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, field_validator

from templatr.exceptions import InvalidFormatter
from templatr.formatter import DefaultFormatter, VariableFormatter, load_formatter
from templatr.helpers import DictClass

_UNSET = object()


class FormatterData(BaseModel):
    cls: str
    args: Optional[list] = None
    kwargs: Optional[Dict[str, Any]] = None

    @field_validator("args", mode="before")
    def _default_args(cls, args):
        if args is None:
            return []

    @field_validator("kwargs", mode="before")
    def _default_kwargs(cls, kwargs):
        if kwargs is None:
            return {}


class VariableData(BaseModel):
    key: str
    path: str
    default: str
    formatter: FormatterData = FormatterData(
        cls=DefaultFormatter.__name__,
        args=[],
        kwargs={},
    )


def _resolve_value(data: Any, path: List[str]):
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
    key: str
    path: Optional[List[str]] = None
    default: Optional[Any] = None
    formatter: VariableFormatter = DefaultFormatter()
    model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("path", mode="before")
    def _split_path(cls, value):
        if value is None:
            return value
        elif isinstance(value, str):
            return value.split(".")
        else:
            return value

    def resolve(self, data: Any) -> Any:
        # use the path that given but if not set or empty default to key
        value_path = self.path or [self.key]
        value = _resolve_value(data, value_path)
        if value is _UNSET:
            value = self.default

        return self.formatter(value)

    @classmethod
    def from_dict(cls, data: dict):
        data: VariableData = VariableData.model_validate(data)
        formatter_args = data.formatter
        try:
            formatter = load_formatter(
                formatter_args.cls,
                formatter_args.args,
                formatter_args.kwargs,
            )
        except ValueError:
            raise InvalidFormatter(
                formatter_cls=formatter_args.cls,
                args=formatter_args.args,
                kwargs=formatter_args.kwargs,
            )

        return cls(
            key=data.key,
            path=data.path,
            default=data.default,
            formatter=formatter,
        )
