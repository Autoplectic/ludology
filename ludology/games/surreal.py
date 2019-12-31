# -*- coding: utf-8 -*-

"""
The Surreal numbers are the subset of Games which are isomorophic to the hyperreals.
"""

from fractions import Fraction
from functools import lru_cache, total_ordering
import numbers

from .game import Game
from ..tools import canonicalize


@total_ordering
class Surreal(Game, numbers.Number):
    """
    The Surreal numbers are the subset of games such that G_L <= G_R, and that
    is true for all options as well. The Surreal numbers are isomorphic to the
    hyperreals. All Surreal numbers with finite birthdays correspond to the
    dyadic rationals, that is, rational numbers whose denominator is a power of
    2.
    """
    def __init__(G, value):
        """
        Construct the Surreal with given value.

        Parameters
        ----------
        value : int, float, Fraction
            The value for the Surreal number.
        """
        if isinstance(value, Surreal):
            G._left, G._right, G._n = value.left, value.right, value.n
        elif isinstance(value, Game) and value.is_number:
            value = canonicalize(value, specify=False)
            G._left, G._right = value.left, value.right

            if not G._left | G._right:
                G._n = Fraction(0)
            else:
                # non-zero dyadic rational
                if G._left:
                    lf = next(iter(G._left)).n
                if G._right:
                    rf = next(iter(G._right)).n

                if not G._right:
                    # positive integer
                    G._n = lf + 1
                elif not G._left:
                    # negative integer
                    G._n = rf - 1
                else:
                    # dyadic rational
                    G._n = (lf + rf) / 2
        else:
            try:
                G._n = Fraction(value)
                if G._n.denominator > 1024:
                    msg = f"{G._n} would result in a very deep game tree."
                    raise ValueError(msg)
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
            except ValueError:
                raise ValueError(f"Can not convert {value} to a Surreal Number.")

    @property
    def n(G):
        """
        The Surreal's value, as a Fraction.
        """
        return G._n

    @property
    def is_number(G):
        """
        Whether the Surreal number is a number or not. By definition, this is True.

        Returns
        -------
        number : bool
            Whether this number is a number (True).
        """
        return True

    @property
    def is_numberish(G):
        """
        A Game is numberish if it is infinitesimally close to a number. All Numbers are numberish.

        Returns
        -------
        numberish : bool
            Whether G is numberish or not (it is).
        """
        return True

    @property
    def is_impartial(G):
        """
        Whether the Surreal number is impartial or not. Only the Surreal 0 is impartial.

        Returns
        -------
        impartial : bool
            Whether this number is impartial.
        """
        return G._n == 0

    @property
    def is_dicotic(G):
        """
        Whether the Surreal number is dicotic or not. Only the Surreal 0 is dicotic.

        Returns
        -------
        dicotic : bool
            Whether this number is dicotic.
        """
        return G._n == 0

    @property
    def is_infinitesimal(G):
        """
        A game is infinitesimal if it is non-zero and smaller than any positive number and greater
        than any negative number. Equivalently, it's left and right stops are both zero. Note, this
        does not imply that an infinitesimal can not be positive (> 0) or negative (< 0).

        Returns
        -------
        infinitesimal : bool
            Whether the Surreal is infinitesimal or not (it is not).
        """
        return False

    @property
    def is_switch(G):
        """
        Whether the Surreal number is a switch or not. By definition, this is not the case.

        Returns
        -------
        switch : bool
            Whether this number is a switch (it is not).
        """
        return False

    def __hash__(G):
        """
        Define the hash of a Surreal as the hash of its value.

        Returns
        -------
        hash : str
            The hash of G.
        """
        return super().__hash__()

    @lru_cache(maxsize=None)
    def __ge__(G, H):
        """
        Test if one Surreal is greather than or equal to another.

        Parameters
        ----------
        H : Surreal, Game
            The second Surreal/Game.

        Returns
        ge : bool
            Whether G >= H or not.
        """
        if isinstance(H, Surreal):
            return G._n >= H._n
        if isinstance(H, numbers.Number):
            return G._n >= H
        if isinstance(H, Game):
            return super().__ge__(H)

        return NotImplemented

    def __eq__(G, H):
        """
        Test if one Surreal is equal to another.

        Parameters
        ----------
        H : Surreal, Game
            The second Surreal/Game.

        Returns
        eq : bool
            Whether G == H or not.
        """
        if isinstance(H, Surreal):
            return G._n == H._n
        if isinstance(H, numbers.Number):
            return G._n == H
        if isinstance(H, Game):
            return super().__eq__(H)

        return NotImplemented

    @lru_cache(maxsize=None)
    def __add__(G, H):
        """
        The sum of two Surreals.

        Parameters
        ----------
        H : Surreal, Game
            The second Surreal/Game.

        Returns
        -------
        sum : Surreal
            The sum of G and H.
        """
        if isinstance(H, Surreal):
            return Surreal(G._n + H._n)
        if isinstance(H, numbers.Number):
            return Surreal(G._n + H)
        if isinstance(H, Game):
            return super().__add__(H)

        return NotImplemented

    @lru_cache(maxsize=None)
    def __mul__(G, H):
        """
        The product of two Surreals.

        Parameters
        ----------
        H : Surreal, Game
            The second Surreal/Game.

        Returns
        -------
        prod : Surreal
            The product of G and H.
        """
        if isinstance(H, Surreal):
            return Surreal(G._n * H._n)
        if isinstance(H, numbers.Number):
            return Surreal(G._n * H)
        if isinstance(H, Game):
            return super().__mul__(H)

        return NotImplemented

    @lru_cache(maxsize=None)
    def __pow__(G, H):
        """
        G ** H = exp(G * log(H))
        """
        return NotImplemented

    @lru_cache(maxsize=None)
    def __truediv__(G, H):
        """
        The quotient of a Surreal by another.

        Parameters
        ----------
        H : Surreal, Game
            The second Surreal/Game.

        Returns
        -------
        div : Surreal
            The quotient of G by H.
        """
        if isinstance(H, Surreal):
            return Surreal(G._n / H._n)
        if isinstance(H, numbers.Number):
            return Surreal(G._n / H)
        if isinstance(H, Game):
            return super().__truediv__(H)

        return NotImplemented

    @lru_cache(maxsize=None)
    def _invert(G):
        """
        The inverse of G.

        Returns
        -------
        Ginv : Surreal
            The inverse of G.
        """
        return Surreal(1/G._n)

    @property
    def value(G):
        """
        The value of G.

        Returns
        -------
        value : str
            The value as a string.
        """
        from .printing import unicode_fraction

        return unicode_fraction(G._n.numerator, G._n.denominator)
