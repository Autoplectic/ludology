"""
"""

from copy import copy
from functools import lru_cache


__all__ = [
    'canonicalize',
    'left_incentives',
    'right_incentives',
    'left_stop',
    'right_stop',
]


@lru_cache(maxsize=None)
def left_incentives(G):
    """
    Compute the left incentives of G:

        { G_L - G }

    Parameters
    ----------
    G : Game
        The game of interest.

    Returns
    -------
    incentives : set
        The left incentives of G.
    """
    return {simplify(G_L - G) for G_L in G._left}


@lru_cache(maxsize=None)
def right_incentives(G):
    """
    Compute the right incentives of G:

        { G - G_R }

    Parameters
    ----------
    G : Game
        The game of interest.

    Returns
    -------
    incentives : set
        The right incentives of G.
    """
    return {simplify(G - G_R) for G_R in G._right}


def stop_order(item):
    """
    if x > y:
        x_- > x_+ > y_- > y_+

    since L is lexicographically less than R, we
    can't rely on natural ordering.
    """
    g, s = item
    return (g, s == '-')


@lru_cache(maxsize=None)
def left_stop(G):
    """
    Compute the left stop of G.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    LS : Game
        The left stop of G.
    initiative : str
        '+' if it is left's turn, '-' if right's.
    """
    if G.is_number:
        return (G, '+')
    else:
        return max((right_stop(G_L) for G_L in G._left), key=stop_order)


@lru_cache(maxsize=None)
def right_stop(G):
    """
    Compute the right stop of G.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    RS : Game
        The right stop of G.
    initiative : str
        '+' if it is left's turn, '-' if right's.
    """
    if G.is_number:
        return (G, '-')
    else:
        return min((left_stop(G_R) for G_R in G._right), key=stop_order)


def remove_dominated(G):
    """
    """
    G._left = {g for g in G._left if not any(g < G_L for G_L in G._left)}
    G._right = {g for g in G._right if not any(g > G_R for G_R in G._right)}


def replace_reversible(G):
    """
    """
    new_left_set = set()
    for G_L in G._left:
        for G_LR in G_L._right:
            if G_LR <= G:  # G_L is reversible through G_LR
                for G_LRL in G_LR._left:
                    new_left_set.add(G_LRL)
                break
        else:   # Not reversible
            new_left_set.add(G_L)
    G._left = new_left_set

    new_right_set = set()
    for G_R in G._right:
        for G_RL in G_R._left:
            if G_RL >= G:  # G_R is reversible through G_RL
                for G_RLR in G_RL._right:
                    new_right_set.add(G_RLR)
                break
        else:  # Not reversible
            new_right_set.add(G_R)
    G._right = new_right_set


def simplify(G):
    """
    """
    G = copy(G)

    G._left = {simplify(G_L) for G_L in G._left}
    G._right = {simplify(G_R) for G_R in G._right}

    old_left, old_right = set(), set()
    while G._left != old_left or G._right != old_right:
        old_left, old_right = G._left, G._right
        remove_dominated(G)
        replace_reversible(G)

    return G


canonicalize = simplify
