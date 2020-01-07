# -*- coding: utf-8 -*-

"""
Switches.
"""

import numbers

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

    def __init__(G, left=None, right=None):
        """
        Construct the Switch.

        Parameters
        ----------
        left : set
            The left set.
        right : set
            The right set.
        """
        if not left or not right:
            msg = "The left and right sets must not be empty."
            raise ValueError(msg)
        if not all(opt.is_number for opt in left | right):
            msg = "All options must be numbers."
            raise ValueError(msg)
        left = {Surreal(G_L.left, G_L.right) for G_L in left}
        right = {Surreal(G_R.left, G_R.right) for G_R in right}
        max_left = max(left)
        min_right = min(right)

        if max_left <= min_right:
            msg = "The confusion interval has zero length."
            raise ValueError(msg)

        G._left = left
        G._right = right
        G._mean = Surreal.from_value((max_left.n + min_right.n) / 2)
        G._temperature = Surreal.from_value((max_left.n - min_right.n) / 2)

    @classmethod
    def from_mean_and_temperature(cls, mean, temperature):
        """
        Construct a Switch from its mean value and temperature.

        Parameters
        ----------
        mean : Number, Surreal
            The mean value.
        temperature : Number, Surreal
            The temperature.
        """
        if not isinstance(mean, Surreal):
            if isinstance(mean, numbers.Number):
                mean = Surreal.from_value(mean)
            elif isinstance(mean, Game):
                mean = Surreal(left=mean.left, right=mean.right)
            else:
                msg = f"Can not convert {mean} to a Surreal."
                raise ValueError(msg)
        if not isinstance(temperature, Surreal):
            if isinstance(temperature, numbers.Number):
                temperature = Surreal.from_value(temperature)
            elif isinstance(temperature, Game):
                temperature = Surreal(left=temperature.left, right=temperature.right)
            else:
                msg = f"Can not convert {temperature} to a Surreal."
                raise ValueError(msg)

        return cls(left={mean + temperature}, right={mean - temperature})

    @property
    def mean(G):
        """
        The mean value of the switch.
        """
        return G._mean

    @property
    def temperature(G):
        """
        The temperature of the switch.
        """
        return G._temperature

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

        return switch(G._mean, G._temperature)

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
