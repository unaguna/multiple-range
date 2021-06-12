from typing import TypeVar

from ._range_class import SetRange, SetRangeUnit

T = TypeVar('T')


def srange(start: T, end: T) -> SetRange[T]:
    return SetRangeUnit(start, end)
