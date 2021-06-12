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

    @abstractmethod
    def __bool__(self):
        ...

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        ...


class SetRangeUnit(SetRange[T], ABC):
    start: T
    include_start: bool
    end: T
    include_end: bool

    def __eq__(self, other):
        if isinstance(other, SetRangeUnit):
            if self.is_empty and other.is_empty:
                return True
            else:
                return self.start == other.start and \
                       self.end == other.end and \
                       self.include_start == other.include_start and \
                       self.include_end == other.include_end
        else:
            return False

    def __hash__(self):
        return hash(('SetRangeUnit', self.start, self.end, self.include_start, self.include_end))


class SetRangeUnitEmpty(SetRangeUnit[T]):

    def __init__(self):
        self.start = None
        self.end = None
        self.include_start = False
        self.include_end = False

    def __contains__(self, item):
        return False

    def __bool__(self):
        return False

    @property
    def is_empty(self) -> bool:
        return True


class SetRangeUnitII(SetRangeUnit[T]):

    def __init__(self, start: T, end: T):
        self.start = start
        self.end = end
        self.include_start = True
        self.include_end = True

    def __contains__(self, item):
        return self.start <= item <= self.end

    def __bool__(self):
        return True

    @property
    def is_empty(self) -> bool:
        return False


class SetRangeUnitIE(SetRangeUnit[T]):

    def __init__(self, start: T, end: T):
        self.start = start
        self.end = end
        self.include_start = True
        self.include_end = False

    def __contains__(self, item):
        return self.start <= item < self.end

    def __bool__(self):
        return True

    @property
    def is_empty(self) -> bool:
        return False


class SetRangeUnitEI(SetRangeUnit[T]):

    def __init__(self, start: T, end: T):
        self.start = start
        self.end = end
        self.include_start = False
        self.include_end = True

    def __contains__(self, item):
        return self.start < item <= self.end

    def __bool__(self):
        return True

    @property
    def is_empty(self) -> bool:
        return False


class SetRangeUnitEE(SetRangeUnit[T]):

    def __init__(self, start: T, end: T):
        self.start = start
        self.end = end
        self.include_start = False
        self.include_end = False

    def __contains__(self, item):
        return self.start < item < self.end

    def __bool__(self):
        return True

    @property
    def is_empty(self) -> bool:
        return False


class SetRangeSum(SetRange[T]):
    pass
