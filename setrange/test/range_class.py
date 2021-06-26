import pytest

from setrange import srange


class TestSetRangeClass:

    @pytest.mark.parametrize('set_range, expected_str', (
            (srange(empty=True), '(empty)'),
            (srange(5, 10, edge='[]'), '[5, 10]'),
            (srange(5, 10, edge='[)'), '[5, 10)'),
            (srange(5, 10, edge='(]'), '(5, 10]'),
            (srange(5, 10, edge='()'), '(5, 10)'),
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
    ))
    def test__srange_unit_int__equal(self, set_range_1, set_range_2, expected_equal):
        """単レンジ[int]の等号演算をテストする。
        """
        if expected_equal:
            assert set_range_1 == set_range_2
            assert set_range_2 == set_range_1
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
            (srange('f', 's'), 'e', False),
            (srange('f', 's'), 'ee', False),
            (srange('f', 's'), 'f', True),
            (srange('f', 's'), 'fa', True),
            (srange('f', 's'), 's', False),
            (srange('f', 's'), 'sa', False),
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
            # 一方が空のパターン
            (srange(5, 6, '[]'), srange(empty=True), srange(5, 6, '[]')),
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
            # 少なくとも一方が空の単レンジであるパターン
            (srange(empty=True), srange(7, 9, '[]'), srange(empty=True)),
            (srange(empty=True), srange(7, 9, '[)'), srange(empty=True)),
            (srange(empty=True), srange(7, 9, '(]'), srange(empty=True)),
            (srange(empty=True), srange(7, 9, '()'), srange(empty=True)),
            (srange(empty=True), srange(empty=True), srange(empty=True)),
            (srange(empty=True), srange(empty=True), srange(empty=True)),
            (srange(empty=True), srange(empty=True), srange(empty=True)),
            (srange(empty=True), srange(empty=True), srange(empty=True)),
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
