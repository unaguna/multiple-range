from ._interval_class import UnionInterval
from ._iterint_class import UnionRange, _UnionRangeForward, _UnionRangeReversed


def iterint(union_interval: UnionInterval,
            *,
            reverse: bool = False) -> UnionRange:
    if reverse:
        return _UnionRangeReversed(union_interval)
    else:
        return _UnionRangeForward(union_interval)
