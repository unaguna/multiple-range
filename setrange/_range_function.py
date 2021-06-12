from typing import TypeVar

from ._range_class import SetRange, SetRangeUnitII, SetRangeUnitEE, SetRangeUnitEI, SetRangeUnitIE

T = TypeVar('T')


def srange(start: T = None, end: T = None, edge: str = '[)', empty: bool = False) -> SetRange[T]:
    # TODO: start, end が None である場合の処理

    if edge == '[)':
        return SetRangeUnitIE(start, end)
    elif edge == '[]':
        return SetRangeUnitII(start, end)
    elif edge == '(]':
        return SetRangeUnitEI(start, end)
    elif edge == '()':
        return SetRangeUnitEE(start, end)
