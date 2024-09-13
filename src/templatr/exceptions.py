from typing import Any, Dict, List


class TemplatrException(Exception):
    """*Base Class for all library specific exceptions.*"""

    pass


class InvalidFormatter(TemplatrException):
    """*Exception to be raised if we have issues with creating your formatter dynamically.*

    **Args**
    - **formatter_cls (str)**: fully qualified classname of custom formatter or classname of built-in Formatters that can be found in templatr.formatters.
    - **args (list)**: list of arguments to passed into the formatter
    - **kwargs (dict[str, Any]))**: dict of keyword arguments passed to the formatter
    """

    formatter_cls: str
    args: list
    kwargs: Dict[str, Any]

    def __init__(self, formatter_cls: str, args: list, kwargs: Dict[str, Any]) -> None:
        super().__init__(f"Unable to instatiate formatter: {formatter_cls}")
        self.formatter_cls = formatter_cls
        self.args = args
        self.kwargs = kwargs


class UnknownFormatter(TemplatrException):
    """*Exception Raised when formatter we tried to create did not exist to be loaded.*

    **Args**
    - **formatter_cls (str)**: Class we attempted to load.
    """

    def __init__(self, formatter_cls: str) -> None:
        super().__init__(f"Unable to find formatter with name: {formatter_cls}")
        self.formatter_cls = formatter_cls


class UnsupportedSource(TemplatrException):
    """*Exception Raised when we are trying to parse json or yaml into template but are not able to use type for parsing.*

    **Args**
    - **_type(type)**: The type we couldn't read the format from.
    """

    def __init__(self, _type: type) -> None:
        super().__init__(f"Unable to parse from source: {_type}")


class MissingValue(TemplatrException):
    """*Exception Raised when we are unable to resolve a value for a given variable and no default has been set.*

    **Args**
    - **key (str)**: The template key we are missing.
    - **path (list[str])**: The path we looked for value in object.
    """

    def __init__(self, key: str, path: List[str]) -> None:
        formatted_path = ".".join(path)
        super().__init__(
            f"Could not resolve value for variable: {key}, using path: {formatted_path}"
        )

        self.key = key
        self.path = path
