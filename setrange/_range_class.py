from abc import abstractmethod, ABC
from typing import TypeVar, Generic

T = TypeVar('T')


class SetRange(Generic[T], ABC):

    @abstractmethod
    def __contains__(self, item):
        ...

    @abstractmethod
    def __eq__(self, other):
        ...

    @property
    def is_empty(self) -> bool:
        # TODO: 抽象メソッド化
        return False


class SetRangeUnit(SetRange[T], ABC):
    start: T
    include_start: bool
    end: T
    include_end: bool

    def __eq__(self, other):
        if isinstance(other, SetRangeUnit):
            return self.start == other.start and \
                   self.end == other.end and \
                   self.include_start == other.include_start and \
                   self.include_end == other.include_end
        else:
            return False

    def __hash__(self):
        return hash(('SetRangeUnit', self.start, self.end, self.include_start, self.include_end))


class SetRangeUnitII(SetRangeUnit[T]):

    def __init__(self, start: T, end: T):
        self.start = start
        self.end = end
        self.include_start = True
        self.include_end = True

    def __contains__(self, item):
        return self.start <= item <= self.end


class SetRangeUnitIE(SetRangeUnit[T]):

    def __init__(self, start: T, end: T):
        self.start = start
        self.end = end
        self.include_start = True
        self.include_end = False

    def __contains__(self, item):
        return self.start <= item < self.end


class SetRangeUnitEI(SetRangeUnit[T]):

    def __init__(self, start: T, end: T):
        self.start = start
        self.end = end
        self.include_start = False
        self.include_end = True

    def __contains__(self, item):
        return self.start < item <= self.end


class SetRangeUnitEE(SetRangeUnit[T]):

    def __init__(self, start: T, end: T):
        self.start = start
        self.end = end
        self.include_start = False
        self.include_end = False

    def __contains__(self, item):
        return self.start < item < self.end


class SetRangeSum(SetRange[T]):
    pass
