from abc import ABC, abstractmethod
from typing import Any
import importlib


class VariableFormatter(ABC):
    @abstractmethod
    def format(self, value: Any) -> Any:
        pass

    def __call__(self, value: Any) -> Any:
        return self.format(value)


class DefaultFormatter(VariableFormatter):
    def format(self, value: Any):
        return value


class ListFormatter(VariableFormatter):
    def __init__(self, seperator: str) -> None:
        self.seperator = seperator

    def format(self, value: list):
        # coerce into string iterable and send it with join
        return self.seperator.join((str(v) for v in value))


def load_formatter(cls_name: str, args: list, kwargs: dict):
    index = cls_name.rfind(".")
    if index == -1:
        # we are using one referenced in this module.
        _module, _cls = __name__, cls_name
    else:
        _module, _cls = cls_name[0:index], cls_name[index + 1 :]
    try:
        _module_instance = importlib.import_module(_module)
        _cls_instance: type[VariableFormatter] = getattr(
            _module_instance, _cls
        )  # will raise exception when class does not exist.
    except:
        raise ValueError(f"Unknown formatter class: {cls_name}")

    if not issubclass(_cls_instance, VariableFormatter):
        raise ValueError(
            f"Formatter {cls_name} is not a VariableFormatter, must inherit from base class to be used"
        )
    return _cls_instance(*args, **kwargs)
