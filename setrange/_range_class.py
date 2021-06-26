from abc import abstractmethod, ABC
from typing import TypeVar, Generic, List, Optional

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
        elif isinstance(other, SetRange):
            return SetRange(self) == other
        else:
            return False

    def __hash__(self):
        return hash(('SetRangeUnit', self.start, self.end, self.include_start, self.include_end))

    @abstractmethod
    def __str__(self):
        ...

    def __repr__(self):
        return f'srange({self.start}, {self.end}, ' \
               f'\'{"[" if self.include_start else "("}{"]" if self.include_end else ")"}\')'

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


def construct_unit(start: T, end: T, include_start: bool, include_end: bool) -> Optional[SetRangeUnit[T]]:
    """SetRangeUnit を継承したインスタンスを作成する。

    Parameters
    ----------
    start
        始点
    end
        終点
    include_start
        始点を含有するかどうか
    include_end
        終点を含有するかどうか

    Returns
    -------
    SetRangeUnit[T]
        構成したインスタンス。空集合となる場合は None。
    """
    if include_start and not include_end:
        if start < end:
            return SetRangeUnitIE(start, end)
        else:
            return None
    elif include_start and include_end:
        if start <= end:
            return SetRangeUnitII(start, end)
        else:
            return None
    elif not include_start and include_end:
        if start < end:
            return SetRangeUnitEI(start, end)
        else:
            return None
    elif not include_start and not include_end:
        if start < end:
            return SetRangeUnitEE(start, end)
        else:
            return None


def _sum_units(e1: SetRangeUnit[T], e2: SetRangeUnit[T]) -> Optional[SetRangeUnit[T]]:
    """2つのレンジの合併がレンジである場合に、その合併を返す。

    Returns
    -------
    SetRangeUnit[T]
        2つのレンジの合併がレンジである場合は合併。そうでない場合は None。
    """
    if e1.start > e2.start or (e1.start == e2.start and e2.include_start):
        e1, e2 = e2, e1

    if e1.end < e2.start:
        return None
    if e1.end == e2.start and not e1.include_end and not e2.include_start:
        return None

    start_point = e1
    if e1.end < e2.end or (e1.end == e2.end and e2.include_end):
        end_point = e2
    else:
        end_point = e1

    return construct_unit(start=start_point.start,
                          end=end_point.end,
                          include_start=start_point.include_start,
                          include_end=end_point.include_end)


def _mul_units(e1: SetRangeUnit[T], e2: SetRangeUnit[T]) -> Optional[SetRangeUnit[T]]:
    """2つのレンジの交叉を返す。

    Returns
    -------
    SetRangeUnit[T]
        2つのレンジの交叉が空集合でない場合は交叉。空集合である場合は None。
    """
    if e1.start > e2.start or (e1.start == e2.start and e2.include_start):
        e1, e2 = e2, e1

    if e1.end < e2.start:
        return None
    if e1.end == e2.start and not (e1.include_end and e2.include_start):
        return None

    start_point = e2
    if e1.end < e2.end or (e1.end == e2.end and not e1.include_end):
        end_point = e1
    else:
        end_point = e2

    return construct_unit(start=start_point.start,
                          end=end_point.end,
                          include_start=start_point.include_start,
                          include_end=end_point.include_end)


class SetRange(Generic[T]):
    _unit_list: List[SetRangeUnit[T]]

    def __init__(self, *units: SetRangeUnit[T]):
        # 引数に与えられた unit のリストは以下の条件を満たさなければならない。
        # ・unit 同士は共通部分を持たない
        # ・空の unit が含まれない
        # ・start でソートされている
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
        elif isinstance(other, SetRangeUnit):
            return self == SetRange(other)
        else:
            return False

    def __str__(self):
        if self.is_empty:
            return '(empty)'
        else:
            return '∪'.join(map(str, self._unit_list))

    def __repr__(self):
        return ' + '.join(map(repr, self._unit_list))

    def __bool__(self):
        return not self.is_empty

    def __add__(self, other):
        """集合論における合併演算

        Returns
        -------
        SetRange[T]
        """
        if isinstance(other, SetRange):
            result_unit_list = list()
            left_unit_list = list(self._unit_list)
            right_unit_list = list(other._unit_list)
            l_index = 0
            r_index = 0

            while l_index < len(left_unit_list) and r_index < len(right_unit_list):
                l_unit = left_unit_list[l_index]
                r_unit = right_unit_list[r_index]

                # 和
                sum_unit = _sum_units(l_unit, r_unit)

                if sum_unit is not None:
                    # l_unit と r_unit の和が区間になる場合は統合して次へ
                    left_unit_list[l_index] = sum_unit
                    r_index += 1

                    # 統合後の区間を left に入れたことで、非標準系になりうるので標準化
                    while l_index + 1 < len(left_unit_list):
                        tmp_unit = _sum_units(left_unit_list[l_index], left_unit_list[l_index+1])
                        if tmp_unit is None:
                            break
                        else:
                            left_unit_list[l_index + 1] = tmp_unit
                            l_index += 1
                else:
                    # 和が区間にならないなら、より値が小さいほうはそのまま結果として採用する。
                    if l_unit.start < r_unit.start:
                        result_unit_list.append(l_unit)
                        l_index += 1
                    else:
                        result_unit_list.append(r_unit)
                        r_index += 1

            result_unit_list.extend(left_unit_list[l_index:])
            result_unit_list.extend(right_unit_list[r_index:])

            return SetRange(*result_unit_list)

        else:
            raise TypeError(f'unsupported operand type(s) for +: \'{type(self)}\' and \'{type(other)}\'')

    def __mul__(self, other):
        """集合論における交叉演算

        Returns
        -------
        SetRange[T]
        """
        if isinstance(other, SetRange):
            # 分配法則 (a+b)*(c+d) = (a+b)*c + (a+b)*d を使用する。
            unit_list_r = list(other._unit_list)

            result = SetRange()
            for set_range in map(lambda u: self * u, unit_list_r):
                result += set_range

            return result
        elif isinstance(other, SetRangeUnit):
            # SetRange 同士の積の演算の中で SetRange * SetRangeUnit がよばれるため、この分岐が必要。

            # 分配法則 (a+b)*c = a*c + b*c を使用する。
            # c をかけることで a, b の順序が逆転したり共通部分が生じたりすることはないため、改めて標準化する必要はない。
            result_unit_list = filter(lambda u: u is not None, map(lambda u: _mul_units(u, other), self._unit_list))
            return SetRange(*result_unit_list)
        else:
            raise TypeError(f'unsupported operand type(s) for *: \'{type(self)}\' and \'{type(other)}\'')

    @property
    def is_empty(self) -> bool:
        return len(self._unit_list) <= 0

    @property
    def unit_num(self) -> int:
        return len(self._unit_list)
