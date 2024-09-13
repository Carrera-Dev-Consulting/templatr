from typing import Any


class DictObjectView:
    """*Internal Class used to be able to access values of a dict as an object instead of calling `get`.*

    **Args**
    - **wrapped (_type_)**: dict we are wrapping to expose as an object.
    """

    def __init__(self, wrapped: dict) -> None:
        self.__dict__ = wrapped

    def __getattribute__(self, name: str) -> Any:
        return self.__dict__.get(name)
