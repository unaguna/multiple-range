import abc
import math
from abc import abstractmethod

from ._interval_class import UnionInterval
from ._interval_function import interval


class UnionRange(abc.ABC):
    _base_union_interval: UnionInterval[int]

    def __init__(self, union_interval: UnionInterval):
        # __eq__ のために正規化しておく
        self._base_union_interval = self._normalize_int_interval(union_interval)

    def __eq__(self, other):
        if isinstance(other, UnionRange):
            return self._base_union_interval == other._base_union_interval
        else:
            return False

    @abstractmethod
    def __iter__(self):
        ...

    @abstractmethod
    def __reversed__(self):
        ...

    @abstractmethod
    def _normalize_int_interval(self, union_interval: UnionInterval) -> UnionInterval[int]:
        """区間を正規化する。

        Parameters
        ----------
        union_interval
            正規化する区間

        Returns
        -------
        UnionInterval
            正規化された区間
        """


class _UnionRangeForward(UnionRange):

    def __iter__(self):
        for interval_unit in self._base_union_interval:
            num = interval_unit.min()
            while num in interval_unit:
                yield num
                num = num + 1

    def __reversed__(self):
        for interval_unit in reversed(self._base_union_interval):
            num = interval_unit.sup() - 1
            while num in interval_unit:
                yield num
                num = num - 1

    def _normalize_int_interval(self, union_interval: UnionInterval) -> UnionInterval[int]:
        if not union_interval.is_interval:
            return sum(map(self._normalize_int_interval, union_interval), interval(empty=True))
        else:
            if union_interval.is_empty:
                return union_interval

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
