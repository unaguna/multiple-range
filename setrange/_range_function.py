from typing import TypeVar

from ._range_class import construct_unit, SetRange

T = TypeVar('T')


def srange(start: T = None, end: T = None, edge: str = '[)', empty: bool = False) -> SetRange[T]:
    # TODO: start, end が None である場合の処理

    if empty:
        return SetRange()

    if edge[0] == '[':
        include_start = True
    elif edge[0] == '(':
        include_start = False
    else:
        raise ValueError('edge must be \'[]\', \'[)\', \'(]\', or \'()\'.')

    if edge[1] == ']':
        include_end = True
    elif edge[1] == ')':
        include_end = False
    else:
        raise ValueError('edge must be \'[]\', \'[)\', \'(]\', or \'()\'.')

    unit = construct_unit(start, end, include_start, include_end)
    if unit is not None:
        return SetRange(unit)
    else:
        return SetRange()
