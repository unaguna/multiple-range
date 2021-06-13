from typing import TypeVar

from ._range_class import SetRange, SetRangeUnitII, SetRangeUnitEE, SetRangeUnitEI, SetRangeUnitIE

T = TypeVar('T')


def srange(start: T = None, end: T = None, edge: str = '[)', empty: bool = False) -> SetRange[T]:
    # TODO: start, end が None である場合の処理

    if empty:
        return SetRange()

    if edge == '[)':
        if start < end:
            return SetRange(SetRangeUnitIE(start, end))
        else:
            return SetRange()
    elif edge == '[]':
        if start <= end:
            return SetRange(SetRangeUnitII(start, end))
        else:
            return SetRange()
    elif edge == '(]':
        if start < end:
            return SetRange(SetRangeUnitEI(start, end))
        else:
            return SetRange()
    elif edge == '()':
        if start < end:
            return SetRange(SetRangeUnitEE(start, end))
        else:
            return SetRange()

    # TODO: edge が想定外である場合の処理
