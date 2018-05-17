"""
"""

from fractions import Fraction
from functools import lru_cache, total_ordering
import numbers

from .game import Game


@total_ordering
class Surreal(Game, numbers.Number):
    """
    """
    def __init__(G, value):
        """
        """
        G._n = Fraction(value)
        if G._n.denominator == 1:
            if G._n == 0:
                G._left = set()
                G._right = set()
            elif G._n > 0:
                G._left = {Surreal(value - 1)}
                G._right = set()
            else:
                G._left = set()
                G._right = {Surreal(value + 1)}
        else:
            G._left = {Surreal(G._n - 1/G._n.denominator)}
            G._right = {Surreal(G._n + 1/G._n.denominator)}

    @property
    def is_number(G):
        """
        """
        return True

    @property
    def is_impartial(G):
        """
        """
        return G._n == 0

    @property
    def is_switch(G):
        """
        """
        return False

    def __hash__(G):
        """
        """
        return hash(G._n)

    @lru_cache(maxsize=None)
    def __ge__(G, H):
        """
        """
        if isinstance(H, Surreal):
            return G._n >= H._n
        elif isinstance(H, Game):
            return super().__ge__(H)
        else:
            return NotImplemented

    def __eq__(G, H):
        """
        """
        if isinstance(H, Surreal):
            return Surreal(G._n == H._n)
        elif isinstance(H, Game):
            return super().__eq__(H)
        else:
            return NotImplemented

    @lru_cache(maxsize=None)
    def __add__(G, H):
        """
        """
        if isinstance(H, Surreal):
            return Surreal(G._n + H._n)
        elif isinstance(H, Game):
            return super().__add__(H)
        else:
            return NotImplemented

    @lru_cache(maxsize=None)
    def __mul__(G, H):
        """
        """
        if isinstance(H, Surreal):
            return Surreal(G._n * H._n)
        elif isinstance(H, Game):
            return super().__mul__(H)
        else:
            return NotImplemented


    @lru_cache(maxsize=None)
    def __truediv__(G, H):
        """
        """
        if isinstance(H, Surreal):
            return Surreal(G._n / H._n)
        elif isinstance(H, Game):
            return super().__truediv__(H)
        else:
            return NotImplemented


    @lru_cache(maxsize=None)
    def _invert(G):
        """
        """
        return Surreal(1/G._n)
