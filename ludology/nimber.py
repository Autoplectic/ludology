"""
Nimbers are the values of impartial games.
"""

from functools import lru_cache
from itertools import count
from math import inf

from .game import Game
from .utils import mex


__all__ = [
    'Nimber',
    'FarStar',
]


class Nimber(Game):
    """
    A Nimber is the value of an impartial game.
    """
    def __init__(G, n):
        """
        Construct the `n`th Nimber.

        Parameters
        ----------
        n : int >= 0
            The value of Nimber to construct.
        """
        if n == 0:
            options = set()
        elif isinstance(n, int):
            options = {Nimber(i) for i in range(n)}
        else:
            msg = "Nimbers must have an integer value."
            raise ValueError(msg)

        G._left = G._right = options
        G._n = n

    @property
    def value(G):
        """
        Return the value of the Nimber.

        Returns
        -------
        v : str
            The value of `G`.
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
        Whether the Nimber is a number or not. Only the Nimber 0 is a number.

        Returns
        -------
        number : bool
            Whether the Nimber is a number or not.
        """
        return G._n == 0

    @property
    def is_numberish(G):
        """
        A Game is numberish if it is infinitesimally close to a number. All Nimbers are numberish.

        Returns
        -------
        numberish : bool
            Whether G is numberish or not (it is).
        """
        return True

    @property
    def is_impartial(G):
        """
        Whether the Nimber is impartial or not. All Nimbers are impartial.

        Returns
        -------
        impartial : bool
            Whether the Nimber is impartial or not.
        """
        return True

    @property
    def is_infinitesimal(G):
        """
        A game is infinitesimal if it is non-zero and smaller than any positive number and greater
        than any negative number. Equivalently, it's left and right stops are both zero. Note, this
        does not imply that an infinitesimal can not be positive (> 0) or negative (< 0).

        Returns
        -------
        infinitesimal : bool
            Whether the Nimber is infinitesimal or not (it is, unless it is zero).
        """
        return G._n != 0

    @property
    def is_dicotic(G):
        """
        A dicotic, or all-small, Game is one where either both or neither player have options
        at every subposition. All Nimbers are dicotic by definition of an impartial game.

        Returns
        -------
        dicotic : bool
            Whether the Game is dicotic or not (it is).
        """
        return True

    @property
    def birthday(G):
        """
        The Nimber's birthday.

        Returns
        -------
        bday : int >= 0
            The Nimber's birthday.
        """
        return G._n

    def __neg__(G):
        """
        The negation of the Nimber `G`. A Nimber is its own inverse.

        Returns
        -------
        G : Nimber
            The Nimber's inverse.
        """
        return G

    @lru_cache(maxsize=None)
    def __add__(G, H):
        """
        The sum of two Nimbers.

        Parameters
        ----------
        H : Nimber, Game
            The Nimber or Game to add by.

        Returns
        -------
        sum : Nimber, Game
            The sum of G and H.
        """
        if isinstance(H, Nimber):
            return Nimber(G._n ^ H._n)
        elif isinstance(H, Game):
            return super().__add__(H)
        else:
            return NotImplemented

    @lru_cache(maxsize=None)
    def __mul__(G, H):
        """
        The product of two Nimbers.

        Parameters
        ----------
        H : Nimber, Game
            The Nimber or Game to multiply by.

        Returns
        -------
        prod : Nimber, Game
            The product of G and H.
        """
        if isinstance(H, Nimber):
            return Nimber(_mul(G._n, H._n))
        elif isinstance(H, Game):
            return super().__mul__(H)
        else:
            return NotImplemented

    def __eq__(G, H):
        """
        The equality of two Nimbers.

        Parameters
        ----------
        H : Nimber, Game
            The Nimber or Game equate to `G`.

        Returns
        -------
        eq : Nimber, Game
            The equality of G and H.
        """
        if isinstance(H, Nimber):
            return G._n == H._n
        elif isinstance(H, Game):
            return super().__eq__(H)
        else:
            return NotImplemented

    def __hash__(G):
        """
        Define the hash of a Nimber as the hash of its value.

        Returns
        -------
        hash : str
            The hash of G.
        """
        return hash(G._n)


class FarStar(Nimber):
    """
    The far-star represents an arbitrarily large Nimber.
    """
    def __init__(G):
        """
        """
        G._n = inf

    @property
    def _left(G):
        """
        The "left set" of far-star.
        """
        return (Nimber(i) for i in count())  # pragma: no branch

    @property
    def _right(G):
        """
        The "right set" of far-star.
        """
        return (Nimber(i) for i in count())  # pragma: no branch

    @property
    def value(G):
        """
        A white star is used to represented far-star.
        """
        return "☆"

    def __add__(G, H):
        """
        The sum of far-star with any Nimber is far-star.

        Parameters
        ----------
        H : Nimber
            The Nimber to add to far-star.

        Returns
        -------
        fs : FarStar
            The far-star.
        """
        if isinstance(H, Nimber):
            return FarStar()
        else:
            return NotImplemented


def _mul(n1, n2):
    """
    The nimber product of `n1` and `n2`.

    Parameters
    ----------
    n1 : int
        The first nimber.
    n2 : int
        The second nimber.

    Returns
    -------
    prod : int
        The
    """
    return mex({_mul(a, n2) ^ _mul(n1, b) ^ _mul(a, b) for a in range(n1) for b in range(n2)})
