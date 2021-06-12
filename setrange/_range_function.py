from typing import TypeVar

from ._range_class import SetRange

T = TypeVar('T')


def srange(start: T, end: T) -> SetRange[T]:
    pass
