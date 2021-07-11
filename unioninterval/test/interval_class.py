from datetime import datetime, timedelta
from typing import Iterable, Sequence

import pytest

from unioninterval import interval, UnionInterval


class TestUnionIntervalClass:

    @pytest.mark.parametrize('set_range', (
            interval(empty=True),
            interval(5, 10, edge='[]'),
            interval(5, 10, edge='[)'),
            interval(5, 10, edge='(]'),
            interval(5, 10, edge='()'),
            interval('f', 's'),
            interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)),
    ))
    def test__interval_unit__type(self, set_range):
        """interval関数の戻り値の型をテストする
        """
        assert isinstance(set_range, UnionInterval)

    @pytest.mark.parametrize('set_range, expected_str', (
        (interval(empty=True), '(empty)'),
        (interval(5, 10, edge='[]'), '[5, 10]'),
        (interval(5, 10, edge='[)'), '[5, 10)'),
        (interval(5, 10, edge='(]'), '(5, 10]'),
        (interval(5, 10, edge='()'), '(5, 10)'),
        (interval(None, 10, edge='[]'), '(-inf, 10]'),
        (interval(None, 10, edge='[)'), '(-inf, 10)'),
        (interval(None, 10, edge='(]'), '(-inf, 10]'),
        (interval(None, 10, edge='()'), '(-inf, 10)'),
        (interval(5, None, edge='[]'), '[5, inf)'),
        (interval(5, None, edge='[)'), '[5, inf)'),
        (interval(5, None, edge='(]'), '(5, inf)'),
        (interval(5, None, edge='()'), '(5, inf)'),
        (interval(None, None, edge='[]'), '(-inf, inf)'),
        (interval(None, None, edge='[)'), '(-inf, inf)'),
        (interval(None, None, edge='(]'), '(-inf, inf)'),
        (interval(None, None, edge='()'), '(-inf, inf)'),
    ))
    def test__interval_unit_int__str(self, set_range, expected_str):
        """単レンジ[int]の文字列化をテストする。
        """
        assert str(set_range) == expected_str

    @pytest.mark.parametrize('set_range_1, set_range_2, expected_equal', (
        (interval(5, 10), interval(5, 10), True),
        (interval(5, 10), interval(5, 9), False),
        (interval(5, 10), interval(5, 10, edge='()'), False),
        (interval(5, 10), interval(5, 10, edge='(]'), False),
        (interval(5, 10), interval(5, 10, edge='[]'), False),
        (interval(None, 10), interval(None, 10, edge='[)'), True),
        (interval(None, 10), interval(None, 10, edge='()'), True),
        (interval(None, 10), interval(None, 10, edge='(]'), False),
        (interval(None, 10), interval(None, 10, edge='[]'), False),
        (interval(5, None), interval(5, None, edge='[)'), True),
        (interval(5, None), interval(5, None, edge='()'), False),
        (interval(5, None), interval(5, None, edge='(]'), False),
        (interval(5, None), interval(5, None, edge='[]'), True),
        (interval(None, None), interval(None, None, edge='[)'), True),
        (interval(None, None), interval(None, None, edge='()'), True),
        (interval(None, None), interval(None, None, edge='(]'), True),
        (interval(None, None), interval(None, None, edge='[]'), True),
        (interval(start=5), interval(5, None), True),
        (interval(start=5, edge='[)'), interval(5, None, edge='[)'), True),
        (interval(start=5, edge='()'), interval(5, None, edge='()'), True),
        (interval(end=10), interval(None, 10), True),
        (interval(end=10, edge='(]'), interval(None, 10, edge='(]'), True),
        (interval(end=10, edge='()'), interval(None, 10, edge='()'), True),
        (interval(), interval(None, None), True),
        (interval(empty=True), interval(empty=True), True),
        (interval(empty=True), interval(empty=True, singleton=1), True),
        (interval(singleton=1), interval(1, 1, edge='[]'), True),
        (interval(singleton=1), interval(1, 2, edge='[]'), False),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)),
         interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)), True),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)),
         interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 34)), False),
    ))
    def test__interval_unit__equal(self, set_range_1, set_range_2, expected_equal):
        """単レンジの等号演算をテストする。
        """
        if expected_equal:
            assert set_range_1 == set_range_2
            assert set_range_2 == set_range_1
            assert hash(set_range_1) == hash(set_range_2)
            assert hash(set_range_2) == hash(set_range_1)
        else:
            assert set_range_1 != set_range_2
            assert set_range_2 != set_range_1

    @pytest.mark.parametrize('set_range, element, expected_contain', (
        (interval(5, 10), 4, False),
        (interval(5, 10), 5, True),
        (interval(5, 10), 9, True),
        (interval(5, 10), 10, False),
        (interval(5, 10), 4.0, False),
        (interval(5, 10), 5.0, True),
        (interval(5, 10), 9.0, True),
        (interval(5, 10), 10.0, False),
        (interval(5, 10, '[]'), 4, False),
        (interval(5, 10, '[]'), 5, True),
        (interval(5, 10, '[]'), 10, True),
        (interval(5, 10, '[]'), 11, False),
        (interval(5, 10, '[]'), 4.0, False),
        (interval(5, 10, '[]'), 5.0, True),
        (interval(5, 10, '[]'), 10.0, True),
        (interval(5, 10, '[]'), 11.0, False),
        (interval(5, 10, '[)'), 4, False),
        (interval(5, 10, '[)'), 5, True),
        (interval(5, 10, '[)'), 9, True),
        (interval(5, 10, '[)'), 10, False),
        (interval(5, 10, '[)'), 4.0, False),
        (interval(5, 10, '[)'), 5.0, True),
        (interval(5, 10, '[)'), 9.0, True),
        (interval(5, 10, '[)'), 10.0, False),
        (interval(5, 10, '(]'), 5, False),
        (interval(5, 10, '(]'), 6, True),
        (interval(5, 10, '(]'), 10, True),
        (interval(5, 10, '(]'), 11, False),
        (interval(5, 10, '(]'), 5.0, False),
        (interval(5, 10, '(]'), 6.0, True),
        (interval(5, 10, '(]'), 10.0, True),
        (interval(5, 10, '(]'), 11.0, False),
        (interval(5, 10, '()'), 5, False),
        (interval(5, 10, '()'), 6, True),
        (interval(5, 10, '()'), 9, True),
        (interval(5, 10, '()'), 10, False),
        (interval(5, 10, '()'), 5.0, False),
        (interval(5, 10, '()'), 6.0, True),
        (interval(5, 10, '()'), 9.0, True),
        (interval(5, 10, '()'), 10.0, False),
        (interval(None, 10, '(]'), -10, True),
        (interval(None, 10, '(]'), 10, True),
        (interval(None, 10, '(]'), 11, False),
        (interval(None, 10, '()'), -10, True),
        (interval(None, 10, '()'), 9, True),
        (interval(None, 10, '()'), 10, False),
        (interval(5, None, '[)'), 4, False),
        (interval(5, None, '[)'), 5, True),
        (interval(5, None, '[)'), 100, True),
        (interval(5, None, '()'), 5, False),
        (interval(5, None, '()'), 6, True),
        (interval(5, None, '()'), 100, True),
        (interval('f', 's'), 'e', False),
        (interval('f', 's'), 'ee', False),
        (interval('f', 's'), 'f', True),
        (interval('f', 's'), 'fa', True),
        (interval('f', 's'), 's', False),
        (interval('f', 's'), 'sa', False),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)),
         datetime(2020, 12, 30, 11, 22, 32), False),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)),
         datetime(2020, 12, 30, 11, 22, 33), True),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)),
         datetime(2020, 12, 31, 11, 22, 32), True),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)),
         datetime(2020, 12, 31, 11, 22, 33), False),
        (interval(None, datetime(2020, 12, 31, 11, 22, 33)),
         datetime(1900, 12, 30, 11, 22, 33), True),
        (interval(None, datetime(2020, 12, 31, 11, 22, 33)),
         datetime(2020, 12, 31, 11, 22, 32), True),
        (interval(None, datetime(2020, 12, 31, 11, 22, 33)),
         datetime(2020, 12, 31, 11, 22, 33), False),
        (interval(datetime(2020, 12, 30, 11, 22, 33), None),
         datetime(2020, 12, 30, 11, 22, 32), False),
        (interval(datetime(2020, 12, 30, 11, 22, 33), None),
         datetime(2020, 12, 30, 11, 22, 33), True),
        (interval(datetime(2020, 12, 30, 11, 22, 33), None),
         datetime(2100, 12, 30, 11, 22, 33), True),
    ))
    def test__interval_unit__contain(self, set_range, element, expected_contain):
        """単レンジの含有演算をテストする。

        端点と比較できるオブジェクトであれば、含有するかどうか確かめられる。
        """
        if expected_contain:
            assert element in set_range
        else:
            assert element not in set_range

    @pytest.mark.parametrize('target, is_empty', (
        (interval(5, 6, '[]'), False),
        (interval(5, 6, '[)'), False),
        (interval(5, 6, '(]'), False),
        (interval(5, 6, '()'), False),
        (interval(5, 5, '[]'), False),
        (interval(5, 5, '[)'), True),
        (interval(5, 5, '(]'), True),
        (interval(5, 5, '()'), True),
        (interval(5, 4, '[]'), True),
        (interval(5, 4, '[)'), True),
        (interval(5, 4, '(]'), True),
        (interval(5, 4, '()'), True),
        (interval(None, 6, '[]'), False),
        (interval(None, 6, '[)'), False),
        (interval(None, 6, '(]'), False),
        (interval(None, 6, '()'), False),
        (interval(5, None, '[]'), False),
        (interval(5, None, '[)'), False),
        (interval(5, None, '(]'), False),
        (interval(5, None, '()'), False),
        (interval(None, None, '[]'), False),
        (interval(None, None, '[)'), False),
        (interval(None, None, '(]'), False),
        (interval(None, None, '()'), False),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 34), '[]'), False),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 34), '[)'), False),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 34), '(]'), False),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 34), '()'), False),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 33), '[]'), False),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 33), '[)'), True),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 33), '(]'), True),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 33), '()'), True),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 32), '[]'), True),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 32), '[)'), True),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 32), '(]'), True),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 32), '()'), True),
    ))
    def test__interval_unit_empty__start_g_end(self, target, is_empty):
        """端点の指定次第で単レンジが空になることをテストする。
        """
        assert target.is_empty == is_empty
        if is_empty:
            assert interval(empty=True) == target
            assert target == interval(empty=True)
            assert not target
        else:
            assert interval(empty=True) != target
            assert target != interval(empty=True)
            assert target

    @pytest.mark.parametrize('interval1, interval2, interval_m', (
        # 単レンジ同士で一方の終点ともう一方の始点が一致するパターン
        (interval(5, 6, '[]'), interval(6, 7, '[]'), interval(5, 7, '[]')),
        (interval(5, 6, '[)'), interval(6, 7, '[]'), interval(5, 7, '[]')),
        (interval(5, 6, '(]'), interval(6, 7, '[]'), interval(5, 7, '(]')),
        (interval(5, 6, '()'), interval(6, 7, '[]'), interval(5, 7, '(]')),
        (interval(5, 6, '[]'), interval(6, 7, '[)'), interval(5, 7, '[)')),
        (interval(5, 6, '[)'), interval(6, 7, '[)'), interval(5, 7, '[)')),
        (interval(5, 6, '(]'), interval(6, 7, '[)'), interval(5, 7, '()')),
        (interval(5, 6, '()'), interval(6, 7, '[)'), interval(5, 7, '()')),
        (interval(5, 6, '[]'), interval(6, 7, '(]'), interval(5, 7, '[]')),
        (interval(5, 6, '[)'), interval(6, 7, '(]'), [interval(5, 6, '[)'), interval(6, 7, '(]')]),
        (interval(5, 6, '(]'), interval(6, 7, '(]'), interval(5, 7, '(]')),
        (interval(5, 6, '()'), interval(6, 7, '(]'), [interval(5, 6, '()'), interval(6, 7, '(]')]),
        (interval(5, 6, '[]'), interval(6, 7, '()'), interval(5, 7, '[)')),
        (interval(5, 6, '[)'), interval(6, 7, '()'), [interval(5, 6, '[)'), interval(6, 7, '()')]),
        (interval(5, 6, '(]'), interval(6, 7, '()'), interval(5, 7, '()')),
        (interval(5, 6, '()'), interval(6, 7, '()'), [interval(5, 6, '()'), interval(6, 7, '()')]),
        (interval(None, 6, '(]'), interval(6, 7, '[]'), interval(None, 7, '(]')),
        (interval(None, 6, '()'), interval(6, 7, '[]'), interval(None, 7, '(]')),
        (interval(None, 6, '(]'), interval(6, 7, '[)'), interval(None, 7, '()')),
        (interval(None, 6, '()'), interval(6, 7, '[)'), interval(None, 7, '()')),
        (interval(None, 6, '(]'), interval(6, 7, '(]'), interval(None, 7, '(]')),
        (interval(None, 6, '()'), interval(6, 7, '(]'), [interval(None, 6, '()'), interval(6, 7, '(]')]),
        (interval(None, 6, '(]'), interval(6, 7, '()'), interval(None, 7, '()')),
        (interval(None, 6, '()'), interval(6, 7, '()'), [interval(None, 6, '()'), interval(6, 7, '()')]),
        (interval(5, 6, '[]'), interval(6, None, '[)'), interval(5, None, '[)')),
        (interval(5, 6, '[)'), interval(6, None, '[)'), interval(5, None, '[)')),
        (interval(5, 6, '(]'), interval(6, None, '[)'), interval(5, None, '()')),
        (interval(5, 6, '()'), interval(6, None, '[)'), interval(5, None, '()')),
        (interval(5, 6, '[]'), interval(6, None, '()'), interval(5, None, '[)')),
        (interval(5, 6, '[)'), interval(6, None, '()'), [interval(5, 6, '[)'), interval(6, None, '()')]),
        (interval(5, 6, '(]'), interval(6, None, '()'), interval(5, None, '()')),
        (interval(5, 6, '()'), interval(6, None, '()'), [interval(5, 6, '()'), interval(6, None, '()')]),
        (interval(None, 6, '(]'), interval(6, None, '[)'), interval(None, None, '()')),
        (interval(None, 6, '()'), interval(6, None, '[)'), interval(None, None, '()')),
        (interval(None, 6, '(]'), interval(6, None, '()'), interval(None, None, '()')),
        (interval(None, 6, '()'), interval(6, None, '()'), [interval(None, 6, '()'), interval(6, None, '()')]),
        # 単レンジ同士で一方ともう一方に共通部分がないパターン
        (interval(5, 6, '[]'), interval(7, 8, '[]'), [interval(5, 6, '[]'), interval(7, 8, '[]')]),
        (interval(5, 6, '[)'), interval(7, 8, '[]'), [interval(5, 6, '[)'), interval(7, 8, '[]')]),
        (interval(5, 6, '(]'), interval(7, 8, '[]'), [interval(5, 6, '(]'), interval(7, 8, '[]')]),
        (interval(5, 6, '()'), interval(7, 8, '[]'), [interval(5, 6, '()'), interval(7, 8, '[]')]),
        (interval(5, 6, '[]'), interval(7, 8, '[)'), [interval(5, 6, '[]'), interval(7, 8, '[)')]),
        (interval(5, 6, '[)'), interval(7, 8, '[)'), [interval(5, 6, '[)'), interval(7, 8, '[)')]),
        (interval(5, 6, '(]'), interval(7, 8, '[)'), [interval(5, 6, '(]'), interval(7, 8, '[)')]),
        (interval(5, 6, '()'), interval(7, 8, '[)'), [interval(5, 6, '()'), interval(7, 8, '[)')]),
        (interval(5, 6, '[]'), interval(7, 8, '(]'), [interval(5, 6, '[]'), interval(7, 8, '(]')]),
        (interval(5, 6, '[)'), interval(7, 8, '(]'), [interval(5, 6, '[)'), interval(7, 8, '(]')]),
        (interval(5, 6, '(]'), interval(7, 8, '(]'), [interval(5, 6, '(]'), interval(7, 8, '(]')]),
        (interval(5, 6, '()'), interval(7, 8, '(]'), [interval(5, 6, '()'), interval(7, 8, '(]')]),
        (interval(5, 6, '[]'), interval(7, 8, '()'), [interval(5, 6, '[]'), interval(7, 8, '()')]),
        (interval(5, 6, '[)'), interval(7, 8, '()'), [interval(5, 6, '[)'), interval(7, 8, '()')]),
        (interval(5, 6, '(]'), interval(7, 8, '()'), [interval(5, 6, '(]'), interval(7, 8, '()')]),
        (interval(5, 6, '()'), interval(7, 8, '()'), [interval(5, 6, '()'), interval(7, 8, '()')]),
        (interval(None, 6, '(]'), interval(7, 8, '[]'), [interval(None, 6, '(]'), interval(7, 8, '[]')]),
        (interval(None, 6, '()'), interval(7, 8, '[]'), [interval(None, 6, '()'), interval(7, 8, '[]')]),
        (interval(None, 6, '(]'), interval(7, 8, '[)'), [interval(None, 6, '(]'), interval(7, 8, '[)')]),
        (interval(None, 6, '()'), interval(7, 8, '[)'), [interval(None, 6, '()'), interval(7, 8, '[)')]),
        (interval(None, 6, '(]'), interval(7, 8, '(]'), [interval(None, 6, '(]'), interval(7, 8, '(]')]),
        (interval(None, 6, '()'), interval(7, 8, '(]'), [interval(None, 6, '()'), interval(7, 8, '(]')]),
        (interval(None, 6, '(]'), interval(7, 8, '()'), [interval(None, 6, '(]'), interval(7, 8, '()')]),
        (interval(None, 6, '()'), interval(7, 8, '()'), [interval(None, 6, '()'), interval(7, 8, '()')]),
        (interval(5, 6, '[]'), interval(7, None, '[)'), [interval(5, 6, '[]'), interval(7, None, '[)')]),
        (interval(5, 6, '[)'), interval(7, None, '[)'), [interval(5, 6, '[)'), interval(7, None, '[)')]),
        (interval(5, 6, '(]'), interval(7, None, '[)'), [interval(5, 6, '(]'), interval(7, None, '[)')]),
        (interval(5, 6, '()'), interval(7, None, '[)'), [interval(5, 6, '()'), interval(7, None, '[)')]),
        (interval(5, 6, '[]'), interval(7, None, '()'), [interval(5, 6, '[]'), interval(7, None, '()')]),
        (interval(5, 6, '[)'), interval(7, None, '()'), [interval(5, 6, '[)'), interval(7, None, '()')]),
        (interval(5, 6, '(]'), interval(7, None, '()'), [interval(5, 6, '(]'), interval(7, None, '()')]),
        (interval(5, 6, '()'), interval(7, None, '()'), [interval(5, 6, '()'), interval(7, None, '()')]),
        (interval(None, 6, '(]'), interval(7, None, '[)'), [interval(None, 6, '(]'), interval(7, None, '[)')]),
        (interval(None, 6, '()'), interval(7, None, '[)'), [interval(None, 6, '()'), interval(7, None, '[)')]),
        (interval(None, 6, '(]'), interval(7, None, '()'), [interval(None, 6, '(]'), interval(7, None, '()')]),
        (interval(None, 6, '()'), interval(7, None, '()'), [interval(None, 6, '()'), interval(7, None, '()')]),
        # 単レンジ同士で一方ともう一方にシングルトンでない共通部分があるパターン
        (interval(5, 7, '[]'), interval(6, 8, '[]'), interval(5, 8, '[]')),
        (interval(5, 7, '[)'), interval(6, 8, '[]'), interval(5, 8, '[]')),
        (interval(5, 7, '(]'), interval(6, 8, '[]'), interval(5, 8, '(]')),
        (interval(5, 7, '()'), interval(6, 8, '[]'), interval(5, 8, '(]')),
        (interval(5, 7, '[]'), interval(6, 8, '[)'), interval(5, 8, '[)')),
        (interval(5, 7, '[)'), interval(6, 8, '[)'), interval(5, 8, '[)')),
        (interval(5, 7, '(]'), interval(6, 8, '[)'), interval(5, 8, '()')),
        (interval(5, 7, '()'), interval(6, 8, '[)'), interval(5, 8, '()')),
        (interval(5, 7, '[]'), interval(6, 8, '(]'), interval(5, 8, '[]')),
        (interval(5, 7, '[)'), interval(6, 8, '(]'), interval(5, 8, '[]')),
        (interval(5, 7, '(]'), interval(6, 8, '(]'), interval(5, 8, '(]')),
        (interval(5, 7, '()'), interval(6, 8, '(]'), interval(5, 8, '(]')),
        (interval(5, 7, '[]'), interval(6, 8, '()'), interval(5, 8, '[)')),
        (interval(5, 7, '[)'), interval(6, 8, '()'), interval(5, 8, '[)')),
        (interval(5, 7, '(]'), interval(6, 8, '()'), interval(5, 8, '()')),
        (interval(5, 7, '()'), interval(6, 8, '()'), interval(5, 8, '()')),
        (interval(None, 7, '(]'), interval(6, 8, '[]'), interval(None, 8, '(]')),
        (interval(None, 7, '()'), interval(6, 8, '[]'), interval(None, 8, '(]')),
        (interval(None, 7, '(]'), interval(6, 8, '[)'), interval(None, 8, '()')),
        (interval(None, 7, '()'), interval(6, 8, '[)'), interval(None, 8, '()')),
        (interval(None, 7, '(]'), interval(6, 8, '(]'), interval(None, 8, '(]')),
        (interval(None, 7, '()'), interval(6, 8, '(]'), interval(None, 8, '(]')),
        (interval(None, 7, '(]'), interval(6, 8, '()'), interval(None, 8, '()')),
        (interval(None, 7, '()'), interval(6, 8, '()'), interval(None, 8, '()')),
        (interval(5, None, '[)'), interval(6, 8, '[]'), interval(5, None, '[)')),
        (interval(5, None, '()'), interval(6, 8, '[]'), interval(5, None, '()')),
        (interval(5, None, '[)'), interval(6, 8, '[)'), interval(5, None, '[)')),
        (interval(5, None, '()'), interval(6, 8, '[)'), interval(5, None, '()')),
        (interval(5, None, '[)'), interval(6, 8, '(]'), interval(5, None, '[)')),
        (interval(5, None, '()'), interval(6, 8, '(]'), interval(5, None, '()')),
        (interval(5, None, '[)'), interval(6, 8, '()'), interval(5, None, '[)')),
        (interval(5, None, '()'), interval(6, 8, '()'), interval(5, None, '()')),
        # 一方が空のパターン
        (interval(5, 6, '[]'), interval(empty=True), interval(5, 6, '[]')),
        (interval(None, 6, '(]'), interval(empty=True), interval(None, 6, '(]')),
        (interval(5, None, '[)'), interval(empty=True), interval(5, None, '[)')),
        (interval(None, None, '()'), interval(empty=True), interval(None, None, '()')),
        (interval(empty=True), interval(empty=True), interval(empty=True)),
        # 一方が単レンジでないパターン
        (interval(4, 6, '[]') + interval(8, 10, '[]'), interval(3, 5, '[]'),
         [interval(3, 6, '[]'), interval(8, 10, '[]')]),
        (interval(4, 6, '[)') + interval(8, 10, '[]'), interval(3, 5, '[]'),
         [interval(3, 6, '[)'), interval(8, 10, '[]')]),
        (interval(4, 6, '(]') + interval(8, 10, '[]'), interval(3, 5, '[]'),
         [interval(3, 6, '[]'), interval(8, 10, '[]')]),
        (interval(4, 6, '()') + interval(8, 10, '[]'), interval(3, 5, '[]'),
         [interval(3, 6, '[)'), interval(8, 10, '[]')]),
        (interval(4, 6, '[]') + interval(8, 10, '[]'), interval(3, 5, '[)'),
         [interval(3, 6, '[]'), interval(8, 10, '[]')]),
        (interval(4, 6, '[)') + interval(8, 10, '[]'), interval(3, 5, '[)'),
         [interval(3, 6, '[)'), interval(8, 10, '[]')]),
        (interval(4, 6, '(]') + interval(8, 10, '[]'), interval(3, 5, '[)'),
         [interval(3, 6, '[]'), interval(8, 10, '[]')]),
        (interval(4, 6, '()') + interval(8, 10, '[]'), interval(3, 5, '[)'),
         [interval(3, 6, '[)'), interval(8, 10, '[]')]),
        (interval(4, 6, '[]') + interval(8, 10, '[]'), interval(3, 5, '(]'),
         [interval(3, 6, '(]'), interval(8, 10, '[]')]),
        (interval(4, 6, '[)') + interval(8, 10, '[]'), interval(3, 5, '(]'),
         [interval(3, 6, '()'), interval(8, 10, '[]')]),
        (interval(4, 6, '(]') + interval(8, 10, '[]'), interval(3, 5, '(]'),
         [interval(3, 6, '(]'), interval(8, 10, '[]')]),
        (interval(4, 6, '()') + interval(8, 10, '[]'), interval(3, 5, '(]'),
         [interval(3, 6, '()'), interval(8, 10, '[]')]),
        (interval(4, 6, '[]') + interval(8, 10, '[]'), interval(3, 5, '()'),
         [interval(3, 6, '(]'), interval(8, 10, '[]')]),
        (interval(4, 6, '[)') + interval(8, 10, '[]'), interval(3, 5, '()'),
         [interval(3, 6, '()'), interval(8, 10, '[]')]),
        (interval(4, 6, '(]') + interval(8, 10, '[]'), interval(3, 5, '()'),
         [interval(3, 6, '(]'), interval(8, 10, '[]')]),
        (interval(4, 6, '()') + interval(8, 10, '[]'), interval(3, 5, '()'),
         [interval(3, 6, '()'), interval(8, 10, '[]')]),
        # 一方が単レンジでないパターン
        (interval(4, 6, '[]') + interval(8, 10, '[]'), interval(6, 8, '[]'), interval(4, 10, '[]')),
        (interval(4, 6, '[]') + interval(8, 10, '[]'), interval(6, 8, '[)'), interval(4, 10, '[]')),
        (interval(4, 6, '[]') + interval(8, 10, '[]'), interval(6, 8, '(]'), interval(4, 10, '[]')),
        (interval(4, 6, '[]') + interval(8, 10, '[]'), interval(6, 8, '()'), interval(4, 10, '[]')),
        (interval(4, 6, '[)') + interval(8, 10, '[]'), interval(6, 8, '[]'), interval(4, 10, '[]')),
        (interval(4, 6, '[)') + interval(8, 10, '[]'), interval(6, 8, '[)'), interval(4, 10, '[]')),
        (interval(4, 6, '[)') + interval(8, 10, '[]'), interval(6, 8, '(]'),
         [interval(4, 6, '[)'), interval(6, 10, '(]')]),
        (interval(4, 6, '[)') + interval(8, 10, '[]'), interval(6, 8, '()'),
         [interval(4, 6, '[)'), interval(6, 10, '(]')]),
        (interval(4, 6, '(]') + interval(8, 10, '[]'), interval(6, 8, '[]'), interval(4, 10, '(]')),
        (interval(4, 6, '(]') + interval(8, 10, '[]'), interval(6, 8, '[)'), interval(4, 10, '(]')),
        (interval(4, 6, '(]') + interval(8, 10, '[]'), interval(6, 8, '(]'), interval(4, 10, '(]')),
        (interval(4, 6, '(]') + interval(8, 10, '[]'), interval(6, 8, '()'), interval(4, 10, '(]')),
        (interval(4, 6, '()') + interval(8, 10, '[]'), interval(6, 8, '[]'), interval(4, 10, '(]')),
        (interval(4, 6, '()') + interval(8, 10, '[]'), interval(6, 8, '[)'), interval(4, 10, '(]')),
        (interval(4, 6, '()') + interval(8, 10, '[]'), interval(6, 8, '(]'),
         [interval(4, 6, '()'), interval(6, 10, '(]')]),
        (interval(4, 6, '()') + interval(8, 10, '[]'), interval(6, 8, '()'),
         [interval(4, 6, '()'), interval(6, 10, '(]')]),
        (interval(4, 6, '[]') + interval(8, 10, '[)'), interval(6, 8, '[]'), interval(4, 10, '[)')),
        (interval(4, 6, '[]') + interval(8, 10, '[)'), interval(6, 8, '[)'), interval(4, 10, '[)')),
        (interval(4, 6, '[]') + interval(8, 10, '[)'), interval(6, 8, '(]'), interval(4, 10, '[)')),
        (interval(4, 6, '[]') + interval(8, 10, '[)'), interval(6, 8, '()'), interval(4, 10, '[)')),
        (interval(4, 6, '[)') + interval(8, 10, '[)'), interval(6, 8, '[]'), interval(4, 10, '[)')),
        (interval(4, 6, '[)') + interval(8, 10, '[)'), interval(6, 8, '[)'), interval(4, 10, '[)')),
        (interval(4, 6, '[)') + interval(8, 10, '[)'), interval(6, 8, '(]'),
         [interval(4, 6, '[)'), interval(6, 10, '()')]),
        (interval(4, 6, '[)') + interval(8, 10, '[)'), interval(6, 8, '()'),
         [interval(4, 6, '[)'), interval(6, 10, '()')]),
        (interval(4, 6, '(]') + interval(8, 10, '[)'), interval(6, 8, '[]'), interval(4, 10, '()')),
        (interval(4, 6, '(]') + interval(8, 10, '[)'), interval(6, 8, '[)'), interval(4, 10, '()')),
        (interval(4, 6, '(]') + interval(8, 10, '[)'), interval(6, 8, '(]'), interval(4, 10, '()')),
        (interval(4, 6, '(]') + interval(8, 10, '[)'), interval(6, 8, '()'), interval(4, 10, '()')),
        (interval(4, 6, '()') + interval(8, 10, '[)'), interval(6, 8, '[]'), interval(4, 10, '()')),
        (interval(4, 6, '()') + interval(8, 10, '[)'), interval(6, 8, '[)'), interval(4, 10, '()')),
        (interval(4, 6, '()') + interval(8, 10, '[)'), interval(6, 8, '(]'),
         [interval(4, 6, '()'), interval(6, 10, '()')]),
        (interval(4, 6, '()') + interval(8, 10, '[)'), interval(6, 8, '()'),
         [interval(4, 6, '()'), interval(6, 10, '()')]),
        (interval(4, 6, '[]') + interval(8, 10, '(]'), interval(6, 8, '[]'), interval(4, 10, '[]')),
        (interval(4, 6, '[]') + interval(8, 10, '(]'), interval(6, 8, '[)'),
         [interval(4, 8, '[)'), interval(8, 10, '(]')]),
        (interval(4, 6, '[]') + interval(8, 10, '(]'), interval(6, 8, '(]'), interval(4, 10, '[]')),
        (interval(4, 6, '[]') + interval(8, 10, '(]'), interval(6, 8, '()'),
         [interval(4, 8, '[)'), interval(8, 10, '(]')]),
        (interval(4, 6, '[)') + interval(8, 10, '(]'), interval(6, 8, '[]'), interval(4, 10, '[]')),
        (interval(4, 6, '[)') + interval(8, 10, '(]'), interval(6, 8, '[)'),
         [interval(4, 8, '[)'), interval(8, 10, '(]')]),
        (interval(4, 6, '[)') + interval(8, 10, '(]'), interval(6, 8, '(]'),
         [interval(4, 6, '[)'), interval(6, 10, '(]')]),
        (interval(4, 6, '[)') + interval(8, 10, '(]'), interval(6, 8, '()'),
         [interval(4, 6, '[)'), interval(6, 8, '()'), interval(8, 10, '(]')]),
        (interval(4, 6, '(]') + interval(8, 10, '(]'), interval(6, 8, '[]'), interval(4, 10, '(]')),
        (interval(4, 6, '(]') + interval(8, 10, '(]'), interval(6, 8, '[)'),
         [interval(4, 8, '()'), interval(8, 10, '(]')]),
        (interval(4, 6, '(]') + interval(8, 10, '(]'), interval(6, 8, '(]'), interval(4, 10, '(]')),
        (interval(4, 6, '(]') + interval(8, 10, '(]'), interval(6, 8, '()'),
         [interval(4, 8, '()'), interval(8, 10, '(]')]),
        (interval(4, 6, '()') + interval(8, 10, '(]'), interval(6, 8, '[]'), interval(4, 10, '(]')),
        (interval(4, 6, '()') + interval(8, 10, '(]'), interval(6, 8, '[)'),
         [interval(4, 8, '()'), interval(8, 10, '(]')]),
        (interval(4, 6, '()') + interval(8, 10, '(]'), interval(6, 8, '(]'),
         [interval(4, 6, '()'), interval(6, 10, '(]')]),
        (interval(4, 6, '()') + interval(8, 10, '(]'), interval(6, 8, '()'),
         [interval(4, 6, '()'), interval(6, 8, '()'), interval(8, 10, '(]')]),
        (interval(4, 6, '[]') + interval(8, 10, '()'), interval(6, 8, '[]'), interval(4, 10, '[)')),
        (interval(4, 6, '[]') + interval(8, 10, '()'), interval(6, 8, '[)'),
         [interval(4, 8, '[)'), interval(8, 10, '()')]),
        (interval(4, 6, '[]') + interval(8, 10, '()'), interval(6, 8, '(]'), interval(4, 10, '[)')),
        (interval(4, 6, '[]') + interval(8, 10, '()'), interval(6, 8, '()'),
         [interval(4, 8, '[)'), interval(8, 10, '()')]),
        (interval(4, 6, '[)') + interval(8, 10, '()'), interval(6, 8, '[]'), interval(4, 10, '[)')),
        (interval(4, 6, '[)') + interval(8, 10, '()'), interval(6, 8, '[)'),
         [interval(4, 8, '[)'), interval(8, 10, '()')]),
        (interval(4, 6, '[)') + interval(8, 10, '()'), interval(6, 8, '(]'),
         [interval(4, 6, '[)'), interval(6, 10, '()')]),
        (interval(4, 6, '[)') + interval(8, 10, '()'), interval(6, 8, '()'),
         [interval(4, 6, '[)'), interval(6, 8, '()'), interval(8, 10, '()')]),
        (interval(4, 6, '(]') + interval(8, 10, '()'), interval(6, 8, '[]'), interval(4, 10, '()')),
        (interval(4, 6, '(]') + interval(8, 10, '()'), interval(6, 8, '[)'),
         [interval(4, 8, '()'), interval(8, 10, '()')]),
        (interval(4, 6, '(]') + interval(8, 10, '()'), interval(6, 8, '(]'), interval(4, 10, '()')),
        (interval(4, 6, '(]') + interval(8, 10, '()'), interval(6, 8, '()'),
         [interval(4, 8, '()'), interval(8, 10, '()')]),
        (interval(4, 6, '()') + interval(8, 10, '()'), interval(6, 8, '[]'), interval(4, 10, '()')),
        (interval(4, 6, '()') + interval(8, 10, '()'), interval(6, 8, '[)'),
         [interval(4, 8, '()'), interval(8, 10, '()')]),
        (interval(4, 6, '()') + interval(8, 10, '()'), interval(6, 8, '(]'),
         [interval(4, 6, '()'), interval(6, 10, '()')]),
        (interval(4, 6, '()') + interval(8, 10, '()'), interval(6, 8, '()'),
         [interval(4, 6, '()'), interval(6, 8, '()'), interval(8, 10, '()')]),

        (interval(4, 6, '[]') + interval(8, 10, '[]') + interval(12, 14, '[]'), interval(6, 12, '[]'),
         interval(4, 14, '[]')),
        # 双方が単レンジでないパターン
        (interval(4, 6, '[]') + interval(8, 10, '[]'), interval(7, 7, '[]') + interval(11, 12, '[]'),
         [interval(4, 6, '[]'), interval(7, 7, '[]'), interval(8, 10, '[]'), interval(11, 12, '[]')]),
        (interval(4, 6, '[]') + interval(8, 10, '[]'), interval(5, 7, '[]') + interval(11, 12, '[]'),
         [interval(4, 7, '[]'), interval(8, 10, '[]'), interval(11, 12, '[]')]),
        (interval(1, 6, '[]') + interval(8, 10, '[]'), interval(2, 3, '[]') + interval(4, 5, '[]'),
         [interval(1, 6, '[]'), interval(8, 10, '[]')]),
        (interval(1, 6, '[]') + interval(8, 10, '[]'), interval(2, 3, '[]') + interval(4, 7, '[]'),
         [interval(1, 7, '[]'), interval(8, 10, '[]')]),
    ))
    def test__interval_unit_int__add__unit(self, interval1, interval2, interval_m):
        """レンジ[int]()の加法演算 (合併) をテストする。
        """
        if isinstance(interval_m, list):
            result = interval2 + interval1
            assert not result.is_empty
            assert result._unit_list == interval_m

            result = interval1 + interval2
            assert not result.is_empty
            assert result._unit_list == interval_m
        else:
            result = interval2 + interval1
            assert result == interval_m

            result = interval1 + interval2
            assert result == interval_m

    @pytest.mark.parametrize('interval1, interval2, interval_r', (
        # interval1 を2つに分割するパターン
        (interval(1, 10, edge='[)'), interval(5, 6, edge='[]'), interval(1, 5, edge='[)') + interval(6, 10, edge='()')),
        (interval(1, 10, edge='[)'), interval(5, 6, edge='[)'), interval(1, 5, edge='[)') + interval(6, 10, edge='[)')),
        (interval(1, 10, edge='[)'), interval(5, 6, edge='(]'), interval(1, 5, edge='[]') + interval(6, 10, edge='()')),
        (interval(1, 10, edge='[)'), interval(5, 6, edge='()'), interval(1, 5, edge='[]') + interval(6, 10, edge='[)')),
        (interval(1, 10, edge='[)'), interval(singleton=5), interval(1, 5, edge='[)') + interval(5, 10, edge='()')),
        # interval1 の左側が削られるパターン
        (interval(1, 10, edge='[)'), interval(0, 6, edge='[]'), interval(6, 10, edge='()')),
        (interval(1, 10, edge='[)'), interval(0, 6, edge='[)'), interval(6, 10, edge='[)')),
        # interval1 の右側が削られるパターン
        (interval(1, 10, edge='[)'), interval(5, 20, edge='[]'), interval(1, 5, edge='[)')),
        (interval(1, 10, edge='[)'), interval(5, 20, edge='(]'), interval(1, 5, edge='[]')),
        # 2つのオペランドの両端が一致するパターン
        (interval(1, 10, edge='[]'), interval(1, 10, edge='[]'), interval(empty=True)),
        (interval(1, 10, edge='[]'), interval(1, 10, edge='[)'), interval(singleton=10)),
        (interval(1, 10, edge='[]'), interval(1, 10, edge='(]'), interval(singleton=1)),
        (interval(1, 10, edge='[]'), interval(1, 10, edge='()'), interval(singleton=1) + interval(singleton=10)),
        # オペランドの一方が空であるパターン
        (interval(1, 10, edge='[]'), interval(empty=True), interval(1, 10, edge='[]')),
        (interval(1, 10, edge='[)'), interval(empty=True), interval(1, 10, edge='[)')),
        (interval(1, 10, edge='(]'), interval(empty=True), interval(1, 10, edge='(]')),
        (interval(1, 10, edge='()'), interval(empty=True), interval(1, 10, edge='()')),
        (interval(empty=True), interval(1, 10, edge='[]'), interval(empty=True)),
        (interval(empty=True), interval(1, 10, edge='[)'), interval(empty=True)),
        (interval(empty=True), interval(1, 10, edge='(]'), interval(empty=True)),
        (interval(empty=True), interval(1, 10, edge='()'), interval(empty=True)),
        # 右オペランドが有界でない場合
        (interval(1, 10, edge='[]'), interval(5, None, edge='[)'), interval(1, 5, edge='[)')),
        (interval(1, 10, edge='[]'), interval(None, 5, edge='(]'), interval(5, 10, edge='(]')),
        (interval(1, 10, edge='[]'), interval(None, None), interval(empty=True)),
        # 他
        (interval(1, 2) + interval(3, 4), interval(1.5, 1.7) + interval(1.9, 3.5),
         interval(1.0, 1.5) + interval(1.7, 2.0) + interval(3.5, 4.0)),

    ))
    def test__interval_unit_int__sub__unit(self, interval1, interval2, interval_r):
        """レンジ[int]()の減法演算 (差集合) をテストする。
        """
        assert interval1 - interval2 == interval_r

    @pytest.mark.parametrize('interval1, interval2, interval_m', (
        # 一方が他方を包含するパターン
        (interval(5, 10, '[]'), interval(7, 9, '[]'), interval(7, 9, '[]')),
        (interval(5, 10, '[)'), interval(7, 9, '[]'), interval(7, 9, '[]')),
        (interval(5, 10, '(]'), interval(7, 9, '[]'), interval(7, 9, '[]')),
        (interval(5, 10, '()'), interval(7, 9, '[]'), interval(7, 9, '[]')),
        (interval(5, 10, '[]'), interval(7, 9, '[)'), interval(7, 9, '[)')),
        (interval(5, 10, '[)'), interval(7, 9, '[)'), interval(7, 9, '[)')),
        (interval(5, 10, '(]'), interval(7, 9, '[)'), interval(7, 9, '[)')),
        (interval(5, 10, '()'), interval(7, 9, '[)'), interval(7, 9, '[)')),
        (interval(5, 10, '[]'), interval(7, 9, '(]'), interval(7, 9, '(]')),
        (interval(5, 10, '[)'), interval(7, 9, '(]'), interval(7, 9, '(]')),
        (interval(5, 10, '(]'), interval(7, 9, '(]'), interval(7, 9, '(]')),
        (interval(5, 10, '()'), interval(7, 9, '(]'), interval(7, 9, '(]')),
        (interval(5, 10, '[]'), interval(7, 9, '()'), interval(7, 9, '()')),
        (interval(5, 10, '[)'), interval(7, 9, '()'), interval(7, 9, '()')),
        (interval(5, 10, '(]'), interval(7, 9, '()'), interval(7, 9, '()')),
        (interval(5, 10, '()'), interval(7, 9, '()'), interval(7, 9, '()')),
        (interval(None, 10, '(]'), interval(7, 9, '[]'), interval(7, 9, '[]')),
        (interval(None, 10, '()'), interval(7, 9, '[]'), interval(7, 9, '[]')),
        (interval(None, 10, '(]'), interval(7, 9, '[)'), interval(7, 9, '[)')),
        (interval(None, 10, '()'), interval(7, 9, '[)'), interval(7, 9, '[)')),
        (interval(None, 10, '(]'), interval(7, 9, '(]'), interval(7, 9, '(]')),
        (interval(None, 10, '()'), interval(7, 9, '(]'), interval(7, 9, '(]')),
        (interval(None, 10, '(]'), interval(7, 9, '()'), interval(7, 9, '()')),
        (interval(None, 10, '()'), interval(7, 9, '()'), interval(7, 9, '()')),
        (interval(5, None, '[)'), interval(7, 9, '[]'), interval(7, 9, '[]')),
        (interval(5, None, '()'), interval(7, 9, '[]'), interval(7, 9, '[]')),
        (interval(5, None, '[)'), interval(7, 9, '[)'), interval(7, 9, '[)')),
        (interval(5, None, '()'), interval(7, 9, '[)'), interval(7, 9, '[)')),
        (interval(5, None, '[)'), interval(7, 9, '(]'), interval(7, 9, '(]')),
        (interval(5, None, '()'), interval(7, 9, '(]'), interval(7, 9, '(]')),
        (interval(5, None, '[)'), interval(7, 9, '()'), interval(7, 9, '()')),
        (interval(5, None, '()'), interval(7, 9, '()'), interval(7, 9, '()')),
        (interval(None, None, '()'), interval(7, 9, '[]'), interval(7, 9, '[]')),
        (interval(None, None, '()'), interval(7, 9, '[)'), interval(7, 9, '[)')),
        (interval(None, None, '()'), interval(7, 9, '(]'), interval(7, 9, '(]')),
        (interval(None, None, '()'), interval(7, 9, '()'), interval(7, 9, '()')),
        # 共通部分が無いパターン (ただしオペランドが空の単レンジでない)
        (interval(5, 6, '[]'), interval(7, 9, '[]'), interval(empty=True)),
        (interval(5, 6, '[)'), interval(7, 9, '[]'), interval(empty=True)),
        (interval(5, 6, '(]'), interval(7, 9, '[]'), interval(empty=True)),
        (interval(5, 6, '()'), interval(7, 9, '[]'), interval(empty=True)),
        (interval(5, 6, '[]'), interval(7, 9, '[)'), interval(empty=True)),
        (interval(5, 6, '[)'), interval(7, 9, '[)'), interval(empty=True)),
        (interval(5, 6, '(]'), interval(7, 9, '[)'), interval(empty=True)),
        (interval(5, 6, '()'), interval(7, 9, '[)'), interval(empty=True)),
        (interval(5, 6, '[]'), interval(7, 9, '(]'), interval(empty=True)),
        (interval(5, 6, '[)'), interval(7, 9, '(]'), interval(empty=True)),
        (interval(5, 6, '(]'), interval(7, 9, '(]'), interval(empty=True)),
        (interval(5, 6, '()'), interval(7, 9, '(]'), interval(empty=True)),
        (interval(5, 6, '[]'), interval(7, 9, '()'), interval(empty=True)),
        (interval(5, 6, '[)'), interval(7, 9, '()'), interval(empty=True)),
        (interval(5, 6, '(]'), interval(7, 9, '()'), interval(empty=True)),
        (interval(5, 6, '()'), interval(7, 9, '()'), interval(empty=True)),
        (interval(None, 6, '(]'), interval(7, 9, '[]'), interval(empty=True)),
        (interval(None, 6, '()'), interval(7, 9, '[]'), interval(empty=True)),
        (interval(None, 6, '(]'), interval(7, 9, '[)'), interval(empty=True)),
        (interval(None, 6, '()'), interval(7, 9, '[)'), interval(empty=True)),
        (interval(None, 6, '(]'), interval(7, 9, '(]'), interval(empty=True)),
        (interval(None, 6, '()'), interval(7, 9, '(]'), interval(empty=True)),
        (interval(None, 6, '(]'), interval(7, 9, '()'), interval(empty=True)),
        (interval(None, 6, '()'), interval(7, 9, '()'), interval(empty=True)),
        (interval(5, 6, '[]'), interval(7, None, '[)'), interval(empty=True)),
        (interval(5, 6, '[)'), interval(7, None, '[)'), interval(empty=True)),
        (interval(5, 6, '(]'), interval(7, None, '[)'), interval(empty=True)),
        (interval(5, 6, '()'), interval(7, None, '[)'), interval(empty=True)),
        (interval(5, 6, '[]'), interval(7, None, '()'), interval(empty=True)),
        (interval(5, 6, '[)'), interval(7, None, '()'), interval(empty=True)),
        (interval(5, 6, '(]'), interval(7, None, '()'), interval(empty=True)),
        (interval(5, 6, '()'), interval(7, None, '()'), interval(empty=True)),
        (interval(None, 6, '(]'), interval(7, None, '[)'), interval(empty=True)),
        (interval(None, 6, '()'), interval(7, None, '[)'), interval(empty=True)),
        (interval(None, 6, '(]'), interval(7, None, '()'), interval(empty=True)),
        (interval(None, 6, '()'), interval(7, None, '()'), interval(empty=True)),
        # 少なくとも一方が空の単レンジであるパターン
        (interval(empty=True), interval(7, 9, '[]'), interval(empty=True)),
        (interval(empty=True), interval(7, 9, '[)'), interval(empty=True)),
        (interval(empty=True), interval(7, 9, '(]'), interval(empty=True)),
        (interval(empty=True), interval(7, 9, '()'), interval(empty=True)),
        (interval(empty=True), interval(empty=True), interval(empty=True)),
        (interval(empty=True), interval(None, 9, '(]'), interval(empty=True)),
        (interval(empty=True), interval(None, 9, '()'), interval(empty=True)),
        (interval(empty=True), interval(7, None, '[)'), interval(empty=True)),
        (interval(empty=True), interval(7, None, '()'), interval(empty=True)),
        # 共通部分があり、それがいずれのオペランドとも一致しないパターン
        (interval(5, 9, '[]'), interval(7, 12, '[]'), interval(7, 9, '[]')),
        (interval(5, 9, '[)'), interval(7, 12, '[]'), interval(7, 9, '[)')),
        (interval(5, 9, '(]'), interval(7, 12, '[]'), interval(7, 9, '[]')),
        (interval(5, 9, '()'), interval(7, 12, '[]'), interval(7, 9, '[)')),
        (interval(5, 9, '[]'), interval(7, 12, '[)'), interval(7, 9, '[]')),
        (interval(5, 9, '[)'), interval(7, 12, '[)'), interval(7, 9, '[)')),
        (interval(5, 9, '(]'), interval(7, 12, '[)'), interval(7, 9, '[]')),
        (interval(5, 9, '()'), interval(7, 12, '[)'), interval(7, 9, '[)')),
        (interval(5, 9, '[]'), interval(7, 12, '(]'), interval(7, 9, '(]')),
        (interval(5, 9, '[)'), interval(7, 12, '(]'), interval(7, 9, '()')),
        (interval(5, 9, '(]'), interval(7, 12, '(]'), interval(7, 9, '(]')),
        (interval(5, 9, '()'), interval(7, 12, '(]'), interval(7, 9, '()')),
        (interval(5, 9, '[]'), interval(7, 12, '()'), interval(7, 9, '(]')),
        (interval(5, 9, '[)'), interval(7, 12, '()'), interval(7, 9, '()')),
        (interval(5, 9, '(]'), interval(7, 12, '()'), interval(7, 9, '(]')),
        (interval(5, 9, '()'), interval(7, 12, '()'), interval(7, 9, '()')),
        # 共通部分がシングルトンであるパターン
        (interval(5, 9, '(]'), interval(9, 12, '[)'), interval(9, 9, '[]')),
        (interval(5, 9, '[]'), interval(9, 12, '[)'), interval(9, 9, '[]')),
        (interval(5, 9, '(]'), interval(9, 12, '[]'), interval(9, 9, '[]')),
        (interval(5, 9, '[]'), interval(9, 12, '[]'), interval(9, 9, '[]')),
        # オペランドが単レンジでない場合
        (interval(5, 10, '(]') + interval(15, 20, '[)'), interval(7, 8, '()') + interval(9, 18, '()'),
         interval(7, 8, '()') + interval(9, 10, '(]') + interval(15, 18, '[)')),
        (interval(5, 10, '(]') + interval(15, 20, '[)'), interval(empty=True), interval(empty=True)),
    ))
    def test__interval_unit_int__mul(self, interval1, interval2, interval_m):
        """レンジ[int]()の乗法演算 (交叉) をテストする。
        """
        assert interval1 * interval2 == interval_m
        assert interval2 * interval1 == interval_m

    @pytest.mark.parametrize('interval1, interval2, expected_issubset', (
        (interval(5, 10), interval(0, 20), True),
        (interval(5, 10), interval(5, 20), True),
        (interval(5, 10), interval(0, 10), True),
        (interval(5, 10), interval(5, 10), True),
        (interval(0, 10, '[]'), interval(0, 10, '[]'), True),
        (interval(0, 10, '(]'), interval(0, 10, '[]'), True),
        (interval(0, 10, '[)'), interval(0, 10, '[]'), True),
        (interval(0, 10, '()'), interval(0, 10, '[]'), True),
        (interval(0, 10, '[]'), interval(0, 10, '(]'), False),
        (interval(0, 10, '(]'), interval(0, 10, '(]'), True),
        (interval(0, 10, '[)'), interval(0, 10, '(]'), False),
        (interval(0, 10, '()'), interval(0, 10, '(]'), True),
        (interval(0, 10, '[]'), interval(0, 10, '[)'), False),
        (interval(0, 10, '(]'), interval(0, 10, '[)'), False),
        (interval(0, 10, '[)'), interval(0, 10, '[)'), True),
        (interval(0, 10, '()'), interval(0, 10, '[)'), True),
        (interval(0, 10, '[]'), interval(0, 10, '()'), False),
        (interval(0, 10, '(]'), interval(0, 10, '()'), False),
        (interval(0, 10, '[)'), interval(0, 10, '()'), False),
        (interval(0, 10, '()'), interval(0, 10, '()'), True),
        (interval(empty=True), interval(0, 10), True),
        (interval(0, 10), interval(empty=True), False),
        (interval(), interval(0, 10), False),
        (interval(0, 10), interval(), True),
        (interval(empty=True), interval(), True),
        (interval(), interval(empty=True), False),
        (interval(0, 10, '[]') + interval(20, 30), interval(0, 30, '[]'), True),
        (interval(0, 10, '[]') + interval(20, 30), interval(5, 25, '[]'), False),
        (interval(0, 10, '[]') + interval(20, 30), interval(0, 11) + interval(18, 35), True),
        (interval(0, 10, '[]') + interval(20, 30), interval(0, 11) + interval(25, 27), False),
        (interval(0, 10, '[]') + interval(20, 30), interval(0, 9) + interval(18, 35), False),
    ))
    def test__interval_unit_int__issubset(self,
                                          interval1: UnionInterval, interval2: UnionInterval, expected_issubset: bool):
        """レンジ[int]()の包含判定をテストする。
        """
        if expected_issubset:
            assert interval1.issubset(interval2)
            assert interval2.issuperset(interval1)
            assert interval1 <= interval2
            assert interval2 >= interval1

            if interval1 == interval2:
                assert not interval1 < interval2
                assert not interval2 > interval1
            else:
                assert interval1 < interval2
                assert interval2 > interval1
        else:
            assert not interval1.issubset(interval2)
            assert not interval2.issuperset(interval1)
            assert not interval1 <= interval2
            assert not interval2 >= interval1
            assert not interval1 < interval2
            assert not interval2 > interval1

    @pytest.mark.parametrize('interval1, interval2', (
        (interval(1, 5, edge='[]'), interval(None, 1, edge='()') + interval(5, None, edge='()')),
        (interval(1, 5, edge='[)'), interval(None, 1, edge='()') + interval(5, None, edge='[)')),
        (interval(1, 5, edge='(]'), interval(None, 1, edge='(]') + interval(5, None, edge='()')),
        (interval(1, 5, edge='()'), interval(None, 1, edge='(]') + interval(5, None, edge='[)')),
        (interval(empty=True), interval(None, None)),
        (interval(1, 5, edge='[]') + interval(10, 15, edge='[]'),
         interval(None, 1, edge='()') + interval(5, 10, edge='()') + interval(15, None, edge='()')),
        (interval(1, 5, edge='[]') + interval(10, 15, edge='(]'),
         interval(None, 1, edge='()') + interval(5, 10, edge='(]') + interval(15, None, edge='()')),
        (interval(1, 5, edge='[)') + interval(10, 15, edge='[]'),
         interval(None, 1, edge='()') + interval(5, 10, edge='[)') + interval(15, None, edge='()')),
        (interval(1, 5, edge='[)') + interval(10, 15, edge='(]'),
         interval(None, 1, edge='()') + interval(5, 10, edge='[]') + interval(15, None, edge='()')),
        (interval(None, 5, edge='()') + interval(5, None, edge='()'), interval(5, 5, edge='[]')),
        (interval(1, 5, edge='()') + interval(5, None, edge='()'),
         interval(None, 1, edge='(]') + interval(5, 5, edge='[]')),
        (interval(None, 5, edge='()') + interval(5, 10, edge='()'),
         interval(5, 5, edge='[]') + interval(10, None, edge='[)')),
    ))
    def test__interval_unit_int__complement(self, interval1: UnionInterval, interval2: UnionInterval):
        """レンジ[int]()の補集合をテストする。
        """
        assert interval1.complement() == interval2
        assert interval2.complement() == interval1

    @pytest.mark.parametrize('interval1, bounded_below, bounded_above', (
        (interval(1, 5, edge='[]'), True, True),
        (interval(1, 5, edge='[)'), True, True),
        (interval(1, 5, edge='(]'), True, True),
        (interval(1, 5, edge='()'), True, True),
        (interval(None, 5, edge='()'), False, True),
        (interval(1, None, edge='()'), True, False),
        (interval(None, None, edge='()'), False, False),
        (interval(empty=True), True, True),
        (interval(1, 5, edge='[]') + interval(7, 10, edge='[]'), True, True),
        (interval(None, 5, edge='[]') + interval(7, 10, edge='[]'), False, True),
        (interval(1, 5, edge='[]') + interval(7, None, edge='[]'), True, False),
        (interval(None, 5, edge='[]') + interval(7, None, edge='[]'), False, False),
    ))
    def test__interval_unit_int__bound(self, interval1: UnionInterval, bounded_below, bounded_above):
        """レンジ[int]()の有界判定をテストする。
        """
        assert interval1.is_bounded_below() == bounded_below
        assert interval1.is_bounded_above() == bounded_above

    @pytest.mark.parametrize('interval1, measure', (
        (interval(1, 5, edge='[]'), 4),
        (interval(1, 5, edge='[)'), 4),
        (interval(1, 5, edge='(]'), 4),
        (interval(1, 5, edge='()'), 4),
        (interval(empty=True), 0),
        (interval(1, 5, edge='()') + interval(9, 11, edge='()'), 6),
        (interval(singleton=1), 0),
        (interval(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 34), '[]'), timedelta(seconds=1)),
        (interval(singleton=datetime(2020, 12, 30, 11, 22, 33)), timedelta(seconds=0)),
    ))
    def test__interval_unit__measure(self, interval1: UnionInterval, measure):
        """レンジ()の測度関数をテストする。
        """
        assert interval1.measure() == measure

    @pytest.mark.parametrize('zero', (
        0,
        0.0,
        timedelta(0),
    ))
    def test__interval_unit__measure__zero(self, zero):
        """空の interval の測度関数をテストする。
        """
        assert interval(empty=True).measure(zero=zero) == zero

    @pytest.mark.parametrize('interval1', (
            interval(1, None),
            interval(None, 5),
            interval(None, None),
            interval(1, 2) + interval(5, None),
            interval(None, 2) + interval(5, 10),
            interval(None, 2) + interval(5, None),
    ))
    def test__interval_unit__measure_err(self, interval1: UnionInterval):
        """レンジ()の測度関数をテストする。
        """
        with pytest.raises(ValueError):
            interval1.measure()

    @pytest.mark.parametrize('intervals', (
        tuple(),
        (interval(1, 3),),
        (interval(singleton=5),),
        (interval(1, 3), interval(5, 7)),
        (interval(1, 3), interval(5, 7), interval(10, 15)),
    ))
    def test__interval__iteration(self, intervals: Sequence[UnionInterval]):
        """UnionInterval の Iterableとしての挙動をテストする
        """
        interval1: UnionInterval = sum(intervals, interval(empty=True))
        assert isinstance(interval1, Iterable)
        assert list(interval1) == list(intervals)
        for i in range(len(intervals)):
            assert isinstance(interval1[i], UnionInterval)
            assert interval1[i] == intervals[i]
        for i in range(len(intervals)):
            assert isinstance(interval1[-i], UnionInterval)
            assert interval1[-i] == intervals[-i]
        if len(intervals) >= 2:
            interval2: UnionInterval = sum(intervals[1:], interval(empty=True))
            assert isinstance(interval1[1:], UnionInterval)
            assert interval1[1:] == interval2

    @pytest.mark.parametrize('interval1, is_interval', (
        (interval(empty=True), True),
        (interval(1, 5, edge='[]'), True),
        (interval(1, 5, edge='[)'), True),
        (interval(1, 5, edge='(]'), True),
        (interval(1, 5, edge='()'), True),
        (interval(1, None), True),
        (interval(None, 1), True),
        (interval(1, 3) + interval(3, 4), True),
        (interval(1, 2) + interval(3, 4), False),
        (interval(1, 2) + interval(3, 4) + interval(5, 6), False),
    ))
    def test__interval__is_interval(self, interval1: UnionInterval, is_interval: bool):
        """UnionInterval#is_interval のテスト
        """
        assert interval1.is_interval == is_interval

    @pytest.mark.parametrize('interval1, inf, sup, min_v, max_v', (
        (interval(empty=True), None, None, None, None),
        (interval(1, 5, edge='[]'), 1, 5, 1, 5),
        (interval(1, 5, edge='[)'), 1, 5, 1, None),
        (interval(1, 5, edge='(]'), 1, 5, None, 5),
        (interval(1, 5, edge='()'), 1, 5, None, None),
        (interval(1, None), 1, None, 1, None),
        (interval(None, 1), None, 1, None, None),
        (interval(None, None), None, None, None, None),
        (interval(1, 3) + interval(3, 4), 1, 4, 1, None),
        (interval(1, 2) + interval(3, 4), 1, 4, 1, None),
        (interval(1, 2) + interval(3, 4) + interval(5, 6), 1, 6, 1, None),
        (interval(1, 2, edge='[]') + interval(3, 4, edge='(]') + interval(5, 6, edge='()'), 1, 6, 1, None),
    ))
    def test__interval__min_max(self, interval1: UnionInterval, inf, sup, min_v, max_v):
        """UnionInterval の最大値/最小値のテスト
        """
        assert interval1.inf() == inf
        assert interval1.sup() == sup
        assert interval1.min() == min_v
        assert interval1.max() == max_v

    @pytest.mark.parametrize('interval1, left_open, right_open', (
        (interval(empty=True), True, True),
        (interval(1, 5, edge='[]'), False, False),
        (interval(1, 5, edge='[)'), False, True),
        (interval(1, 5, edge='(]'), True, False),
        (interval(1, 5, edge='()'), True, True),
        (interval(1, None), False, True),
        (interval(None, 1), True, True),
        (interval(None, None), True, True),
        (interval(1, 2, edge='[]') + interval(3, 4, edge='[]'), False, False),
        (interval(1, 2, edge='[)') + interval(3, 4, edge='[]'), False, False),
        (interval(1, 2, edge='(]') + interval(3, 4, edge='[]'), True, False),
        (interval(1, 2, edge='()') + interval(3, 4, edge='[]'), True, False),
        (interval(1, 2, edge='[]') + interval(3, 4, edge='[)'), False, True),
        (interval(1, 2, edge='[)') + interval(3, 4, edge='[)'), False, True),
        (interval(1, 2, edge='(]') + interval(3, 4, edge='[)'), True, True),
        (interval(1, 2, edge='()') + interval(3, 4, edge='[)'), True, True),
        (interval(1, 2, edge='[]') + interval(3, 4, edge='(]'), False, False),
        (interval(1, 2, edge='[)') + interval(3, 4, edge='(]'), False, False),
        (interval(1, 2, edge='(]') + interval(3, 4, edge='(]'), True, False),
        (interval(1, 2, edge='()') + interval(3, 4, edge='(]'), True, False),
        (interval(1, 2, edge='[]') + interval(3, 4, edge='()'), False, True),
        (interval(1, 2, edge='[)') + interval(3, 4, edge='()'), False, True),
        (interval(1, 2, edge='(]') + interval(3, 4, edge='()'), True, True),
        (interval(1, 2, edge='()') + interval(3, 4, edge='()'), True, True),
    ))
    def test__interval__open__closed(self, interval1: UnionInterval, left_open, right_open):
        """UnionInterval の left_open, right_open のテスト
        """
        if left_open:
            assert interval1.left_open()
            assert not interval1.left_closed()
        else:
            assert not interval1.left_open()
            assert interval1.left_closed()

        if right_open:
            assert interval1.right_open()
            assert not interval1.right_closed()
        else:
            assert not interval1.right_open()
            assert interval1.right_closed()

    @pytest.mark.parametrize('interval1, is_singleton', (
        (interval(empty=True), False),
        (interval(singleton=1), True),
        (interval(1, 1, edge='[]'), True),
        (interval(1, 2, edge='[]'), False),
        (interval(1, 2, edge='[)'), False),
        (interval(1, 2, edge='(]'), False),
        (interval(1, 2, edge='()'), False),
        (interval(singleton=1) + interval(singleton=1), True),
        (interval(singleton=1) + interval(singleton=2), False),
    ))
    def test__interval__is_singleton(self, interval1: UnionInterval, is_singleton):
        """単集合判定をテストする。
        """
        assert interval1.is_singleton == is_singleton
