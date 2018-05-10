"""
"""

from .game import Game
from .utils import mex

class Nimber(Game):
    """
    """
    def __init__(self, n):
        """
        """
        if n == 0:
            options = set()
        else:
            options = {Nimber(i) for i in range(n)}
        self._left = self._right = options
        self._n = n

    @property
    def value(G):
        """
        """
        if G._n == 0:
            return '0'
        elif G._n == 1:
            return '*'
        else:
            return f"*{G._n}"

    @property
    def is_number(G):
        """
        """
        return False

    @property
    def is_impartial(G):
        """
        """
        return True

    @property
    def birthday(G):
        """
        """
        return G._n

    def __neg__(G):
        """
        """
        return G

    def __add__(G, H):
        """
        """
        if isinstance(H, Nimber):
            return Nimber(G._n ^ H._n)
        elif isinstance(H, Game):
            return super().__add__(H)
        else:
            return NotImplemented

    def __radd__(G, H):
        """
        """
        return G.__add__(H)

    def __mul__(G, H):
        """
        """
        if isinstance(H, Nimber):
            return Nimber(_mul(G._n, H._n))
        elif isinstance(H, Game):
            return super().__mul__(H)
        else:
            return NotImplemented

    def __rmul__(G, H):
        """
        """
        return G.__mul__(H)

def _mul(n1, n2):
    """
    """
    return mex({_mul(a, n2) ^ _mul(n1, b) ^ _mul(a, b) for a in range(n1) for b in range(n2)})