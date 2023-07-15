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


class Bound(typing.Generic[T]):
    """
    Defines the boundaries of the key
    """
    def __init__(self, lower: T, upper: T):
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
    

    def __str__(self):
        return f"[{self.lower_bound}, {self.upper_bound}]"
    
    def __repr__(self) -> str:
        return str(self)