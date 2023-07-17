"""
Defines the basic keys for the bounded dict
"""
from __future__ import annotations

import typing

T = typing.TypeVar("T")
_KT = typing.TypeVar("_KT")


@typing.runtime_checkable
class Comparable(typing.Protocol, typing.Generic[T]):
    """
    Represents a generic type that implements comparison functions
    """

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


class Bound(typing.Generic[T]):
    """
    Defines the boundaries of the key
    """

    def __init__(self, lower: Comparable[T], upper: Comparable[T]):
        if not isinstance(lower, Comparable):
            raise ValueError(
                f"'{str(lower)}' may not be used as a lower bound - only comparable values are allowed"
            )
        self.__lower: T = lower
        """The least acceptable value"""

        self.__upper: T = upper
        """The largest acceptable value"""

    @property
    def lower_bound(self) -> T:
        """
        The least acceptable value
        """
        return self.__lower

    @property
    def upper_bound(self) -> T:
        """
        The largest acceptable value
        """
        return self.__upper

    def __contains__(self, value: T) -> bool:
        return self.lower_bound <= value <= self.upper_bound

    def intersects_on_left(self, other: Bound[T]) -> bool:
        """
        Whether this bound intersects another bound on the left hand side

        Example:
            >>> bound1 = Bound(0, 5)
            >>> bound2 = Bound(4, 9)
            >>> bound3 = Bound(8, 14)
            >>> bound1.intersects_on_left(bound2)
            False
            >>> bound1.intersects_on_left(bound3)
            False
            >>> bound2.intersects_on_left(bound1)
            True
            >>> bound2.intersects_on_left(bound3)
            False
            >>> bound3.intersects_on_left(bound1)
            False
            >>> bound3.intersects_on_left(bound2)
            True

        Args:
            other: The other bound to compare to

        Returns:
            Whether this bound intersects another bound on the left hand side
        """
        return other.lower_bound <= self.upper_bound <= other.upper_bound

    def intersects_on_right(self, other: Bound[T]) -> bool:
        """
        Whether this bound intersects another bound on the right

        Example:
            >>> bound1 = Bound(0, 5)
            >>> bound2 = Bound(4, 7)
            >>> bound3 = Bound(6, 10)
            >>> bound1.intersects_right(bound2)
            True
            >>> bound1.intersects_on_right(bound3)
            False
            >>> bound2.intersects_on_right(bound1)
            False
            >>> bound2.intersects_on_right(bound3)
            True

        Args:
            other: The other set of bounds to compare to

        Returns:
            Whether this bound intersects on the right
        """
        return self.lower_bound <= other.lower_bound <= self.upper_bound

    def intersects(self, other: Bound[T]) -> bool:
        """
        Whether this bound intersects with the other

        Example:
            >>> bound1 = Bound(0, 5)
            >>> bound2 = Bound(4, 7)
            >>> bound3 = Bound(6, 10)
            >>> bound1.intersects(bound2)
            True
            >>> bound1.intersects(bound3)
            False
            >>> bound2.intersects(bound1)
            True
            >>> bound2.intersects(bound3)
            True
            >>> bound3.intersects(bound1)
            False
            >>> bound3.intersects(bound2)
            True

        Args:
            other: The other set of bounds to compare to

        Returns:
            Whether this bound intersects with the other 
        """
        return self.intersects_on_left(other) or self.intersects_on_right(other)

    def distance_from(self, lower_bound: _KT, upper_bound: _KT):
        """
        Determines the distance between one bound and another
        """
        return (lower_bound - self.lower_bound) + (self.upper_bound - upper_bound)



    def __str__(self):
        return f"[{self.lower_bound}, {self.upper_bound}]"

    def __repr__(self) -> str:
        return str(self)


class Entry(typing.Generic[T, _KT]):
    """
    Represents an individual value within a Bounded Dictionary
    """
    def __init__(self, lower_bound: _KT, upper_bound: _KT, value: T) -> None:
        if lower_bound > upper_bound:
            lower_bound, upper_bound = upper_bound, lower_bound

        self.__bound: Bound[_KT] = Bound(lower=lower_bound, upper=upper_bound)
        self.__value = value
        self.__children: typing.List[Entry[T, _KT]] = list()

    @typing.overload
    def set(self, bound: typing.Tuple[_KT, _KT], value: T) -> None:
        lower_bound, upper_bound = bound

        if lower_bound > upper_bound:
            lower_bound, upper_bound = upper_bound, lower_bound

        return self.set(lower_bound=lower_bound, upper_bound=upper_bound, value=value)

    @typing.overload
    def set(self, bounds: slice[_KT], value: T):
        if bounds.start is None:
            lower_bound = self.lower_bound
        else:
            lower_bound = bounds.start

        if bounds.stop is None:
            upper_bound = self.upper_bound
        else:
            upper_bound = bounds.stop

        if lower_bound > upper_bound:
            lower_bound, upper_bound = upper_bound, lower_bound

        return self.set(lower_bound=lower_bound, upper_bound=upper_bound, value=value)

    def set(self, lower_bound: _KT, upper_bound: _KT, value: T) -> None:
        """
        Set the value on this entry or one of its children
        """
        if lower_bound > upper_bound:
            lower_bound, upper_bound = upper_bound, lower_bound

        if self.lower_bound == lower_bound and self.upper_bound == upper_bound:
            self.value = value

    @property
    def value(self) -> T:
        """
        The value that this entry contains
        """
        return self.__value

    @property
    def bounds(self) -> Bound[_KT]:
        """
        The bounds that dictates what may be found within this entry
        """
        return self.__bound

    @property
    def lower_bound(self) -> _KT:
        """
        The lower bound defining what may be in this entry
        """
        return self.__bound.lower_bound

    @property
    def upper_bound(self) -> _KT:
        """
        The lower bound defining what may be in this entry
        """
        return self.__bound.upper_bound

    @typing.overload
    def search(self, lower_bound: _KT, upper_bound: _KT) -> typing.Optional[typing.Union[T, typing.Sequence[T]]]:
        """
        Look for a value nested within this entry
        """
        return self.search((lower_bound, upper_bound))

    def search(self, bounds: typing.Tuple[_KT, _KT]) -> typing.Optional[typing.Union[T, typing.Sequence[T]]]:
        """
        Look for a value nested within this entry
        """
        if not isinstance(bounds, typing.Sequence) or len(bounds) != 2:
            raise ValueError(
                f"'{str(bounds)}' cannot be used to search - "
                "value must be a sequence of two values marking a lower and upper bound"
            )

        if bounds not in self:
            return None

        candidates: typing.List[Entry[T, _KT]] = list({
            child_entry.search(bounds)
            for child_entry in self.__children
            if bounds in child_entry
        })

        if candidates and len(candidates) == 1:
            return candidates[0]
        elif candidates and len(candidates) > 1:
            return candidates

        return self.value

    def __contains__(self, bounds: typing.Tuple[_KT, _KT]) -> bool:
        if not isinstance(bounds, typing.Sequence) or len(bounds) != 2:
            raise ValueError(
                f"'{str(bounds)}' cannot be used to check for containment - "
                "value must be a sequence of two values marking a lower and upper bound"
            )

        lower_bound, upper_bound = bounds
        return self.bounds.lower_bound <= lower_bound and upper_bound <= self.bounds.upper_bound
    