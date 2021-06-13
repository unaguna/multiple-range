from abc import abstractmethod, ABC
from typing import TypeVar, Generic, List

T = TypeVar('T')


class SetRangeUnit(Generic[T], ABC):
    start: T
    include_start: bool
    end: T
    include_end: bool

    @abstractmethod
    def __contains__(self, item):
        ...

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

    @abstractmethod
    def __str__(self):
        ...

    def __bool__(self):
        return not self.is_empty

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        ...


class SetRangeUnitII(SetRangeUnit[T]):

    def __init__(self, start: T, end: T):
        self.start = start
        self.end = end
        self.include_start = True
        self.include_end = True

    def __contains__(self, item):
        return self.start <= item <= self.end

    def __str__(self):
        return f'[{self.start}, {self.end}]'

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

    def __str__(self):
        return f'[{self.start}, {self.end})'

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

    def __str__(self):
        return f'({self.start}, {self.end}]'

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

    def __str__(self):
        return f'({self.start}, {self.end})'

    @property
    def is_empty(self) -> bool:
        return False


class SetRange(Generic[T]):
    _unit_list: List[SetRangeUnit[T]]

    def __init__(self, *units: SetRangeUnit[T]):
        # 引数に与えられた unit のリストは以下の条件を満たさなければならない。
        # ・unit 同士は共通部分を持たない
        # ・空の unit が含まれない
        # ・start, include_start, end, include_end でソートされている
        self._unit_list = list(units)

    def __contains__(self, item):
        for unit in self._unit_list:
            if item in unit:
                return True
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, SetRange):
            return self._unit_list == other._unit_list
        else:
            return False

    def __str__(self):
        if self.is_empty:
            return '(empty)'
        else:
            return '∪'.join(map(str, self._unit_list))

    def __bool__(self):
        return not self.is_empty

    def __add__(self, other):
        """集合論における合併演算

        Returns
        -------
        SetRange[T]
        """
        # TODO: 実装

    @property
    def is_empty(self) -> bool:
        return len(self._unit_list) <= 0
