from datetime import datetime, timedelta

import pytest

from setrange import srange, SetRange


class TestSetRangeClass:

    @pytest.mark.parametrize('set_range', (
        srange(empty=True),
        srange(5, 10, edge='[]'),
        srange(5, 10, edge='[)'),
        srange(5, 10, edge='(]'),
        srange(5, 10, edge='()'),
        srange('f', 's'),
        srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)),
    ))
    def test__srange_unit__type(self, set_range):
        """srange関数の戻り値の型をテストする
        """
        assert isinstance(set_range, SetRange)

    @pytest.mark.parametrize('set_range, expected_str', (
        (srange(empty=True), '(empty)'),
        (srange(5, 10, edge='[]'), '[5, 10]'),
        (srange(5, 10, edge='[)'), '[5, 10)'),
        (srange(5, 10, edge='(]'), '(5, 10]'),
        (srange(5, 10, edge='()'), '(5, 10)'),
        (srange(None, 10, edge='[]'), '(-inf, 10]'),
        (srange(None, 10, edge='[)'), '(-inf, 10)'),
        (srange(None, 10, edge='(]'), '(-inf, 10]'),
        (srange(None, 10, edge='()'), '(-inf, 10)'),
        (srange(5, None, edge='[]'), '[5, inf)'),
        (srange(5, None, edge='[)'), '[5, inf)'),
        (srange(5, None, edge='(]'), '(5, inf)'),
        (srange(5, None, edge='()'), '(5, inf)'),
        (srange(None, None, edge='[]'), '(-inf, inf)'),
        (srange(None, None, edge='[)'), '(-inf, inf)'),
        (srange(None, None, edge='(]'), '(-inf, inf)'),
        (srange(None, None, edge='()'), '(-inf, inf)'),
    ))
    def test__srange_unit_int__str(self, set_range, expected_str):
        """単レンジ[int]の文字列化をテストする。
        """
        assert str(set_range) == expected_str

    @pytest.mark.parametrize('set_range_1, set_range_2, expected_equal', (
        (srange(5, 10), srange(5, 10), True),
        (srange(5, 10), srange(5, 9), False),
        (srange(5, 10), srange(5, 10, edge='()'), False),
        (srange(5, 10), srange(5, 10, edge='(]'), False),
        (srange(5, 10), srange(5, 10, edge='[]'), False),
        (srange(None, 10), srange(None, 10, edge='[)'), True),
        (srange(None, 10), srange(None, 10, edge='()'), True),
        (srange(None, 10), srange(None, 10, edge='(]'), False),
        (srange(None, 10), srange(None, 10, edge='[]'), False),
        (srange(5, None), srange(5, None, edge='[)'), True),
        (srange(5, None), srange(5, None, edge='()'), False),
        (srange(5, None), srange(5, None, edge='(]'), False),
        (srange(5, None), srange(5, None, edge='[]'), True),
        (srange(None, None), srange(None, None, edge='[)'), True),
        (srange(None, None), srange(None, None, edge='()'), True),
        (srange(None, None), srange(None, None, edge='(]'), True),
        (srange(None, None), srange(None, None, edge='[]'), True),
        (srange(start=5), srange(5, None), True),
        (srange(start=5, edge='[)'), srange(5, None, edge='[)'), True),
        (srange(start=5, edge='()'), srange(5, None, edge='()'), True),
        (srange(end=10), srange(None, 10), True),
        (srange(end=10, edge='(]'), srange(None, 10, edge='(]'), True),
        (srange(end=10, edge='()'), srange(None, 10, edge='()'), True),
        (srange(), srange(None, None), True),
        (srange(empty=True), srange(empty=True), True),
        (srange(empty=True), srange(empty=True, singleton=1), True),
        (srange(singleton=1), srange(1, 1, edge='[]'), True),
        (srange(singleton=1), srange(1, 2, edge='[]'), False),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)),
         srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)), True),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)),
         srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 34)), False),
    ))
    def test__srange_unit__equal(self, set_range_1, set_range_2, expected_equal):
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
        (srange(5, 10), 4, False),
        (srange(5, 10), 5, True),
        (srange(5, 10), 9, True),
        (srange(5, 10), 10, False),
        (srange(5, 10), 4.0, False),
        (srange(5, 10), 5.0, True),
        (srange(5, 10), 9.0, True),
        (srange(5, 10), 10.0, False),
        (srange(5, 10, '[]'), 4, False),
        (srange(5, 10, '[]'), 5, True),
        (srange(5, 10, '[]'), 10, True),
        (srange(5, 10, '[]'), 11, False),
        (srange(5, 10, '[]'), 4.0, False),
        (srange(5, 10, '[]'), 5.0, True),
        (srange(5, 10, '[]'), 10.0, True),
        (srange(5, 10, '[]'), 11.0, False),
        (srange(5, 10, '[)'), 4, False),
        (srange(5, 10, '[)'), 5, True),
        (srange(5, 10, '[)'), 9, True),
        (srange(5, 10, '[)'), 10, False),
        (srange(5, 10, '[)'), 4.0, False),
        (srange(5, 10, '[)'), 5.0, True),
        (srange(5, 10, '[)'), 9.0, True),
        (srange(5, 10, '[)'), 10.0, False),
        (srange(5, 10, '(]'), 5, False),
        (srange(5, 10, '(]'), 6, True),
        (srange(5, 10, '(]'), 10, True),
        (srange(5, 10, '(]'), 11, False),
        (srange(5, 10, '(]'), 5.0, False),
        (srange(5, 10, '(]'), 6.0, True),
        (srange(5, 10, '(]'), 10.0, True),
        (srange(5, 10, '(]'), 11.0, False),
        (srange(5, 10, '()'), 5, False),
        (srange(5, 10, '()'), 6, True),
        (srange(5, 10, '()'), 9, True),
        (srange(5, 10, '()'), 10, False),
        (srange(5, 10, '()'), 5.0, False),
        (srange(5, 10, '()'), 6.0, True),
        (srange(5, 10, '()'), 9.0, True),
        (srange(5, 10, '()'), 10.0, False),
        (srange(None, 10, '(]'), -10, True),
        (srange(None, 10, '(]'), 10, True),
        (srange(None, 10, '(]'), 11, False),
        (srange(None, 10, '()'), -10, True),
        (srange(None, 10, '()'), 9, True),
        (srange(None, 10, '()'), 10, False),
        (srange(5, None, '[)'), 4, False),
        (srange(5, None, '[)'), 5, True),
        (srange(5, None, '[)'), 100, True),
        (srange(5, None, '()'), 5, False),
        (srange(5, None, '()'), 6, True),
        (srange(5, None, '()'), 100, True),
        (srange('f', 's'), 'e', False),
        (srange('f', 's'), 'ee', False),
        (srange('f', 's'), 'f', True),
        (srange('f', 's'), 'fa', True),
        (srange('f', 's'), 's', False),
        (srange('f', 's'), 'sa', False),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)),
         datetime(2020, 12, 30, 11, 22, 32), False),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)),
         datetime(2020, 12, 30, 11, 22, 33), True),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)),
         datetime(2020, 12, 31, 11, 22, 32), True),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 31, 11, 22, 33)),
         datetime(2020, 12, 31, 11, 22, 33), False),
        (srange(None, datetime(2020, 12, 31, 11, 22, 33)),
         datetime(1900, 12, 30, 11, 22, 33), True),
        (srange(None, datetime(2020, 12, 31, 11, 22, 33)),
         datetime(2020, 12, 31, 11, 22, 32), True),
        (srange(None, datetime(2020, 12, 31, 11, 22, 33)),
         datetime(2020, 12, 31, 11, 22, 33), False),
        (srange(datetime(2020, 12, 30, 11, 22, 33), None),
         datetime(2020, 12, 30, 11, 22, 32), False),
        (srange(datetime(2020, 12, 30, 11, 22, 33), None),
         datetime(2020, 12, 30, 11, 22, 33), True),
        (srange(datetime(2020, 12, 30, 11, 22, 33), None),
         datetime(2100, 12, 30, 11, 22, 33), True),
    ))
    def test__srange_unit__contain(self, set_range, element, expected_contain):
        """単レンジの含有演算をテストする。

        端点と比較できるオブジェクトであれば、含有するかどうか確かめられる。
        """
        if expected_contain:
            assert element in set_range
        else:
            assert element not in set_range

    @pytest.mark.parametrize('target, is_empty', (
        (srange(5, 6, '[]'), False),
        (srange(5, 6, '[)'), False),
        (srange(5, 6, '(]'), False),
        (srange(5, 6, '()'), False),
        (srange(5, 5, '[]'), False),
        (srange(5, 5, '[)'), True),
        (srange(5, 5, '(]'), True),
        (srange(5, 5, '()'), True),
        (srange(5, 4, '[]'), True),
        (srange(5, 4, '[)'), True),
        (srange(5, 4, '(]'), True),
        (srange(5, 4, '()'), True),
        (srange(None, 6, '[]'), False),
        (srange(None, 6, '[)'), False),
        (srange(None, 6, '(]'), False),
        (srange(None, 6, '()'), False),
        (srange(5, None, '[]'), False),
        (srange(5, None, '[)'), False),
        (srange(5, None, '(]'), False),
        (srange(5, None, '()'), False),
        (srange(None, None, '[]'), False),
        (srange(None, None, '[)'), False),
        (srange(None, None, '(]'), False),
        (srange(None, None, '()'), False),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 34), '[]'), False),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 34), '[)'), False),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 34), '(]'), False),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 34), '()'), False),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 33), '[]'), False),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 33), '[)'), True),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 33), '(]'), True),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 33), '()'), True),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 32), '[]'), True),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 32), '[)'), True),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 32), '(]'), True),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 32), '()'), True),
    ))
    def test__srange_unit_empty__start_g_end(self, target, is_empty):
        """端点の指定次第で単レンジが空になることをテストする。
        """
        assert target.is_empty == is_empty
        if is_empty:
            assert srange(empty=True) == target
            assert target == srange(empty=True)
            assert not target
        else:
            assert srange(empty=True) != target
            assert target != srange(empty=True)
            assert target

    @pytest.mark.parametrize('srange1, srange2, srange_m', (
        # 単レンジ同士で一方の終点ともう一方の始点が一致するパターン
        (srange(5, 6, '[]'), srange(6, 7, '[]'), srange(5, 7, '[]')),
        (srange(5, 6, '[)'), srange(6, 7, '[]'), srange(5, 7, '[]')),
        (srange(5, 6, '(]'), srange(6, 7, '[]'), srange(5, 7, '(]')),
        (srange(5, 6, '()'), srange(6, 7, '[]'), srange(5, 7, '(]')),
        (srange(5, 6, '[]'), srange(6, 7, '[)'), srange(5, 7, '[)')),
        (srange(5, 6, '[)'), srange(6, 7, '[)'), srange(5, 7, '[)')),
        (srange(5, 6, '(]'), srange(6, 7, '[)'), srange(5, 7, '()')),
        (srange(5, 6, '()'), srange(6, 7, '[)'), srange(5, 7, '()')),
        (srange(5, 6, '[]'), srange(6, 7, '(]'), srange(5, 7, '[]')),
        (srange(5, 6, '[)'), srange(6, 7, '(]'), [srange(5, 6, '[)'), srange(6, 7, '(]')]),
        (srange(5, 6, '(]'), srange(6, 7, '(]'), srange(5, 7, '(]')),
        (srange(5, 6, '()'), srange(6, 7, '(]'), [srange(5, 6, '()'), srange(6, 7, '(]')]),
        (srange(5, 6, '[]'), srange(6, 7, '()'), srange(5, 7, '[)')),
        (srange(5, 6, '[)'), srange(6, 7, '()'), [srange(5, 6, '[)'), srange(6, 7, '()')]),
        (srange(5, 6, '(]'), srange(6, 7, '()'), srange(5, 7, '()')),
        (srange(5, 6, '()'), srange(6, 7, '()'), [srange(5, 6, '()'), srange(6, 7, '()')]),
        (srange(None, 6, '(]'), srange(6, 7, '[]'), srange(None, 7, '(]')),
        (srange(None, 6, '()'), srange(6, 7, '[]'), srange(None, 7, '(]')),
        (srange(None, 6, '(]'), srange(6, 7, '[)'), srange(None, 7, '()')),
        (srange(None, 6, '()'), srange(6, 7, '[)'), srange(None, 7, '()')),
        (srange(None, 6, '(]'), srange(6, 7, '(]'), srange(None, 7, '(]')),
        (srange(None, 6, '()'), srange(6, 7, '(]'), [srange(None, 6, '()'), srange(6, 7, '(]')]),
        (srange(None, 6, '(]'), srange(6, 7, '()'), srange(None, 7, '()')),
        (srange(None, 6, '()'), srange(6, 7, '()'), [srange(None, 6, '()'), srange(6, 7, '()')]),
        (srange(5, 6, '[]'), srange(6, None, '[)'), srange(5, None, '[)')),
        (srange(5, 6, '[)'), srange(6, None, '[)'), srange(5, None, '[)')),
        (srange(5, 6, '(]'), srange(6, None, '[)'), srange(5, None, '()')),
        (srange(5, 6, '()'), srange(6, None, '[)'), srange(5, None, '()')),
        (srange(5, 6, '[]'), srange(6, None, '()'), srange(5, None, '[)')),
        (srange(5, 6, '[)'), srange(6, None, '()'), [srange(5, 6, '[)'), srange(6, None, '()')]),
        (srange(5, 6, '(]'), srange(6, None, '()'), srange(5, None, '()')),
        (srange(5, 6, '()'), srange(6, None, '()'), [srange(5, 6, '()'), srange(6, None, '()')]),
        (srange(None, 6, '(]'), srange(6, None, '[)'), srange(None, None, '()')),
        (srange(None, 6, '()'), srange(6, None, '[)'), srange(None, None, '()')),
        (srange(None, 6, '(]'), srange(6, None, '()'), srange(None, None, '()')),
        (srange(None, 6, '()'), srange(6, None, '()'), [srange(None, 6, '()'), srange(6, None, '()')]),
        # 単レンジ同士で一方ともう一方に共通部分がないパターン
        (srange(5, 6, '[]'), srange(7, 8, '[]'), [srange(5, 6, '[]'), srange(7, 8, '[]')]),
        (srange(5, 6, '[)'), srange(7, 8, '[]'), [srange(5, 6, '[)'), srange(7, 8, '[]')]),
        (srange(5, 6, '(]'), srange(7, 8, '[]'), [srange(5, 6, '(]'), srange(7, 8, '[]')]),
        (srange(5, 6, '()'), srange(7, 8, '[]'), [srange(5, 6, '()'), srange(7, 8, '[]')]),
        (srange(5, 6, '[]'), srange(7, 8, '[)'), [srange(5, 6, '[]'), srange(7, 8, '[)')]),
        (srange(5, 6, '[)'), srange(7, 8, '[)'), [srange(5, 6, '[)'), srange(7, 8, '[)')]),
        (srange(5, 6, '(]'), srange(7, 8, '[)'), [srange(5, 6, '(]'), srange(7, 8, '[)')]),
        (srange(5, 6, '()'), srange(7, 8, '[)'), [srange(5, 6, '()'), srange(7, 8, '[)')]),
        (srange(5, 6, '[]'), srange(7, 8, '(]'), [srange(5, 6, '[]'), srange(7, 8, '(]')]),
        (srange(5, 6, '[)'), srange(7, 8, '(]'), [srange(5, 6, '[)'), srange(7, 8, '(]')]),
        (srange(5, 6, '(]'), srange(7, 8, '(]'), [srange(5, 6, '(]'), srange(7, 8, '(]')]),
        (srange(5, 6, '()'), srange(7, 8, '(]'), [srange(5, 6, '()'), srange(7, 8, '(]')]),
        (srange(5, 6, '[]'), srange(7, 8, '()'), [srange(5, 6, '[]'), srange(7, 8, '()')]),
        (srange(5, 6, '[)'), srange(7, 8, '()'), [srange(5, 6, '[)'), srange(7, 8, '()')]),
        (srange(5, 6, '(]'), srange(7, 8, '()'), [srange(5, 6, '(]'), srange(7, 8, '()')]),
        (srange(5, 6, '()'), srange(7, 8, '()'), [srange(5, 6, '()'), srange(7, 8, '()')]),
        (srange(None, 6, '(]'), srange(7, 8, '[]'), [srange(None, 6, '(]'), srange(7, 8, '[]')]),
        (srange(None, 6, '()'), srange(7, 8, '[]'), [srange(None, 6, '()'), srange(7, 8, '[]')]),
        (srange(None, 6, '(]'), srange(7, 8, '[)'), [srange(None, 6, '(]'), srange(7, 8, '[)')]),
        (srange(None, 6, '()'), srange(7, 8, '[)'), [srange(None, 6, '()'), srange(7, 8, '[)')]),
        (srange(None, 6, '(]'), srange(7, 8, '(]'), [srange(None, 6, '(]'), srange(7, 8, '(]')]),
        (srange(None, 6, '()'), srange(7, 8, '(]'), [srange(None, 6, '()'), srange(7, 8, '(]')]),
        (srange(None, 6, '(]'), srange(7, 8, '()'), [srange(None, 6, '(]'), srange(7, 8, '()')]),
        (srange(None, 6, '()'), srange(7, 8, '()'), [srange(None, 6, '()'), srange(7, 8, '()')]),
        (srange(5, 6, '[]'), srange(7, None, '[)'), [srange(5, 6, '[]'), srange(7, None, '[)')]),
        (srange(5, 6, '[)'), srange(7, None, '[)'), [srange(5, 6, '[)'), srange(7, None, '[)')]),
        (srange(5, 6, '(]'), srange(7, None, '[)'), [srange(5, 6, '(]'), srange(7, None, '[)')]),
        (srange(5, 6, '()'), srange(7, None, '[)'), [srange(5, 6, '()'), srange(7, None, '[)')]),
        (srange(5, 6, '[]'), srange(7, None, '()'), [srange(5, 6, '[]'), srange(7, None, '()')]),
        (srange(5, 6, '[)'), srange(7, None, '()'), [srange(5, 6, '[)'), srange(7, None, '()')]),
        (srange(5, 6, '(]'), srange(7, None, '()'), [srange(5, 6, '(]'), srange(7, None, '()')]),
        (srange(5, 6, '()'), srange(7, None, '()'), [srange(5, 6, '()'), srange(7, None, '()')]),
        (srange(None, 6, '(]'), srange(7, None, '[)'), [srange(None, 6, '(]'), srange(7, None, '[)')]),
        (srange(None, 6, '()'), srange(7, None, '[)'), [srange(None, 6, '()'), srange(7, None, '[)')]),
        (srange(None, 6, '(]'), srange(7, None, '()'), [srange(None, 6, '(]'), srange(7, None, '()')]),
        (srange(None, 6, '()'), srange(7, None, '()'), [srange(None, 6, '()'), srange(7, None, '()')]),
        # 単レンジ同士で一方ともう一方にシングルトンでない共通部分があるパターン
        (srange(5, 7, '[]'), srange(6, 8, '[]'), srange(5, 8, '[]')),
        (srange(5, 7, '[)'), srange(6, 8, '[]'), srange(5, 8, '[]')),
        (srange(5, 7, '(]'), srange(6, 8, '[]'), srange(5, 8, '(]')),
        (srange(5, 7, '()'), srange(6, 8, '[]'), srange(5, 8, '(]')),
        (srange(5, 7, '[]'), srange(6, 8, '[)'), srange(5, 8, '[)')),
        (srange(5, 7, '[)'), srange(6, 8, '[)'), srange(5, 8, '[)')),
        (srange(5, 7, '(]'), srange(6, 8, '[)'), srange(5, 8, '()')),
        (srange(5, 7, '()'), srange(6, 8, '[)'), srange(5, 8, '()')),
        (srange(5, 7, '[]'), srange(6, 8, '(]'), srange(5, 8, '[]')),
        (srange(5, 7, '[)'), srange(6, 8, '(]'), srange(5, 8, '[]')),
        (srange(5, 7, '(]'), srange(6, 8, '(]'), srange(5, 8, '(]')),
        (srange(5, 7, '()'), srange(6, 8, '(]'), srange(5, 8, '(]')),
        (srange(5, 7, '[]'), srange(6, 8, '()'), srange(5, 8, '[)')),
        (srange(5, 7, '[)'), srange(6, 8, '()'), srange(5, 8, '[)')),
        (srange(5, 7, '(]'), srange(6, 8, '()'), srange(5, 8, '()')),
        (srange(5, 7, '()'), srange(6, 8, '()'), srange(5, 8, '()')),
        (srange(None, 7, '(]'), srange(6, 8, '[]'), srange(None, 8, '(]')),
        (srange(None, 7, '()'), srange(6, 8, '[]'), srange(None, 8, '(]')),
        (srange(None, 7, '(]'), srange(6, 8, '[)'), srange(None, 8, '()')),
        (srange(None, 7, '()'), srange(6, 8, '[)'), srange(None, 8, '()')),
        (srange(None, 7, '(]'), srange(6, 8, '(]'), srange(None, 8, '(]')),
        (srange(None, 7, '()'), srange(6, 8, '(]'), srange(None, 8, '(]')),
        (srange(None, 7, '(]'), srange(6, 8, '()'), srange(None, 8, '()')),
        (srange(None, 7, '()'), srange(6, 8, '()'), srange(None, 8, '()')),
        (srange(5, None, '[)'), srange(6, 8, '[]'), srange(5, None, '[)')),
        (srange(5, None, '()'), srange(6, 8, '[]'), srange(5, None, '()')),
        (srange(5, None, '[)'), srange(6, 8, '[)'), srange(5, None, '[)')),
        (srange(5, None, '()'), srange(6, 8, '[)'), srange(5, None, '()')),
        (srange(5, None, '[)'), srange(6, 8, '(]'), srange(5, None, '[)')),
        (srange(5, None, '()'), srange(6, 8, '(]'), srange(5, None, '()')),
        (srange(5, None, '[)'), srange(6, 8, '()'), srange(5, None, '[)')),
        (srange(5, None, '()'), srange(6, 8, '()'), srange(5, None, '()')),
        # 一方が空のパターン
        (srange(5, 6, '[]'), srange(empty=True), srange(5, 6, '[]')),
        (srange(None, 6, '(]'), srange(empty=True), srange(None, 6, '(]')),
        (srange(5, None, '[)'), srange(empty=True), srange(5, None, '[)')),
        (srange(None, None, '()'), srange(empty=True), srange(None, None, '()')),
        (srange(empty=True), srange(empty=True), srange(empty=True)),
        # 一方が単レンジでないパターン
        (srange(4, 6, '[]') + srange(8, 10, '[]'), srange(3, 5, '[]'), [srange(3, 6, '[]'), srange(8, 10, '[]')]),
        (srange(4, 6, '[)') + srange(8, 10, '[]'), srange(3, 5, '[]'), [srange(3, 6, '[)'), srange(8, 10, '[]')]),
        (srange(4, 6, '(]') + srange(8, 10, '[]'), srange(3, 5, '[]'), [srange(3, 6, '[]'), srange(8, 10, '[]')]),
        (srange(4, 6, '()') + srange(8, 10, '[]'), srange(3, 5, '[]'), [srange(3, 6, '[)'), srange(8, 10, '[]')]),
        (srange(4, 6, '[]') + srange(8, 10, '[]'), srange(3, 5, '[)'), [srange(3, 6, '[]'), srange(8, 10, '[]')]),
        (srange(4, 6, '[)') + srange(8, 10, '[]'), srange(3, 5, '[)'), [srange(3, 6, '[)'), srange(8, 10, '[]')]),
        (srange(4, 6, '(]') + srange(8, 10, '[]'), srange(3, 5, '[)'), [srange(3, 6, '[]'), srange(8, 10, '[]')]),
        (srange(4, 6, '()') + srange(8, 10, '[]'), srange(3, 5, '[)'), [srange(3, 6, '[)'), srange(8, 10, '[]')]),
        (srange(4, 6, '[]') + srange(8, 10, '[]'), srange(3, 5, '(]'), [srange(3, 6, '(]'), srange(8, 10, '[]')]),
        (srange(4, 6, '[)') + srange(8, 10, '[]'), srange(3, 5, '(]'), [srange(3, 6, '()'), srange(8, 10, '[]')]),
        (srange(4, 6, '(]') + srange(8, 10, '[]'), srange(3, 5, '(]'), [srange(3, 6, '(]'), srange(8, 10, '[]')]),
        (srange(4, 6, '()') + srange(8, 10, '[]'), srange(3, 5, '(]'), [srange(3, 6, '()'), srange(8, 10, '[]')]),
        (srange(4, 6, '[]') + srange(8, 10, '[]'), srange(3, 5, '()'), [srange(3, 6, '(]'), srange(8, 10, '[]')]),
        (srange(4, 6, '[)') + srange(8, 10, '[]'), srange(3, 5, '()'), [srange(3, 6, '()'), srange(8, 10, '[]')]),
        (srange(4, 6, '(]') + srange(8, 10, '[]'), srange(3, 5, '()'), [srange(3, 6, '(]'), srange(8, 10, '[]')]),
        (srange(4, 6, '()') + srange(8, 10, '[]'), srange(3, 5, '()'), [srange(3, 6, '()'), srange(8, 10, '[]')]),
        # 一方が単レンジでないパターン
        (srange(4, 6, '[]') + srange(8, 10, '[]'), srange(6, 8, '[]'), srange(4, 10, '[]')),
        (srange(4, 6, '[]') + srange(8, 10, '[]'), srange(6, 8, '[)'), srange(4, 10, '[]')),
        (srange(4, 6, '[]') + srange(8, 10, '[]'), srange(6, 8, '(]'), srange(4, 10, '[]')),
        (srange(4, 6, '[]') + srange(8, 10, '[]'), srange(6, 8, '()'), srange(4, 10, '[]')),
        (srange(4, 6, '[)') + srange(8, 10, '[]'), srange(6, 8, '[]'), srange(4, 10, '[]')),
        (srange(4, 6, '[)') + srange(8, 10, '[]'), srange(6, 8, '[)'), srange(4, 10, '[]')),
        (srange(4, 6, '[)') + srange(8, 10, '[]'), srange(6, 8, '(]'), [srange(4, 6, '[)'), srange(6, 10, '(]')]),
        (srange(4, 6, '[)') + srange(8, 10, '[]'), srange(6, 8, '()'), [srange(4, 6, '[)'), srange(6, 10, '(]')]),
        (srange(4, 6, '(]') + srange(8, 10, '[]'), srange(6, 8, '[]'), srange(4, 10, '(]')),
        (srange(4, 6, '(]') + srange(8, 10, '[]'), srange(6, 8, '[)'), srange(4, 10, '(]')),
        (srange(4, 6, '(]') + srange(8, 10, '[]'), srange(6, 8, '(]'), srange(4, 10, '(]')),
        (srange(4, 6, '(]') + srange(8, 10, '[]'), srange(6, 8, '()'), srange(4, 10, '(]')),
        (srange(4, 6, '()') + srange(8, 10, '[]'), srange(6, 8, '[]'), srange(4, 10, '(]')),
        (srange(4, 6, '()') + srange(8, 10, '[]'), srange(6, 8, '[)'), srange(4, 10, '(]')),
        (srange(4, 6, '()') + srange(8, 10, '[]'), srange(6, 8, '(]'), [srange(4, 6, '()'), srange(6, 10, '(]')]),
        (srange(4, 6, '()') + srange(8, 10, '[]'), srange(6, 8, '()'), [srange(4, 6, '()'), srange(6, 10, '(]')]),
        (srange(4, 6, '[]') + srange(8, 10, '[)'), srange(6, 8, '[]'), srange(4, 10, '[)')),
        (srange(4, 6, '[]') + srange(8, 10, '[)'), srange(6, 8, '[)'), srange(4, 10, '[)')),
        (srange(4, 6, '[]') + srange(8, 10, '[)'), srange(6, 8, '(]'), srange(4, 10, '[)')),
        (srange(4, 6, '[]') + srange(8, 10, '[)'), srange(6, 8, '()'), srange(4, 10, '[)')),
        (srange(4, 6, '[)') + srange(8, 10, '[)'), srange(6, 8, '[]'), srange(4, 10, '[)')),
        (srange(4, 6, '[)') + srange(8, 10, '[)'), srange(6, 8, '[)'), srange(4, 10, '[)')),
        (srange(4, 6, '[)') + srange(8, 10, '[)'), srange(6, 8, '(]'), [srange(4, 6, '[)'), srange(6, 10, '()')]),
        (srange(4, 6, '[)') + srange(8, 10, '[)'), srange(6, 8, '()'), [srange(4, 6, '[)'), srange(6, 10, '()')]),
        (srange(4, 6, '(]') + srange(8, 10, '[)'), srange(6, 8, '[]'), srange(4, 10, '()')),
        (srange(4, 6, '(]') + srange(8, 10, '[)'), srange(6, 8, '[)'), srange(4, 10, '()')),
        (srange(4, 6, '(]') + srange(8, 10, '[)'), srange(6, 8, '(]'), srange(4, 10, '()')),
        (srange(4, 6, '(]') + srange(8, 10, '[)'), srange(6, 8, '()'), srange(4, 10, '()')),
        (srange(4, 6, '()') + srange(8, 10, '[)'), srange(6, 8, '[]'), srange(4, 10, '()')),
        (srange(4, 6, '()') + srange(8, 10, '[)'), srange(6, 8, '[)'), srange(4, 10, '()')),
        (srange(4, 6, '()') + srange(8, 10, '[)'), srange(6, 8, '(]'), [srange(4, 6, '()'), srange(6, 10, '()')]),
        (srange(4, 6, '()') + srange(8, 10, '[)'), srange(6, 8, '()'), [srange(4, 6, '()'), srange(6, 10, '()')]),
        (srange(4, 6, '[]') + srange(8, 10, '(]'), srange(6, 8, '[]'), srange(4, 10, '[]')),
        (srange(4, 6, '[]') + srange(8, 10, '(]'), srange(6, 8, '[)'), [srange(4, 8, '[)'), srange(8, 10, '(]')]),
        (srange(4, 6, '[]') + srange(8, 10, '(]'), srange(6, 8, '(]'), srange(4, 10, '[]')),
        (srange(4, 6, '[]') + srange(8, 10, '(]'), srange(6, 8, '()'), [srange(4, 8, '[)'), srange(8, 10, '(]')]),
        (srange(4, 6, '[)') + srange(8, 10, '(]'), srange(6, 8, '[]'), srange(4, 10, '[]')),
        (srange(4, 6, '[)') + srange(8, 10, '(]'), srange(6, 8, '[)'), [srange(4, 8, '[)'), srange(8, 10, '(]')]),
        (srange(4, 6, '[)') + srange(8, 10, '(]'), srange(6, 8, '(]'), [srange(4, 6, '[)'), srange(6, 10, '(]')]),
        (srange(4, 6, '[)') + srange(8, 10, '(]'), srange(6, 8, '()'),
         [srange(4, 6, '[)'), srange(6, 8, '()'), srange(8, 10, '(]')]),
        (srange(4, 6, '(]') + srange(8, 10, '(]'), srange(6, 8, '[]'), srange(4, 10, '(]')),
        (srange(4, 6, '(]') + srange(8, 10, '(]'), srange(6, 8, '[)'), [srange(4, 8, '()'), srange(8, 10, '(]')]),
        (srange(4, 6, '(]') + srange(8, 10, '(]'), srange(6, 8, '(]'), srange(4, 10, '(]')),
        (srange(4, 6, '(]') + srange(8, 10, '(]'), srange(6, 8, '()'), [srange(4, 8, '()'), srange(8, 10, '(]')]),
        (srange(4, 6, '()') + srange(8, 10, '(]'), srange(6, 8, '[]'), srange(4, 10, '(]')),
        (srange(4, 6, '()') + srange(8, 10, '(]'), srange(6, 8, '[)'), [srange(4, 8, '()'), srange(8, 10, '(]')]),
        (srange(4, 6, '()') + srange(8, 10, '(]'), srange(6, 8, '(]'), [srange(4, 6, '()'), srange(6, 10, '(]')]),
        (srange(4, 6, '()') + srange(8, 10, '(]'), srange(6, 8, '()'),
         [srange(4, 6, '()'), srange(6, 8, '()'), srange(8, 10, '(]')]),
        (srange(4, 6, '[]') + srange(8, 10, '()'), srange(6, 8, '[]'), srange(4, 10, '[)')),
        (srange(4, 6, '[]') + srange(8, 10, '()'), srange(6, 8, '[)'), [srange(4, 8, '[)'), srange(8, 10, '()')]),
        (srange(4, 6, '[]') + srange(8, 10, '()'), srange(6, 8, '(]'), srange(4, 10, '[)')),
        (srange(4, 6, '[]') + srange(8, 10, '()'), srange(6, 8, '()'), [srange(4, 8, '[)'), srange(8, 10, '()')]),
        (srange(4, 6, '[)') + srange(8, 10, '()'), srange(6, 8, '[]'), srange(4, 10, '[)')),
        (srange(4, 6, '[)') + srange(8, 10, '()'), srange(6, 8, '[)'), [srange(4, 8, '[)'), srange(8, 10, '()')]),
        (srange(4, 6, '[)') + srange(8, 10, '()'), srange(6, 8, '(]'), [srange(4, 6, '[)'), srange(6, 10, '()')]),
        (srange(4, 6, '[)') + srange(8, 10, '()'), srange(6, 8, '()'),
         [srange(4, 6, '[)'), srange(6, 8, '()'), srange(8, 10, '()')]),
        (srange(4, 6, '(]') + srange(8, 10, '()'), srange(6, 8, '[]'), srange(4, 10, '()')),
        (srange(4, 6, '(]') + srange(8, 10, '()'), srange(6, 8, '[)'), [srange(4, 8, '()'), srange(8, 10, '()')]),
        (srange(4, 6, '(]') + srange(8, 10, '()'), srange(6, 8, '(]'), srange(4, 10, '()')),
        (srange(4, 6, '(]') + srange(8, 10, '()'), srange(6, 8, '()'), [srange(4, 8, '()'), srange(8, 10, '()')]),
        (srange(4, 6, '()') + srange(8, 10, '()'), srange(6, 8, '[]'), srange(4, 10, '()')),
        (srange(4, 6, '()') + srange(8, 10, '()'), srange(6, 8, '[)'), [srange(4, 8, '()'), srange(8, 10, '()')]),
        (srange(4, 6, '()') + srange(8, 10, '()'), srange(6, 8, '(]'), [srange(4, 6, '()'), srange(6, 10, '()')]),
        (srange(4, 6, '()') + srange(8, 10, '()'), srange(6, 8, '()'),
         [srange(4, 6, '()'), srange(6, 8, '()'), srange(8, 10, '()')]),

        (srange(4, 6, '[]') + srange(8, 10, '[]') + srange(12, 14, '[]'), srange(6, 12, '[]'), srange(4, 14, '[]')),
        # 双方が単レンジでないパターン
        (srange(4, 6, '[]') + srange(8, 10, '[]'), srange(7, 7, '[]') + srange(11, 12, '[]'),
         [srange(4, 6, '[]'), srange(7, 7, '[]'), srange(8, 10, '[]'), srange(11, 12, '[]')]),
        (srange(4, 6, '[]') + srange(8, 10, '[]'), srange(5, 7, '[]') + srange(11, 12, '[]'),
         [srange(4, 7, '[]'), srange(8, 10, '[]'), srange(11, 12, '[]')]),
        (srange(1, 6, '[]') + srange(8, 10, '[]'), srange(2, 3, '[]') + srange(4, 5, '[]'),
         [srange(1, 6, '[]'), srange(8, 10, '[]')]),
        (srange(1, 6, '[]') + srange(8, 10, '[]'), srange(2, 3, '[]') + srange(4, 7, '[]'),
         [srange(1, 7, '[]'), srange(8, 10, '[]')]),
    ))
    def test__srange_unit_int__add__unit(self, srange1, srange2, srange_m):
        """レンジ[int]()の加法演算 (合併) をテストする。
        """
        if isinstance(srange_m, list):
            result = srange2 + srange1
            assert not result.is_empty
            assert result._unit_list == srange_m

            result = srange1 + srange2
            assert not result.is_empty
            assert result._unit_list == srange_m
        else:
            result = srange2 + srange1
            assert result == srange_m

            result = srange1 + srange2
            assert result == srange_m

    @pytest.mark.parametrize('srange1, srange2, srange_m', (
        # 一方が他方を包含するパターン
        (srange(5, 10, '[]'), srange(7, 9, '[]'), srange(7, 9, '[]')),
        (srange(5, 10, '[)'), srange(7, 9, '[]'), srange(7, 9, '[]')),
        (srange(5, 10, '(]'), srange(7, 9, '[]'), srange(7, 9, '[]')),
        (srange(5, 10, '()'), srange(7, 9, '[]'), srange(7, 9, '[]')),
        (srange(5, 10, '[]'), srange(7, 9, '[)'), srange(7, 9, '[)')),
        (srange(5, 10, '[)'), srange(7, 9, '[)'), srange(7, 9, '[)')),
        (srange(5, 10, '(]'), srange(7, 9, '[)'), srange(7, 9, '[)')),
        (srange(5, 10, '()'), srange(7, 9, '[)'), srange(7, 9, '[)')),
        (srange(5, 10, '[]'), srange(7, 9, '(]'), srange(7, 9, '(]')),
        (srange(5, 10, '[)'), srange(7, 9, '(]'), srange(7, 9, '(]')),
        (srange(5, 10, '(]'), srange(7, 9, '(]'), srange(7, 9, '(]')),
        (srange(5, 10, '()'), srange(7, 9, '(]'), srange(7, 9, '(]')),
        (srange(5, 10, '[]'), srange(7, 9, '()'), srange(7, 9, '()')),
        (srange(5, 10, '[)'), srange(7, 9, '()'), srange(7, 9, '()')),
        (srange(5, 10, '(]'), srange(7, 9, '()'), srange(7, 9, '()')),
        (srange(5, 10, '()'), srange(7, 9, '()'), srange(7, 9, '()')),
        (srange(None, 10, '(]'), srange(7, 9, '[]'), srange(7, 9, '[]')),
        (srange(None, 10, '()'), srange(7, 9, '[]'), srange(7, 9, '[]')),
        (srange(None, 10, '(]'), srange(7, 9, '[)'), srange(7, 9, '[)')),
        (srange(None, 10, '()'), srange(7, 9, '[)'), srange(7, 9, '[)')),
        (srange(None, 10, '(]'), srange(7, 9, '(]'), srange(7, 9, '(]')),
        (srange(None, 10, '()'), srange(7, 9, '(]'), srange(7, 9, '(]')),
        (srange(None, 10, '(]'), srange(7, 9, '()'), srange(7, 9, '()')),
        (srange(None, 10, '()'), srange(7, 9, '()'), srange(7, 9, '()')),
        (srange(5, None, '[)'), srange(7, 9, '[]'), srange(7, 9, '[]')),
        (srange(5, None, '()'), srange(7, 9, '[]'), srange(7, 9, '[]')),
        (srange(5, None, '[)'), srange(7, 9, '[)'), srange(7, 9, '[)')),
        (srange(5, None, '()'), srange(7, 9, '[)'), srange(7, 9, '[)')),
        (srange(5, None, '[)'), srange(7, 9, '(]'), srange(7, 9, '(]')),
        (srange(5, None, '()'), srange(7, 9, '(]'), srange(7, 9, '(]')),
        (srange(5, None, '[)'), srange(7, 9, '()'), srange(7, 9, '()')),
        (srange(5, None, '()'), srange(7, 9, '()'), srange(7, 9, '()')),
        (srange(None, None, '()'), srange(7, 9, '[]'), srange(7, 9, '[]')),
        (srange(None, None, '()'), srange(7, 9, '[)'), srange(7, 9, '[)')),
        (srange(None, None, '()'), srange(7, 9, '(]'), srange(7, 9, '(]')),
        (srange(None, None, '()'), srange(7, 9, '()'), srange(7, 9, '()')),
        # 共通部分が無いパターン (ただしオペランドが空の単レンジでない)
        (srange(5, 6, '[]'), srange(7, 9, '[]'), srange(empty=True)),
        (srange(5, 6, '[)'), srange(7, 9, '[]'), srange(empty=True)),
        (srange(5, 6, '(]'), srange(7, 9, '[]'), srange(empty=True)),
        (srange(5, 6, '()'), srange(7, 9, '[]'), srange(empty=True)),
        (srange(5, 6, '[]'), srange(7, 9, '[)'), srange(empty=True)),
        (srange(5, 6, '[)'), srange(7, 9, '[)'), srange(empty=True)),
        (srange(5, 6, '(]'), srange(7, 9, '[)'), srange(empty=True)),
        (srange(5, 6, '()'), srange(7, 9, '[)'), srange(empty=True)),
        (srange(5, 6, '[]'), srange(7, 9, '(]'), srange(empty=True)),
        (srange(5, 6, '[)'), srange(7, 9, '(]'), srange(empty=True)),
        (srange(5, 6, '(]'), srange(7, 9, '(]'), srange(empty=True)),
        (srange(5, 6, '()'), srange(7, 9, '(]'), srange(empty=True)),
        (srange(5, 6, '[]'), srange(7, 9, '()'), srange(empty=True)),
        (srange(5, 6, '[)'), srange(7, 9, '()'), srange(empty=True)),
        (srange(5, 6, '(]'), srange(7, 9, '()'), srange(empty=True)),
        (srange(5, 6, '()'), srange(7, 9, '()'), srange(empty=True)),
        (srange(None, 6, '(]'), srange(7, 9, '[]'), srange(empty=True)),
        (srange(None, 6, '()'), srange(7, 9, '[]'), srange(empty=True)),
        (srange(None, 6, '(]'), srange(7, 9, '[)'), srange(empty=True)),
        (srange(None, 6, '()'), srange(7, 9, '[)'), srange(empty=True)),
        (srange(None, 6, '(]'), srange(7, 9, '(]'), srange(empty=True)),
        (srange(None, 6, '()'), srange(7, 9, '(]'), srange(empty=True)),
        (srange(None, 6, '(]'), srange(7, 9, '()'), srange(empty=True)),
        (srange(None, 6, '()'), srange(7, 9, '()'), srange(empty=True)),
        (srange(5, 6, '[]'), srange(7, None, '[)'), srange(empty=True)),
        (srange(5, 6, '[)'), srange(7, None, '[)'), srange(empty=True)),
        (srange(5, 6, '(]'), srange(7, None, '[)'), srange(empty=True)),
        (srange(5, 6, '()'), srange(7, None, '[)'), srange(empty=True)),
        (srange(5, 6, '[]'), srange(7, None, '()'), srange(empty=True)),
        (srange(5, 6, '[)'), srange(7, None, '()'), srange(empty=True)),
        (srange(5, 6, '(]'), srange(7, None, '()'), srange(empty=True)),
        (srange(5, 6, '()'), srange(7, None, '()'), srange(empty=True)),
        (srange(None, 6, '(]'), srange(7, None, '[)'), srange(empty=True)),
        (srange(None, 6, '()'), srange(7, None, '[)'), srange(empty=True)),
        (srange(None, 6, '(]'), srange(7, None, '()'), srange(empty=True)),
        (srange(None, 6, '()'), srange(7, None, '()'), srange(empty=True)),
        # 少なくとも一方が空の単レンジであるパターン
        (srange(empty=True), srange(7, 9, '[]'), srange(empty=True)),
        (srange(empty=True), srange(7, 9, '[)'), srange(empty=True)),
        (srange(empty=True), srange(7, 9, '(]'), srange(empty=True)),
        (srange(empty=True), srange(7, 9, '()'), srange(empty=True)),
        (srange(empty=True), srange(empty=True), srange(empty=True)),
        (srange(empty=True), srange(None, 9, '(]'), srange(empty=True)),
        (srange(empty=True), srange(None, 9, '()'), srange(empty=True)),
        (srange(empty=True), srange(7, None, '[)'), srange(empty=True)),
        (srange(empty=True), srange(7, None, '()'), srange(empty=True)),
        # 共通部分があり、それがいずれのオペランドとも一致しないパターン
        (srange(5, 9, '[]'), srange(7, 12, '[]'), srange(7, 9, '[]')),
        (srange(5, 9, '[)'), srange(7, 12, '[]'), srange(7, 9, '[)')),
        (srange(5, 9, '(]'), srange(7, 12, '[]'), srange(7, 9, '[]')),
        (srange(5, 9, '()'), srange(7, 12, '[]'), srange(7, 9, '[)')),
        (srange(5, 9, '[]'), srange(7, 12, '[)'), srange(7, 9, '[]')),
        (srange(5, 9, '[)'), srange(7, 12, '[)'), srange(7, 9, '[)')),
        (srange(5, 9, '(]'), srange(7, 12, '[)'), srange(7, 9, '[]')),
        (srange(5, 9, '()'), srange(7, 12, '[)'), srange(7, 9, '[)')),
        (srange(5, 9, '[]'), srange(7, 12, '(]'), srange(7, 9, '(]')),
        (srange(5, 9, '[)'), srange(7, 12, '(]'), srange(7, 9, '()')),
        (srange(5, 9, '(]'), srange(7, 12, '(]'), srange(7, 9, '(]')),
        (srange(5, 9, '()'), srange(7, 12, '(]'), srange(7, 9, '()')),
        (srange(5, 9, '[]'), srange(7, 12, '()'), srange(7, 9, '(]')),
        (srange(5, 9, '[)'), srange(7, 12, '()'), srange(7, 9, '()')),
        (srange(5, 9, '(]'), srange(7, 12, '()'), srange(7, 9, '(]')),
        (srange(5, 9, '()'), srange(7, 12, '()'), srange(7, 9, '()')),
        # 共通部分がシングルトンであるパターン
        (srange(5, 9, '(]'), srange(9, 12, '[)'), srange(9, 9, '[]')),
        (srange(5, 9, '[]'), srange(9, 12, '[)'), srange(9, 9, '[]')),
        (srange(5, 9, '(]'), srange(9, 12, '[]'), srange(9, 9, '[]')),
        (srange(5, 9, '[]'), srange(9, 12, '[]'), srange(9, 9, '[]')),
        # オペランドが単レンジでない場合
        (srange(5, 10, '(]') + srange(15, 20, '[)'), srange(7, 8, '()') + srange(9, 18, '()'),
         srange(7, 8, '()') + srange(9, 10, '(]') + srange(15, 18, '[)')),
        (srange(5, 10, '(]') + srange(15, 20, '[)'), srange(empty=True), srange(empty=True)),
    ))
    def test__srange_unit_int__mul(self, srange1, srange2, srange_m):
        """レンジ[int]()の乗法演算 (交叉) をテストする。
        """
        assert srange1 * srange2 == srange_m
        assert srange2 * srange1 == srange_m

    @pytest.mark.parametrize('srange1, srange2, expected_issubset', (
        (srange(5, 10), srange(0, 20), True),
        (srange(5, 10), srange(5, 20), True),
        (srange(5, 10), srange(0, 10), True),
        (srange(5, 10), srange(5, 10), True),
        (srange(0, 10, '[]'), srange(0, 10, '[]'), True),
        (srange(0, 10, '(]'), srange(0, 10, '[]'), True),
        (srange(0, 10, '[)'), srange(0, 10, '[]'), True),
        (srange(0, 10, '()'), srange(0, 10, '[]'), True),
        (srange(0, 10, '[]'), srange(0, 10, '(]'), False),
        (srange(0, 10, '(]'), srange(0, 10, '(]'), True),
        (srange(0, 10, '[)'), srange(0, 10, '(]'), False),
        (srange(0, 10, '()'), srange(0, 10, '(]'), True),
        (srange(0, 10, '[]'), srange(0, 10, '[)'), False),
        (srange(0, 10, '(]'), srange(0, 10, '[)'), False),
        (srange(0, 10, '[)'), srange(0, 10, '[)'), True),
        (srange(0, 10, '()'), srange(0, 10, '[)'), True),
        (srange(0, 10, '[]'), srange(0, 10, '()'), False),
        (srange(0, 10, '(]'), srange(0, 10, '()'), False),
        (srange(0, 10, '[)'), srange(0, 10, '()'), False),
        (srange(0, 10, '()'), srange(0, 10, '()'), True),
        (srange(empty=True), srange(0, 10), True),
        (srange(0, 10), srange(empty=True), False),
        (srange(), srange(0, 10), False),
        (srange(0, 10), srange(), True),
        (srange(empty=True), srange(), True),
        (srange(), srange(empty=True), False),
        (srange(0, 10, '[]') + srange(20, 30), srange(0, 30, '[]'), True),
        (srange(0, 10, '[]') + srange(20, 30), srange(5, 25, '[]'), False),
        (srange(0, 10, '[]') + srange(20, 30), srange(0, 11) + srange(18, 35), True),
        (srange(0, 10, '[]') + srange(20, 30), srange(0, 11) + srange(25, 27), False),
        (srange(0, 10, '[]') + srange(20, 30), srange(0, 9) + srange(18, 35), False),
    ))
    def test__srange_unit_int__issubset(self, srange1: SetRange, srange2: SetRange, expected_issubset: bool):
        """レンジ[int]()の包含判定をテストする。
        """
        if expected_issubset:
            assert srange1.issubset(srange2)
            assert srange2.issuperset(srange1)
            assert srange1 <= srange2
            assert srange2 >= srange1

            if srange1 == srange2:
                assert not srange1 < srange2
                assert not srange2 > srange1
            else:
                assert srange1 < srange2
                assert srange2 > srange1
        else:
            assert not srange1.issubset(srange2)
            assert not srange2.issuperset(srange1)
            assert not srange1 <= srange2
            assert not srange2 >= srange1
            assert not srange1 < srange2
            assert not srange2 > srange1

    @pytest.mark.parametrize('srange1, srange2', (
        (srange(1, 5, edge='[]'), srange(None, 1, edge='()') + srange(5, None, edge='()')),
        (srange(1, 5, edge='[)'), srange(None, 1, edge='()') + srange(5, None, edge='[)')),
        (srange(1, 5, edge='(]'), srange(None, 1, edge='(]') + srange(5, None, edge='()')),
        (srange(1, 5, edge='()'), srange(None, 1, edge='(]') + srange(5, None, edge='[)')),
        (srange(empty=True), srange(None, None)),
        (srange(1, 5, edge='[]') + srange(10, 15, edge='[]'),
         srange(None, 1, edge='()') + srange(5, 10, edge='()') + srange(15, None, edge='()')),
        (srange(1, 5, edge='[]') + srange(10, 15, edge='(]'),
         srange(None, 1, edge='()') + srange(5, 10, edge='(]') + srange(15, None, edge='()')),
        (srange(1, 5, edge='[)') + srange(10, 15, edge='[]'),
         srange(None, 1, edge='()') + srange(5, 10, edge='[)') + srange(15, None, edge='()')),
        (srange(1, 5, edge='[)') + srange(10, 15, edge='(]'),
         srange(None, 1, edge='()') + srange(5, 10, edge='[]') + srange(15, None, edge='()')),
        (srange(None, 5, edge='()') + srange(5, None, edge='()'), srange(5, 5, edge='[]')),
        (srange(1, 5, edge='()') + srange(5, None, edge='()'),
         srange(None, 1, edge='(]') + srange(5, 5, edge='[]')),
        (srange(None, 5, edge='()') + srange(5, 10, edge='()'),
         srange(5, 5, edge='[]') + srange(10, None, edge='[)')),
    ))
    def test__srange_unit_int__complement(self, srange1: SetRange, srange2: SetRange):
        """レンジ[int]()の補集合をテストする。
        """
        assert srange1.complement() == srange2
        assert srange2.complement() == srange1

    @pytest.mark.parametrize('srange1, bounded_below, bounded_above', (
        (srange(1, 5, edge='[]'), True, True),
        (srange(1, 5, edge='[)'), True, True),
        (srange(1, 5, edge='(]'), True, True),
        (srange(1, 5, edge='()'), True, True),
        (srange(None, 5, edge='()'), False, True),
        (srange(1, None, edge='()'), True, False),
        (srange(None, None, edge='()'), False, False),
        (srange(empty=True), True, True),
        (srange(1, 5, edge='[]') + srange(7, 10, edge='[]'), True, True),
        (srange(None, 5, edge='[]') + srange(7, 10, edge='[]'), False, True),
        (srange(1, 5, edge='[]') + srange(7, None, edge='[]'), True, False),
        (srange(None, 5, edge='[]') + srange(7, None, edge='[]'), False, False),
    ))
    def test__srange_unit_int__bound(self, srange1: SetRange, bounded_below, bounded_above):
        """レンジ[int]()の有界判定をテストする。
        """
        assert srange1.is_bounded_below() == bounded_below
        assert srange1.is_bounded_above() == bounded_above

    @pytest.mark.parametrize('srange1, measure', (
        (srange(1, 5, edge='[]'), 4),
        (srange(1, 5, edge='[)'), 4),
        (srange(1, 5, edge='(]'), 4),
        (srange(1, 5, edge='()'), 4),
        (srange(empty=True), 0),
        (srange(1, 5, edge='()') + srange(9, 11, edge='()'), 6),
        (srange(datetime(2020, 12, 30, 11, 22, 33), datetime(2020, 12, 30, 11, 22, 34), '[]'), timedelta(seconds=1)),
    ))
    def test__srange_unit__measure(self, srange1: SetRange, measure):
        """レンジ()の測度関数をテストする。
        """
        assert srange1.measure() == measure

    @pytest.mark.parametrize('srange1', (
        srange(1, None),
        srange(None, 5),
        srange(None, None),
        srange(1, 2) + srange(5, None),
        srange(None, 2) + srange(5, 10),
        srange(None, 2) + srange(5, None),
    ))
    def test__srange_unit__measure_err(self, srange1: SetRange):
        """レンジ()の測度関数をテストする。
        """
        with pytest.raises(ValueError):
            srange1.measure()
