"""
A dictionary defined by ranges instead of discrete keys
"""
from __future__ import annotations
import typing

from uuid import uuid1

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

    def get(self, key: _KEY, default=None) -> typing.Any:
        if not isinstance(key, typing.Sequence) or len(key) != 2:
            raise ValueError(
                f"'{str(key)}' cannot be used as a key - "
                "value must be a sequence of two values marking a lower and upper bound"
            )
        
        return self.search(key=key, default=default)
        

    def __getitem__(self, key: _KEY) -> _T:
        if not isinstance(key, typing.Sequence) or len(key) != 2:
            raise ValueError(
                f"'{str(key)}' cannot be used as a key - "
                "value must be a sequence of two values marking a lower and upper bound"
            )
        sentinel = uuid1()
        searched_value = self.search(key=key, default=sentinel)

        if searched_value == sentinel:
            raise KeyError(f"There are no keys in this dictionary matching '{str(key)}'")
        
        return searched_value

    def __setitem__(self, key: _KEY, value: _T):
        if not isinstance(key, typing.Sequence) or len(key) != 2:
            raise ValueError(
                f"'{str(key)}' cannot be used as a key - "
                "value must be a sequence of two values marking a lower and upper bound"
            )
        for entry in self.__entries:
            if key in entry:
                key.set(key, value)

    @typing.overload
    def search(self, lower_bound: _KT, upper_bound: _KT, default=None) -> typing.Optional[typing.Union[_T, typing.Sequence[_T]]]:
        """
        Search for a value
        """
        return self.search(key=(lower_bound, upper_bound), default=default)

    def search(self, key: _KEY, default=None) -> typing.Optional[typing.Union[_T, typing.Sequence[_T]]]:
        """
        Search for a value
        """
        if not isinstance(key, typing.Sequence) or len(key) != 2:
            raise ValueError(
                f"'{str(key)}' cannot be used as a key - "
                "value must be a sequence of two values marking a lower and upper bound"
            )
        
        for entry in self.__entries:
            found_value = entry.search(key)
            if found_value:
                return found_value

        return default

