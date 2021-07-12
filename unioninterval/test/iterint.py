import pytest

from unioninterval import interval, UnionInterval, iterint


class TestIterint:

    @pytest.mark.parametrize('interval1, interval2, expected_equal', (
        (interval(1, 10, edge='[]'), interval(1, 10, edge='[]'), True),
        (interval(1, 10, edge='[)'), interval(1, 10, edge='[)'), True),
        (interval(1, 10, edge='(]'), interval(1, 10, edge='(]'), True),
        (interval(1, 10, edge='()'), interval(1, 10, edge='()'), True),
        (interval(1, 10), interval(1, 9), False),
        (interval(1, 10, edge='[]'), interval(1, 10, edge='[)'), False),
        (interval(1, 10, edge='[]'), interval(1, 11, edge='[)'), True),
        (interval(1, 10, edge='[]'), interval(1, 10, edge='(]'), False),
        (interval(1, 10, edge='[]'), interval(0, 10, edge='(]'), True),
        (interval(1, 10, edge='[]'), interval(0.9, 10.1, edge='[]'), True),
        (interval(1, 10, edge='[]'), interval(0.9, 10.1, edge='[)'), True),
        (interval(1, 10, edge='[]'), interval(0.9, 10.1, edge='(]'), True),
        (interval(1, 10, edge='[]'), interval(0.9, 10.1, edge='()'), True),
        (interval(1, 3, edge='[]') + interval(4, 6, edge='[]'), interval(1, 6, edge='[]'), True),
        (interval(1, 3, edge='[)') + interval(4, 6, edge='[]'), interval(1, 6, edge='[]'), False),
        (interval(1, 3, edge='[)') + interval(4, 6, edge='[]'),
         interval(1, 3, edge='[)') + interval(4, 7, edge='[)'), True),
        (interval(1, 2, edge='[)'), interval(singleton=1), True),
        (interval(1, 2, edge='(]'), interval(singleton=2), True),
        (interval(1, 2, edge='()'), interval(empty=True), True),
    ))
    def test__iterint__equal(self, interval1: UnionInterval, interval2: UnionInterval, expected_equal):
        """iterint の等号演算をテストする。
        """
        if expected_equal:
            assert iterint(interval1) == iterint(interval2)
            assert not iterint(interval1) != iterint(interval2)
        else:
            assert not iterint(interval1) == iterint(interval2)
            assert iterint(interval1) != iterint(interval2)

    @pytest.mark.parametrize('interval1, int_list', (
        (interval(1, 5, edge='[]'), [1, 2, 3, 4, 5]),
        (interval(1, 5, edge='[)'), [1, 2, 3, 4]),
        (interval(1, 5, edge='(]'), [2, 3, 4, 5]),
        (interval(1, 5, edge='()'), [2, 3, 4]),
        (interval(0.9, 5.1, edge='[]'), [1, 2, 3, 4, 5]),
        (interval(0.9, 5.1, edge='[)'), [1, 2, 3, 4, 5]),
        (interval(0.9, 5.1, edge='(]'), [1, 2, 3, 4, 5]),
        (interval(0.9, 5.1, edge='()'), [1, 2, 3, 4, 5]),
        (interval(1, 3, edge='[]') + interval(5, 7, edge='[]'), [1, 2, 3, 5, 6, 7]),
        (interval(1, 3, edge='[]') + interval(5, 7, edge='[)'), [1, 2, 3, 5, 6]),
        (interval(1, 3, edge='[]') + interval(5, 7, edge='(]'), [1, 2, 3, 6, 7]),
        (interval(1, 3, edge='[]') + interval(5, 7, edge='()'), [1, 2, 3, 6]),
    ))
    def test__iterint__iter(self, interval1: UnionInterval, int_list):
        """iterint のイテレータをテストする。
        """
        assert list(iterint(interval1)) == int_list
