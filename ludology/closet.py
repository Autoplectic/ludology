# -*- coding: utf-8 -*-

"""
A collection of common games.
"""

from .games import Game, Nimber, Surreal, Switch
from .tools import canonicalize


__all__ = [
    'g1',
    'g2',
    'g3',
    'g4',
    'g5',
    'half',
    'miny',
    'one',
    'pm_one',
    'quarter',
    'star',
    'star2',
    'tiny',
    'two',
    'up',
    'uptimal',
    'zero',
]


# numbers
zero = Surreal.from_value(0)
one = Surreal.from_value(1)
two = Surreal.from_value(2)
half = Surreal.from_value(1 / 2)
quarter = Surreal.from_value(1 / 4)

# nimbers
star = Nimber.from_integer(1)
star2 = Nimber.from_integer(2)

# other infinitesimals
up = Game({zero}, {star})
upstar = Game({zero}, {zero, star})

# switch
pm_one = Switch.from_mean_and_temperature(mean=zero, temperature=one)

# more complex examples
g1 = canonicalize(Game({5 / 2, Game({4}, {2})}, {Game({0}, {-4}), Game({-1}, {-2})}))
g2 = canonicalize(Game({Game({4}, {2})}, {Game({Game({0}, {-2})}, {Game({-4}, {-6})})}))
g3 = canonicalize(Game({Game({3}, {one + star})}, {Game({-one + star}, {-two + star}), Game({0}, {-3})}))
g4 = canonicalize(Game({5}, {Game({1}, {-9})}))
g5 = canonicalize(Game({Game({2}, {0}), Game({2}, {star})}, {Game({0}, {-2 + star}), Game({star}, {-2 + star})}))


# Factories for specific game types.
def tiny(G):
    """
    Construct a Tiny Game: {0 || 0 | -G}.

    Parameters
    ----------
    G : Game
        The Game to make Tiny.

    Returns
    -------
    T : Game
        {0 || 0 | G}
    """
    return canonicalize(Game({0}, {Game({0}, {-G})}))


def miny(G):
    """
    Construct a Miny Game: {G | 0 || 0}.

    Parameters
    ----------
    G : Game
        The Game to make Miny.

    Returns
    -------
    M : Game
        {-G | 0 || 0}
    """
    return -tiny(G)


def uptimal(*nums):
    """
    Construct an Uptimal.

    Parameters
    ----------
    nums : [int]
        The uptimal values

    Returns
    -------
    U : Game
        The uptimal.
    """
    raise NotImplementedError
