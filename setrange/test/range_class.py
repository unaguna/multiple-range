import pytest

from setrange import srange, SetRange


class TestSetRangeClass:

    def test__srange_unit_int__str(self):
        """単レンジ[int]の文字列化をテストする。
        """
        assert str(srange(empty=True)) == '(empty)'
        assert str(srange(5, 10, edge='[]')) == '[5, 10]'
        assert str(srange(5, 10, edge='[)')) == '[5, 10)'
        assert str(srange(5, 10, edge='(]')) == '(5, 10]'
        assert str(srange(5, 10, edge='()')) == '(5, 10)'

    def test__srange_unit_int__equal(self):
        """単レンジ[int]の等号演算をテストする。
        """
        set_range_1: SetRange[int] = srange(5, 10)
        set_range_2: SetRange[int] = srange(5, 10)
        set_range_x: SetRange[int] = srange(5, 9)
        set_range_ee: SetRange[int] = srange(5, 10, edge='()')
        set_range_ei: SetRange[int] = srange(5, 10, edge='(]')
        set_range_ii: SetRange[int] = srange(5, 10, edge='[]')

        assert set_range_1 == set_range_2
        assert set_range_1 != set_range_x
        assert set_range_1 != set_range_ee
        assert set_range_1 != set_range_ei
        assert set_range_1 != set_range_ii

    def test__srange_unit_int__contain(self):
        """単レンジ[int]の含有演算をテストする。

        int 型で指定した端点と比較できるオブジェクトであれば、含有するかどうか確かめられる。
        """
        set_range: SetRange[int] = srange(5, 10)

        assert 4 not in set_range
        assert 5 in set_range
        assert 9 in set_range
        assert 10 not in set_range
        assert 4.0 not in set_range
        assert 5.0 in set_range
        assert 9.0 in set_range
        assert 10.0 not in set_range

    def test__srange_unit_str__contain(self):
        """単レンジ[str]の含有演算をテストする。
        """
        set_range: SetRange[str] = srange('f', 's')

        assert 'e' not in set_range
        assert 'ea' not in set_range
        assert 'f' in set_range
        assert 'fa' in set_range
        assert 's' not in set_range
        assert 'sa' not in set_range

    def test__srange_unit_int_ie__contain(self):
        """単レンジ[int][)の含有演算をテストする。
        """
        set_range: SetRange[int] = srange(5, 10, '[)')

        assert 4 not in set_range
        assert 5 in set_range
        assert 9 in set_range
        assert 10 not in set_range
        assert 4.0 not in set_range
        assert 5.0 in set_range
        assert 9.0 in set_range
        assert 10.0 not in set_range

    def test__srange_unit_int_ei__contain(self):
        """単レンジ[int](]の含有演算をテストする。
        """
        set_range: SetRange[int] = srange(5, 10, '(]')

        assert 5 not in set_range
        assert 6 in set_range
        assert 10 in set_range
        assert 11 not in set_range
        assert 5.0 not in set_range
        assert 6.0 in set_range
        assert 10.0 in set_range
        assert 11.0 not in set_range

    def test__srange_unit_int_ii__contain(self):
        """単レンジ[int][]の含有演算をテストする。
        """
        set_range: SetRange[int] = srange(5, 10, '[]')

        assert 4 not in set_range
        assert 5 in set_range
        assert 10 in set_range
        assert 11 not in set_range
        assert 4.0 not in set_range
        assert 5.0 in set_range
        assert 10.0 in set_range
        assert 11.0 not in set_range

    def test__srange_unit_int_ee__contain(self):
        """単レンジ[int]()の含有演算をテストする。
        """
        set_range: SetRange[int] = srange(5, 10, '()')

        assert 5 not in set_range
        assert 6 in set_range
        assert 9 in set_range
        assert 10 not in set_range
        assert 5.0 not in set_range
        assert 6.0 in set_range
        assert 9.0 in set_range
        assert 10.0 not in set_range

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
    ))
    def test__srange_unit_int__add__unit(self, srange1, srange2, srange_m):
        """レンジ[int]()の加法演算 (合併) をテストする。
        """
        if isinstance(srange_m, list):
            result = srange1 + srange2
            assert not result.is_empty
            assert result._unit_list == srange_m
        else:
            result = srange1 + srange2
            assert result == srange_m
