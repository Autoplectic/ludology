# -*- coding: utf-8 -*-

"""
Nimbers are the values of impartial games.
"""

import numbers
from functools import lru_cache
from itertools import count
from math import inf

from .game import Game
from ..utils import mex


__all__ = [
    'Nimber',
    'FarStar',
]


class Nimber(Game):
    """
    Nimbers: Impartial Games.

    A Nimber is the value of an impartial game. They are an important and well
    understood subset of Games.
    """

    def __init__(G, n):
        """
        Construct the nth Nimber.

        Parameters
        ----------
        n : int >= 0
            The value of Nimber to construct.
        """
        if n == 0:
            options = set()
        elif isinstance(n, int):
            options = {Nimber(i) for i in range(n)}
        elif isinstance(n, Game) and n.is_impartial:
            options = {Nimber(i) for i in range(len(n._left))}
        else:
            msg = "Nimbers must have an integer value."
            raise ValueError(msg)

        G._left = G._right = options
        G._n = len(G._left)

    @property
    def n(G):
        """
        The Nimber's integer value.

        Returns
        -------
        n : int
            The integer value of the Nimber.
        """
        return G._n

    @property
    def value(G):
        """
        The value of the Nimber.

        Returns
        -------
        v : str
            The value of `G`.
        """
        if G._n == 0:
            return '0'
        if G._n == 1:
            return '∗'
        return f"∗{G._n}"

    @property
    def is_number(G):
        """
        Determine if G is a number.

        Only the Nimber 0 is a number.

        Returns
        -------
        number : bool
            Whether the Nimber is a number or not.
        """
        return G._n == 0

    @property
    def is_numberish(G):
        """
        Determine if G is numberish.

        A Game is numberish if it is infinitesimally close to a number. All
        Nimbers are numberish.

        Returns
        -------
        numberish : bool
            Whether G is numberish or not (it is).
        """
        return True

    @property
    def is_impartial(G):
        """
        Determine if G is impartial.

        A Game is impartial if its left and right options are the same, all its
        options are impartial. All Nimbers are impartial.

        Returns
        -------
        impartial : bool
            Whether the Nimber is impartial or not.
        """
        return True

    @property
    def is_infinitesimal(G):
        """
        Determine if G is infinitesimal.

        A game is infinitesimal if it is non-zero and smaller than any positive
        number and greater than any negative number. Equivalently, it's left and
        right stops are both zero. Note, this does not imply that an
        infinitesimal can not be positive (> 0) or negative (< 0).

        Returns
        -------
        infinitesimal : bool
            Whether the Nimber is infinitesimal or not (it is, unless it is zero).
        """
        return G._n != 0

    @property
    def is_dicotic(G):
        """
        Determine if G is dicotic.

        A dicotic, or all-small, Game is one where either both or neither player have options
        at every subposition. All Nimbers are dicotic by definition of an impartial game.

        Returns
        -------
        dicotic : bool
            Whether the Game is dicotic or not (it is).
        """
        return True

    @property
    def is_switch(G):
        """
        Determine if G is a switch.

        No Nimbers are switches.

        Returns
        -------
        number : bool
            Whether G is a switch or not.
        """
        return False

    @property
    def birthday(G):
        """
        The Nimber's birthday.

        The birthday of a Nimber is its integer value.

        Returns
        -------
        bday : int >= 0
            The Nimber's birthday.
        """
        return G._n

    def __neg__(G):
        """
        Compute the negation of the Nimber `G`.

        A Nimber is its own inverse.

        Returns
        -------
        G : Nimber
            The Nimber's inverse.
        """
        return G

    @lru_cache(maxsize=None)
    def __add__(G, H):
        """
        Compute the sum of G and H.

        The sum of two Nimbers is equal it their mex (maximum excluded element),
        which can be found via their exclusive or.

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
        if isinstance(H, (Game, numbers.Number)):
            return super().__add__(H)

        return NotImplemented

    @lru_cache(maxsize=None)
    def __mul__(G, H):
        """
        Compute the product of G and H.

        The product of two Nimbers can be found using a simple recursive
        formula:
        .. math::
           mex(G' * H + G * H' + G' * H') for all G' < G and H' < H

        where * and + are nimber products and sums, respectively.

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
        if isinstance(H, (Game, numbers.Number)):
            return super().__mul__(H)

        return NotImplemented

    def __eq__(G, H):
        """
        Determine if G equals H.

        Two Nimbers are equal if their integer values are equal.

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
        if isinstance(H, (Game, numbers.Number)):
            return super().__eq__(H)

        return NotImplemented

    def __hash__(G):
        """
        Construct the hash for G.

        Use the parent class Game's hash. We must specifically do it here
        because __eq__ is defined for this class.

        Returns
        -------
        hash : str
            The hash of G.
        """
        return super().__hash__()


class FarStar(Nimber):
    """
    The Far-Star.

    The Far-Star represents an arbitrarily large Nimber, and is useful for
    evaluating outcome class of many dicotic games.
    """

    def __init__(G):
        """
        Construct the Far-Star.
        """
        G._n = inf

    @property
    def left(G):
        """
        The "left set" of Far-Star.

        Returns
        -------
        left_set : generator
            All nimbers.
        """
        return (Nimber(i) for i in count())  # pragma: no branch

    @property
    def right(G):
        """
        The "right set" of Far-Star.

        Returns
        -------
        right_set : generator
            All nimbers.
        """
        return (Nimber(i) for i in count())  # pragma: no branch

    @property
    def value(G):
        """
        The value of G.

        A white star is used to represented Far-Star.

        Returns
        -------
        star : str
            The value of Far-Star.
        """
        return "☆"

    def __add__(G, H):
        """
        Compute the sum of G and H.

        The sum of Far-Star with any Nimber is Far-Star.

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
    Compute the Nimber product of `n1` and `n2`.

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
