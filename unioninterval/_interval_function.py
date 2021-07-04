from typing import TypeVar, Optional, overload

from ._interval_class import construct_unit, SetRange
from ._interval_endpoint import MinEndPoint, MaxEndPoint

T = TypeVar('T')


@overload
def srange(start: T = None, end: T = None, edge: str = '[)', empty: bool = False, singleton: T = None):
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


def srange(start: Optional[T] = None,
           end: Optional[T] = None,
           edge: str = '[)',
           empty: bool = False,
           singleton: T = None) -> SetRange[T]:
    """srange インスタンスを作成する。

    この関数では数学的な意味での『区間』に相当するインスタンスが作成される。

    この関数では『区間』でない集合を作ることはできないが、集合における合併を + 演算として実装しているため、
    この関数で作成されるインスタンスの和を計算することで区間の有限合併に相当するインスタンスを作成できる。

    必ずしも端点が数値である必要はなく、比較演算 (<, <=, >, >=) が実装されていてそれが全順序性をもっていればよい。

    Parameters
    ----------
    start
        レンジの始点。None が指定された場合、下に有界でないレンジが作成される。
    end
        レンジの終点。None が指定された場合、上に有界でないレンジが作成される。
    edge: str
        レンジの始点や終点をレンジに含むかどうかを指定する。'[]', '[)', '(]', '()' のいずれかを指定することができる。
        '[' と '(' は始点を含むかどうかを指定する文字であり、'[' であればこのレンジは始点を含み、'(' であれば含まない。
        同様に ']' と ')' は終点を含むかどうかを指定する文字であり、']' であればこのレンジは終点を含み、')' であれば終点を含まない。
        ただし、ここでいう含むとは集合における含有 (∈) の意味であり、python の演算子 in で判定されるものである。
    empty: bool
        True を指定すると空集合に相当するレンジが作成される。このとき、他の引数は無視される。
    singleton
        None 以外の値を指定すると、その値のみを含む区間が作成される。このとき、他の引数は無視される。
        ただし、引数 empty が True である場合はこの引数が無視されて空集合に相当するレンジが作成される。

    Returns
    -------
    SetRange
        作成されたレンジ
    """

    if empty:
        return SetRange()

    if singleton is not None:
        return SetRange(construct_unit(singleton, singleton, True, True))

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
