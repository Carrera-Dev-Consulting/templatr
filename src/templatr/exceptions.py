from typing import Any, Dict


class TemplatrException(Exception):
    pass


class InvalidFormatter(TemplatrException):
    def __init__(self, formatter_cls: str, args: list, kwargs: Dict[str, Any]) -> None:
        super().__init__(f"Unable to instatiate formatter: {formatter_cls}")
        self.formatter_cls = formatter_cls
        self.args = args
        self.kwargs = kwargs
