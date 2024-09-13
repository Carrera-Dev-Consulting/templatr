from typing import Any


class DictClass:
    def __init__(self, wrapped: dict) -> None:
        self.__dict__ = wrapped

    def __getattribute__(self, name: str) -> Any:
        return self.__dict__.get(name)
