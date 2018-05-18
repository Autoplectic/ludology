"""
Various tools for computing properties of Games.
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
    return {canonicalize(G_L - G) for G_L in G._left}


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
    return {canonicalize(G - G_R) for G_R in G._right}


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
def left_stop(G, adorn=True):
    """
    Compute the (adorned) left stop of G.

    Parameters
    ----------
    G : Game
        The Game of interest.
    adorn : bool
        Whether to adorn the stop or not. Defaults to True.

    Returns
    -------
    LS : Game
        The left stop of G.
    initiative : str
        '+' if it is left's turn, '-' if right's. Only returned if adorn is True.
    """
    if G.is_number:
        ls = (G, '+')
    else:
        ls = max((right_stop(G_L) for G_L in G._left), key=stop_order)

    if adorn:
        return ls
    else:
        return ls[0]


@lru_cache(maxsize=None)
def right_stop(G, adorn=True):
    """
    Compute the (adorned) right stop of G.

    Parameters
    ----------
    G : Game
        The Game of interest.
    adorn : bool
        Whether to adorn the stop or not. Defaults to True.

    Returns
    -------
    RS : Game
        The right stop of G.
    initiative : str
        '+' if it is left's turn, '-' if right's. Only returned if adorn is True.
    """
    if G.is_number:
        rs = (G, '-')
    else:
        rs = min((left_stop(G_R) for G_R in G._right), key=stop_order)

    if adorn:
        return rs
    else:
        return rs[0]


def remove_dominated(G):
    """
    Remove the dominated options of G.

    A left option is dominated if there exists another left option greater than
    it. A right option is dominated if there exists another right option less
    than it. In essence, it would always be a "bad idea" to move to a dominated
    option, because there exists a different option which was objectively and
    strictly superior.

    Parameters
    ----------
    G : Game
        The Game of interest.
    """
    G._left = {g for g in G._left if not any(g < G_L for G_L in G._left)}
    G._right = {g for g in G._right if not any(g > G_R for G_R in G._right)}


def replace_reversible(G):
    """
    Remove the reversable options of G.

    A left option is reversible if it has a right option which is less than G.
    In this case, that left option can be replaced with it's right option's left options.
    Essentially, this means that if left were to make a move to an option from which right
    has the ability to move to a position which is strictly better for her than G, it is a
    "no brainer" to do so, and so that left option might as well be replaced with the options
    available after right makes the obvious responce.

    Parameters
    ----------
    G : Game
        The Game of interest.
    """
    new_left_set = set()
    for G_L in G._left:
        for G_LR in G_L._right:
            if G_LR <= G:  # G_L is reversible through G_LR
                for G_LRL in G_LR._left:
                    new_left_set.add(G_LRL)
                break
        else:  # Not reversible
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


def canonicalize(G):
    """
    Return the canonical form of the game G.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    K : Game
        The Game G in canonical form.
    """
    G = copy(G)

    G._left = {canonicalize(G_L) for G_L in G._left}
    G._right = {canonicalize(G_R) for G_R in G._right}

    old_left, old_right = set(), set()
    while G._left != old_left or G._right != old_right:
        old_left, old_right = G._left, G._right
        remove_dominated(G)
        replace_reversible(G)

    return G
