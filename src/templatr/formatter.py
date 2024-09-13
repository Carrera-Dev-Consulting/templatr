from abc import ABC, abstractmethod
from typing import Any
import importlib

from templatr.exceptions import InvalidFormatter, UnknownFormatter


class VariableFormatter(ABC):
    """*Base Class for formatters that are used to coerce the value we define in our templates into a string for interpolation.*"""

    @abstractmethod
    def format(self, value: Any) -> Any:  # pragma: no cover
        """*Format function that will manipulate the value into whatever shape you want it to with no restriction on the return type.*

        **Args**
        - **value** (Any): Value we want to format.

        **Returns**
        - **(Any)**: the value you want to put into your template
        """
        pass

    def __call__(self, value: Any) -> Any:
        """*Call to make our formatters work like a function, offloads call to abstracted `format` method.*

        **Args**
        - **value (Any)**: Value we want to format.

        **Returns**
        - **(Any)**: Formatted value
        """
        return self.format(value)


class DefaultFormatter(VariableFormatter):
    """*Default Formatter that will just return the value back as is making no modifications. This should be used if you don't need any special formatting for your variable value before it gets interpolated.*"""

    def format(self, value: Any):
        """*Formats value by not doing anything to it. Used for when you want the value as is.*

        **Args**
        - **value (Any)**: value to format.

        **Returns**
        - **(Any)**: same as value arg.
        """
        return value


class ListFormatter(VariableFormatter):
    """*Formatter used to join a list of items together for output.*

    **Args**
    - **seperator (str)**: The string you want to use to join the items in your list together with.
    """

    seperator: str

    def __init__(self, seperator: str) -> None:
        self.seperator = seperator

    def format(self, value: list):
        """*Formats the list given as value into a single string of the items as a string joined with the configured seprator.*

        **Args**
        - **value (list)**: List of items we are formatting.

        **Returns**
        - **(str)**: Formatted string of list joined by seperator.
        """
        # coerce into string iterable and send it with join
        return self.seperator.join((str(v) for v in value))


def load_formatter(cls_name: str, args: list, kwargs: dict):
    """*Loads a formatter dynamically by using the cls_name to dynamically discover the formatter cls_instance and passes in the args, and kwargs given to instance.*

    **Args**
    - **cls_name (str)**: Fully-Qualified Classname for Formatter class or a Class Name for a formatter in the templatr formatter module.
    - **args (list)**: Arguments you wish to pass to your formatter instance.
    - **kwargs (dict)**: Key-Word Arguments you wish to pass to your formatter instance.

    ***Raises***
    - **UnknownFormatter**: when given cls_name cannot be loaded correctly.
    - **InvalidFormatter**: When given cls is not a variable formatter.
    - **InvalidFormatter**: When given args and kwargs cannot create formatter class.

    **Returns**
    - **(VariableFormatter)**: VariableFormatter that was instantiated from the given arguments.
    """
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
    except Exception as exc:
        raise UnknownFormatter(f"Unknown formatter class: {cls_name}") from exc

    if not issubclass(_cls_instance, VariableFormatter):
        raise InvalidFormatter(formatter_cls=cls_name, args=args, kwargs=kwargs)
    try:
        return _cls_instance(*args, **kwargs)
    except Exception as exc:
        raise InvalidFormatter(
            formatter_cls=cls_name, args=args, kwargs=kwargs
        ) from exc
