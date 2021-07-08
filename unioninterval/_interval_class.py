from abc import abstractmethod, ABC
from typing import TypeVar, Generic, List, Optional

from ._interval_endpoint import MinEndPoint, MaxEndPoint

T = TypeVar('T')


class Interval(Generic[T], ABC):
    start: T
    include_start: bool
    end: T
    include_end: bool

    @abstractmethod
    def __contains__(self, item):
        ...

    def __eq__(self, other):
        if isinstance(other, Interval):
            if self.is_empty and other.is_empty:
                return True
            else:
                return self.start == other.start and \
                       self.end == other.end and \
                       self.include_start == other.include_start and \
                       self.include_end == other.include_end
        elif isinstance(other, UnionInterval):
            return UnionInterval(self) == other
        else:
            return False

    def __hash__(self):
        return hash(('Interval', self.start, self.end, self.include_start, self.include_end))

    @abstractmethod
    def __str__(self):
        ...

    def __repr__(self):
        return f'interval({self.start}, {self.end}, ' \
               f'\'{"[" if self.include_start else "("}{"]" if self.include_end else ")"}\')'

    def __bool__(self):
        return not self.is_empty

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        ...

    def measure(self):
        return self.end - self.start


class IntervalII(Interval[T]):

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


class IntervalIE(Interval[T]):

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


class IntervalEI(Interval[T]):

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


class IntervalEE(Interval[T]):

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


def construct_unit(start: T, end: T, include_start: bool, include_end: bool) -> Optional[Interval[T]]:
    """Interval を継承したインスタンスを作成する。

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
    Interval[T]
        構成したインスタンス。空集合となる場合は None。
    """
    if include_start and not include_end:
        if start < end:
            return IntervalIE(start, end)
        else:
            return None
    elif include_start and include_end:
        if start <= end:
            return IntervalII(start, end)
        else:
            return None
    elif not include_start and include_end:
        if start < end:
            return IntervalEI(start, end)
        else:
            return None
    elif not include_start and not include_end:
        if start < end:
            return IntervalEE(start, end)
        else:
            return None


def _sum_units(e1: Interval[T], e2: Interval[T]) -> Optional[Interval[T]]:
    """2つのレンジの合併がレンジである場合に、その合併を返す。

    Returns
    -------
    Interval[T]
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


def _mul_units(e1: Interval[T], e2: Interval[T]) -> Optional[Interval[T]]:
    """2つのレンジの交叉を返す。

    Returns
    -------
    Interval[T]
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


