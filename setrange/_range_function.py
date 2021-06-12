from typing import TypeVar

from ._range_class import SetRange, SetRangeUnitII, SetRangeUnitEE, SetRangeUnitEI, SetRangeUnitIE

T = TypeVar('T')


def srange(start: T, end: T, edge: str = '[)') -> SetRange[T]:
    if edge == '[)':
        return SetRangeUnitIE(start, end)
    elif edge == '[]':
        return SetRangeUnitII(start, end)
    elif edge == '(]':
        return SetRangeUnitEI(start, end)
    elif edge == '()':
        return SetRangeUnitEE(start, end)
