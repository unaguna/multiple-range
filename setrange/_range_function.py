from typing import TypeVar

from ._range_class import SetRange, SetRangeUnitII, SetRangeUnitEE, SetRangeUnitEI, SetRangeUnitIE, SetRangeUnitEmpty

T = TypeVar('T')


def srange(start: T = None, end: T = None, edge: str = '[)', empty: bool = False) -> SetRange[T]:
    # TODO: start, end が None である場合の処理

    if empty:
        return SetRangeUnitEmpty()

    if edge == '[)':
        if start < end:
            return SetRangeUnitIE(start, end)
        else:
            return SetRangeUnitEmpty()
    elif edge == '[]':
        if start <= end:
            return SetRangeUnitII(start, end)
        else:
            return SetRangeUnitEmpty()
    elif edge == '(]':
        if start < end:
            return SetRangeUnitEI(start, end)
        else:
            return SetRangeUnitEmpty()
    elif edge == '()':
        if start < end:
            return SetRangeUnitEE(start, end)
        else:
            return SetRangeUnitEmpty()

    # TODO: edge が想定外である場合の処理
