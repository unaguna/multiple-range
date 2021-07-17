from ._interval_class import UnionInterval
from ._iterint_class import UnionRange, _UnionRangeForward


def iterint(union_interval: UnionInterval,
            *,
            reverse: bool = False) -> UnionRange:
    return _UnionRangeForward(union_interval)
