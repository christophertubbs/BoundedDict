"""
A dictionary defined by ranges instead of discrete keys
"""
from __future__ import annotations
import typing
from typing import Any

from .entry import Bound
from .entry import Comparable
from .entry import Entry

_KT = typing.TypeVar("_KT", bound=Comparable)
_T = typing.TypeVar("_T")

_KEY = typing.Tuple[_KT, _KT]

class BoundedDict(typing.Dict[Bound[_KT], _T]):
    """
    A dictionary that uses bounds for keys instead of discrete values
    """
    def __init__(self) -> None:
        self.__entries: typing.List[Entry] = list()

    def __getitem__(self, key: _KEY) -> _T:
        pass
    
    def __setitem__(self, key: _KEY, value: _T):
        pass

