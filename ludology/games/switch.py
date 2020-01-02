# -*- coding: utf-8 -*-

"""
Switches.
"""

from .game import Game
from .surreal import Surreal


__all__ = [
    "Switch",
]


class Switch(Game):
    """
    Switches: the simplest hot games.

    A switch is the simplest type of "hot" game: one in which both players have
    an incentive to play. It is of the form {G_L | G_R}, where both G_L and G_R
    are numbers, and G_L > G_R.
    """

    def __init__(G, mean, temp=None):
        """
        """
        if isinstance(mean, Game) and mean.is_switch:
            G._left, G._right = mean.left, mean.right

            lf = Surreal(next(iter(G._left))).n
            rf = Surreal(next(iter(G._right))).n

            G._mean = Surreal((lf + rf) / 2)
            G._temp = Surreal((lf - rf) / 2)
        else:
            G._mean = Surreal(mean)
            G._temp = Surreal(temp)
            G._left = {Surreal(G._mean.n + G._temp.n)}
            G._right = {Surreal(G._mean.n - G._temp.n)}

    @property
    def mean(G):
        """
        The mean value of the switch.
        """
        return G._mean

    @property
    def temp(G):
        """
        The temperature of the switch.
        """
        return G._temp

    @property
    def value(G):
        """
        The value of G as a string.

        Returns
        -------
        value : str
            The value.
        """
        from .printing import switch

        return switch(G._mean, G._temp)

    @property
    def is_impartial(G):
        """
        Determine if G is impartial.

        No switch is impartial.

        Returns
        -------
        impartial : bool
            Whether G is impartial or not.
        """
        return False

    @property
    def is_dicotic(G):
        """
        Determine if G is dicotic.

        No switch is dicotic.

        Returns
        -------
        dicotic : bool
            Whether the Game is dicotic or not.
        """
        return False

    @property
    def is_infinitesimal(G):
        """
        Determine if G is infinitesimal.

        No switch is infinitesimal.

        Returns
        -------
        infinitesimal : bool
            Whether the game is infinitesimal or not.
        """
        return False

    @property
    def is_number(G):
        """
        Determine if G is a number.

        No switch is a number.

        Returns
        -------
        number : bool
            Whether G is a number or not.
        """
        return False

    @property
    def is_numberish(G):
        """
        Determine if G is numberish.

        No switch is numberish..

        Returns
        -------
        numberish : bool
            Whether G is numberish or not.
        """
        return False

    @property
    def is_switch(G):
        """
        Determine if G is a switch.

        Every switch is a switch.

        Returns
        -------
        number : bool
            Whether G is a switch or not.
        """
        return True