class UnionInterval(Generic[T]):
    _unit_list: List[Interval[T]]

    def __init__(self, *units: Interval[T]):
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
        if isinstance(other, UnionInterval):
            return self._unit_list == other._unit_list
        else:
            return False

    def __hash__(self):
        return hash(tuple(self._unit_list))

    def __str__(self):
        if self.is_empty:
            return '(empty)'
        else:
            return '∪'.join(map(str, self._unit_list))

    def __repr__(self):
        if self.is_empty:
            return 'interval(empty=True)'
        else:
            return ' + '.join(map(repr, self._unit_list))

    def __bool__(self):
        return not self.is_empty

    def __iter__(self):
        for unit in self._unit_list:
            yield UnionInterval(unit)

    def __getitem__(self, item: int):
        if isinstance(item, slice):
            return UnionInterval(*self._unit_list[item])
        else:
            return UnionInterval(self._unit_list[item])

    def __len__(self) -> int:
        return len(self._unit_list)

    def __add__(self, other):
        """集合論における合併演算

        Returns
        -------
        UnionInterval[T]
        """
        if isinstance(other, UnionInterval):
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
                        tmp_unit = _sum_units(left_unit_list[l_index], left_unit_list[l_index + 1])
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

            return UnionInterval(*result_unit_list)

        else:
            return NotImplemented

    def __mul__(self, other):
        """集合論における交叉演算

        Returns
        -------
        UnionInterval[T]
        """
        if isinstance(other, UnionInterval):
            # 分配法則 (a+b)*(c+d) = (a+b)*c + (a+b)*d を使用する。
            unit_list_r = list(other._unit_list)

            result = UnionInterval()
            for set_range in map(lambda u: self * u, unit_list_r):
                result += set_range

            return result
        elif isinstance(other, Interval):
            # UnionInterval 同士の積の演算の中で UnionInterval * Interval がよばれるため、この分岐が必要。

            # 分配法則 (a+b)*c = a*c + b*c を使用する。
            # c をかけることで a, b の順序が逆転したり共通部分が生じたりすることはないため、改めて標準化する必要はない。
            result_unit_list = filter(lambda u: u is not None, map(lambda u: _mul_units(u, other), self._unit_list))
            return UnionInterval(*result_unit_list)
        else:
            return NotImplemented

    def __le__(self, other):
        try:
            return self.issubset(other)
        except TypeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self != other and self.issubset(other)
        except TypeError:
            return NotImplemented

    def __ge__(self, other):
        try:
            return self.issuperset(other)
        except TypeError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return self != other and self.issuperset(other)
        except TypeError:
            return NotImplemented

    def issubset(self, other) -> bool:
        """すべての要素が other に含まれるか判定する。

        Parameters
        ----------
        other: UnionInterval
            判定対象の UnionInterval。

        Returns
        -------
        bool
            すべての要素が other に含まれれば True、そうでない場合は False。
        """
        if isinstance(other, UnionInterval):
            return self + other == other
        else:
            raise TypeError(f'unsupported argument type for {type(self)}.issubset: \'{type(other)}\'')

    def issuperset(self, other) -> bool:
        """other のすべての要素が含まれるか判定する。

        Parameters
        ----------
        other: UnionInterval
            判定対象の UnionInterval。

        Returns
        -------
        bool
            other のすべての要素が含まれれば True、そうでない場合は False。
        """
        if isinstance(other, UnionInterval):
            return self + other == self
        else:
            raise TypeError(f'unsupported argument type for {type(self)}.issuperset: \'{type(other)}\'')

    def is_bounded_below(self) -> bool:
        """下に有界であるかどうかを返す
        """
        if self.is_empty:
            return True
        else:
            return self._unit_list[0].start != MinEndPoint()

    def is_bounded_above(self) -> bool:
        """上に有界であるかどうかを返す
        """
        if self.is_empty:
            return True
        else:
            return self._unit_list[-1].end != MaxEndPoint()

    def complement(self):
        """補集合である UnionInterval を作成して返す。

        Returns
        -------
        UnionInterval
            このインスタンスの補集合
        """
        # 戻り値となる UnionInterval の _unit_list
        complement_unit_list = []

        # このインスタンスの各 Interval に左から接する Interval を作って戻り値の UnionInterval を構成する unit とする。
        next_start = MinEndPoint()
        next_include_start = False
        for unit in self._unit_list:
            complement_unit_list.append(construct_unit(next_start,
                                                       unit.start,
                                                       next_include_start,
                                                       not unit.include_start))
            next_start = unit.end
            next_include_start = not unit.include_end

        # 上のループでは、最後の Interval に右から接する Interval を作っていないため、作る。
        complement_unit_list.append(construct_unit(next_start, MaxEndPoint(), next_include_start, False))

        # 上のループで (-inf,-inf] を作ろうとした場合などに complement_unit_list に None が入るため、それを除去して使用する。
        return UnionInterval(*filter(lambda u: u is not None, complement_unit_list))

    def measure(self, *, zero=0):
        """UnionInterval の長さを返す。

        長さの計算は - 演算によって行い、複数の Interval の長さの和は + 演算によって行われる。
        ただし、空集合である場合は zero に指定した値を返し、UnionInterval が有界でない場合は ValueError を raise する。

        Parameters
        ----------
        zero
            空集合の長さとして出力する値

        Returns
        -------
        any
            このレンジの長さ。

        Raises
        ------
        ValueError
            このインスタンスが上下に有界でない場合
        """
        if self.is_empty:
            return zero
        elif self.is_bounded_below() and self.is_bounded_above():
            return sum(map(lambda u: u.measure(), self._unit_list[1:]), self._unit_list[0].measure())
        else:
            raise ValueError('The UnionInterval is not bounded.')

    @property
    def is_empty(self) -> bool:
        return len(self._unit_list) <= 0

    @property
    def is_interval(self) -> bool:
        """数学的な区間であるかどうかを返す。

        Returns
        -------
        bool
            この UnionInterval が含むいかなる2点についてもその中点がこの UnionInterval に含まれるなら True。
            そうでなければ False。
        """
        return len(self._unit_list) <= 1
