from ._interval_class import UnionInterval
from ._iterint_class import UnionRange, _UnionRangeForward


def iterint(union_interval: UnionInterval) -> UnionRange:
    return _UnionRangeForward(union_interval)
