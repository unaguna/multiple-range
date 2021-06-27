from typing import TypeVar, Optional, overload

from ._range_class import construct_unit, SetRange
from ._range_end_point import MinEndPoint, MaxEndPoint

T = TypeVar('T')


@overload
def srange(start: T = None, end: T = None, edge: str = '[)', empty: bool = False):
    ...


@overload
def srange(start: None = None, end: T = None, edge: str = '()', empty: bool = False) -> SetRange[T]:
    ...


@overload
def srange(start: T = None, end: None = None, edge: str = '[)', empty: bool = False) -> SetRange[T]:
    ...


@overload
def srange(start: None = None, end: None = None, edge: str = '()', empty: bool = False) -> SetRange[T]:
    ...


def srange(start: Optional[T] = None, end: Optional[T] = None, edge: str = '[)', empty: bool = False) -> SetRange[T]:

    if empty:
        return SetRange()

    if start is None:
        start = MinEndPoint()
        include_start = False
    elif edge[0] == '[':
        include_start = True
    elif edge[0] == '(':
        include_start = False
    else:
        raise ValueError('edge must be \'[]\', \'[)\', \'(]\', or \'()\'.')

    if end is None:
        end = MaxEndPoint()
        include_end = False
    elif edge[1] == ']':
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
