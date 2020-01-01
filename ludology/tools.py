# -*- coding: utf-8 -*-

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
    'remoteness',
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
    If x > y:
        x_- > x_+ > y_- > y_+

    Since L is lexicographically less than R, we can't rely on natural ordering.
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
        '+' if it is left's turn, '-' if right's. Only returned if adorn is
        True.
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
    left = copy(G._left)
    for g in G._left:
        if any(g < G_L for G_L in left):
            left.remove(g)
    right = copy(G._right)
    for g in G._right:
        if any(g > G_R for G_R in right):
            right.remove(g)
    G._left = left
    G._right = right


def replace_reversible(G):
    """
    Remove the reversable options of G.

    A left option is reversible if it has a right option which is less than G.
    In this case, that left option can be replaced with it's right option's left
    options. Essentially, this means that if left were to make a move to an
    option from which right has the ability to move to a position which is
    strictly better for her than G, it is a "no brainer" to do so, and so that
    left option might as well be replaced with the options available after right
    makes the obvious responce.

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


def make_specific(G):
    """
    Return G as a more specific subtype of Game, if possible.

    Parameters
    ----------
    G : Game
        The game to make specific.

    Returns
    -------
    G : [Game, Nimber, Surreal, Switch]
        G as a subclass of Game.
    """
    from .games import Nimber, Surreal, Switch

    if G.is_number:
        return Surreal(G)
    if G.is_impartial:
        return Nimber(G)
    if G.is_switch:
        return Switch(G)

    return G


@lru_cache(maxsize=None)
def canonicalize(G, specify=True):
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
    cG = copy(G)

    cG._left = {canonicalize(G_L) for G_L in cG.left}
    cG._right = {canonicalize(G_R) for G_R in cG.right}

    old_left, old_right = set(), set()
    while cG.left != old_left or cG.right != old_right:
        old_left, old_right = cG.left, cG.right
        remove_dominated(cG)
        replace_reversible(cG)

    if specify:
        return make_specific(cG)
    return cG


@lru_cache(maxsize=None)
def remoteness(N):
    """
    The remoteness of N.

    Parameters
    ----------
    N : Nimber
        The nimber of interest.

    Returns
    -------
    remote : int
        The remoteness of N.
    """
    if N._n == 0:
        return 0

    remotes = {remoteness(n) for n in N._left}

    if all(remote % 2 == 1 for remote in remotes):
        return 1 + max(remotes)
    else:
        return 1 + min(remote for remote in remotes if remote % 2 == 0)
