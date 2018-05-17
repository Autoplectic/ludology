"""
The Surreal numbers are the subset of Games which are isomorophic to the hyperreals.
"""

from fractions import Fraction
from functools import lru_cache, total_ordering
import numbers

from .game import Game


@total_ordering
class Surreal(Game, numbers.Number):
    """
    The Surreal numbers are the subset of games such that G_L <= G_R, and that is
    true for all options as well. The Surreal numbers are isomorphic to the hyperreals.
    All Surreal numbers with finite birthdays correspond to the dyadic rationals, that is,
    rational numbers whose denominator is a power of 2.
    """
    def __init__(G, value):
        """
        Construct the Surreal with given value.

        Parameters
        ----------
        value : int, float, Fraction
            The value for the Surreal number.
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
        Whether the Surreal number is a number or not. By definition, this is True.

        Parameters
        ----------
        G : Surreal
            The Surreal of interest.

        Returns
        -------
        number : bool
            Whether this number is a number (True).
        """
        return True

    @property
    def is_impartial(G):
        """
        Whether the Surreal number is impartial or not. Only the Surreal 0 is impartial.

        Parameters
        ----------
        G : Surreal
            The Surreal of interest.

        Returns
        -------
        impartial : bool
            Whether this number is impartial.
        """
        return G._n == 0

    @property
    def is_switch(G):
        """
        Whether the Surreal number is a switch or not. By definition, this is not the case.

        Parameters
        ----------
        G : Surreal
            The Surreal of interest.

        Returns
        -------
        switch : bool
            Whether this number is a switch (it is not).
        """
        return False

    def __hash__(G):
        """
        Define the hash of a Surreal as the hash of its value.

        Parameters
        ----------
        G : Surreal
            The Surreal of interest.

        Returns
        -------
        hash : str
            The hash of G.
        """
        return hash(G._n)

    @lru_cache(maxsize=None)
    def __ge__(G, H):
        """
        Test if one Surreal is greather than or equal to another.

        Parameters
        ----------
        G : Surreal
            The first Surreal.
        H : Surreal, Game
            The second Surreal/Game.

        Returns
        ge : bool
            Whether G >= H or not.
        """
        if isinstance(H, Surreal):
            return G._n >= H._n
        elif isinstance(H, Game):
            return super().__ge__(H)
        else:
            return NotImplemented

    def __eq__(G, H):
        """
        Test if one Surreal is equal to another.

        Parameters
        ----------
        G : Surreal
            The first Surreal.
        H : Surreal, Game
            The second Surreal/Game.

        Returns
        eq : bool
            Whether G == H or not.
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
        The sum of two Surreals.

        Parameters
        ----------
        G : Surreal
            The first Surreal.
        H : Surreal, Game
            The second Surreal/Game.

        Returns
        -------
        sum : Surreal
            The sum of G and H.
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
        The product of two Surreals.

        Parameters
        ----------
        G : Surreal
            The first Surreal.
        H : Surreal, Game
            The second Surreal/Game.

        Returns
        -------
        prod : Surreal
            The product of G and H.
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
        The quotient of a Surreal by another.

        Parameters
        ----------
        G : Surreal
            The first Surreal.
        H : Surreal, Game
            The second Surreal/Game.

        Returns
        -------
        div : Surreal
            The quotient of G by H.
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
        The inverse of G.

        Parameters
        ----------
        G : Surreal
            The Surreal of interest.

        Returns
        -------
        Ginv : Surreal
            The inverse of G.
        """
        return Surreal(1/G._n)
