import math

from ._interval_class import UnionInterval
from ._interval_function import interval


def _normalize_int_interval(union_interval: UnionInterval) -> UnionInterval[int]:
    """区間を正規化する。

    整数値のみが入ることを前提に、区間を2整数 a, b を用いて [a, b) と表すよう変更する。

    Parameters
    ----------
    union_interval
        正規化する区間

    Returns
    -------
    UnionInterval
        正規化された区間
    """
    if not union_interval.is_interval:
        return sum(map(_normalize_int_interval, union_interval), interval(empty=True))
    else:
        # start を決定
        if union_interval.left_closed():
            start = math.ceil(union_interval.inf())
        else:
            start = math.floor(union_interval.inf()) + 1

        # end を決定
        if union_interval.right_closed():
            end = math.floor(union_interval.sup()) + 1
        else:
            end = math.ceil(union_interval.sup())

        return interval(start, end, edge='[)')


class UnionRange:
    _base_union_interval: UnionInterval[int]

    def __init__(self, union_interval: UnionInterval):
        self._base_union_interval = _normalize_int_interval(union_interval)

    def __eq__(self, other):
        if isinstance(other, UnionRange):
            return self._base_union_interval == other._base_union_interval
        else:
            return False

    def __iter__(self):
        for interval_unit in self._base_union_interval:
            num = interval_unit.min()
            while num in interval_unit:
                yield num
                num = num + 1
