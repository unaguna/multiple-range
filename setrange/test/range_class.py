from setrange import srange, SetRange


class TestSetRangeClass:

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
