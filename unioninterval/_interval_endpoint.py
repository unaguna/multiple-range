class MinEndPoint:
    """レンジの始点の番兵

    どんなオブジェクトよりも小さい。
    """
    def __str__(self):
        return '-inf'

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __hash__(self):
        return hash(self.__class__)

    def __lt__(self, other):
        return self != other

    def __le__(self, other):
        return True

    def __gt__(self, other):
        return False

    def __ge__(self, other):
        return self == other


class MaxEndPoint:
    """レンジの終点の番兵

    どんなオブジェクトよりも大きい。
    """
    def __str__(self):
        return 'inf'

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __hash__(self):
        return hash(self.__class__)

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return self == other

    def __gt__(self, other):
        return self != other

    def __ge__(self, other):
        return True
