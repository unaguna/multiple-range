from abc import abstractmethod, ABC
from typing import TypeVar, Generic

T = TypeVar('T')


class SetRange(Generic[T], ABC):

    @abstractmethod
    def __contains__(self, item):
        ...


class SetRangeUnit(SetRange[T]):
    start: T
    include_start: bool
    end: T
    include_end: bool

    def __init__(self, start: T, end: T):
        self.start = start
        self.end = end
        self.include_start = True
        self.include_end = False

    def __contains__(self, item):
        return self.start <= item < self.end


class SetRangeSum(SetRange[T]):
    pass
