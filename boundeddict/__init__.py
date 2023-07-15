from __future__ import annotations
import typing

from .entry import Bound
from .entry import Comparable

_KT = typing.TypeVar("_KT", bound=Comparable)
_T = typing.TypeVar("_T")


class BoundedDict(typing.Mapping[Bound[_KT], _T]):
    """
    A dictionary that uses bounds for keys instead of discrete values
    """
    def __init__(self) -> None:
        self.__entries: typing.List = list()