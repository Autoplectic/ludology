# -*- coding: utf-8 -*-

"""
Various tools for computing properties of Games.
"""

from functools import lru_cache

from .canonical_form import canonical_form


__all__ = [
    'left_incentives',
    'left_stop',
    'right_incentives',
    'right_stop',
    'remoteness',
]


@lru_cache(maxsize=None)
def left_incentives(G):
    """
    Compute the left incentives of G.

    The left incentives are defined as:
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
    return {canonical_form(G_L - G) for G_L in G.left}


@lru_cache(maxsize=None)
def right_incentives(G):
    """
    Compute the right incentives of G.

    The right incentives are defined as:
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
    return {canonical_form(G - G_R) for G_R in G.right}


def stop_order(item):
    """
    Construct a key for ordering left and right stops.

    If x > y:
        x- > x+ > y- > y+

    Since L is lexicographically less than R, we can't rely on natural ordering.

    Parameters
    ----------
    item : tuple
        A game, and an adornment.

    Returns
    -------
    item : tuple
        The same tuple, but with the second argument augmented for proper
        ordering.
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
        '+' if it is left's turn, '-' if right's. Only returned if adorn is
        True.
    """
    if G.is_number:
        ls = (G, '+')
    else:
        ls = max((right_stop(G_L) for G_L in G.left), key=stop_order)

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
        '+' if it is left's turn, '-' if right's. Only returned if adorn is
        True.
    """
    if G.is_number:
        rs = (G, '-')
    else:
        rs = min((left_stop(G_R) for G_R in G.right), key=stop_order)

    if adorn:
        return rs
    else:
        return rs[0]


@lru_cache(maxsize=None)
def remoteness(N):
    """
    Compute the remoteness of N.

    Parameters
    ----------
    N : Nimber
        The nimber of interest.

    Returns
    -------
    remote : int
        The remoteness of N.
    """
    if N.n == 0:
        return 0

    remotes = {remoteness(n) for n in N.left}

    if all(remote % 2 == 1 for remote in remotes):
        return 1 + max(remotes)
    else:
        return 1 + min(remote for remote in remotes if remote % 2 == 0)
