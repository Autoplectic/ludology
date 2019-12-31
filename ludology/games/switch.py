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
    A switch is the simplest type of "hot" game: one in which both players have
    an incentive to play.
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
        Return the value of G as a string.

        Returns
        -------
        value : str
            The value.
        """
        from .printing import switch

        return switch(G._mean, G._temp)
