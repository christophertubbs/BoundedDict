from __future__ import annotations

import typing

T = typing.TypeVar("T")


class Comparable(typing.Protocol, typing.Generic[T]):
    def __eq__(self, __value: object) -> bool:
        ...

    def __gt__(self, other: Comparable[T]) -> bool:
        ...

    def __ge__(self, other: Comparable[T]) -> bool:
        ...

    def __lt__(self, other: Comparable[T]) -> bool:
        ...

    def __le__(self, other: Comparable[T]) -> bool:
        ...


COMPARABLE = Comparable[T]


class Bound(COMPARABLE):
    def __init__(self, lower: T, upper: T):
        self.__lower: T = lower
        self.__upper: T = upper

    @property
    def lower_bound(self) -> T:
        return self.__lower
    
    @property
    def upper_bound(self) -> T:
        return self.__upper
    
    def __contains__(self, value: T) -> bool:
        return self.lower_bound <= value <= self.upper_bound
    
    def intersects(self, other: Bound[T]) -> bool:
        intersects_to_the_right = self.lower_bound <= other.lower_bound <= self.upper_bound
        intersects_to_the_left = other.lower_bound <= self.upper_bound <= other.upper_bound 
        return intersects_to_the_left or intersects_to_the_right
    
    