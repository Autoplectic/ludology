"""
"""

from fractions import Fraction
import numbers

from .game import Game

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
