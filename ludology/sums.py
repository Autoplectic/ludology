# -*- coding: utf-8 -*-

"""
A variety of ways of summing games.
"""

from functools import lru_cache, wraps

from .canonical_form import canonical_form
from .games import Game

__all__ = [
    'disjunctive',
    'conjunctive',
    'selective',
    'diminished_disjunctive',
    'continued_conjunctive',
    'shortened_selective',
    'ordinal',
    'side',
    'sequential',
]


def canonize(f):
    """
    Construct a decorator to add a `canon` option to f.

    Add a `canon` option to `f` which toggles whether the function returns the
    canonical form of the value.

    Parameters
    ----------
    f : func
        The function to wrap.

    Returns
    -------
    wrapped : func
        The wrapped form of `f`.
    """
    @wraps(f)
    def wrapped(G, H, canon=True):
        game = f(G, H)
        if canon:
            return canonical_form(game)

        return game

    return wrapped


@lru_cache(maxsize=None)
@canonize
def disjunctive(G, H):
    """
    Compute the disjunctive sum of G and H.

    Move in exactly one component.

    Parameters
    ----------
    G : Game
        The first Game.
    H : Game
        The second Game.

    Returns
    -------
    sum : Game
        The disjunctive sum of G and H.
    """
    left_1 = {disjunctive(G_L, H) for G_L in G.left}
    left_2 = {disjunctive(G, H_L) for H_L in H.left}
    right_1 = {disjunctive(G_R, H) for G_R in G.right}
    right_2 = {disjunctive(G, H_R) for H_R in H.right}
    return Game(left_1 | left_2, right_1 | right_2)


@lru_cache(maxsize=None)
@canonize
def conjunctive(G, H):
    """
    Compute the conjunctive sum of G and H.

    Move in all components. Play ends when any one of them terminates.

    Parameters
    ----------
    G : Game
        The first Game.
    H : Game
        The second Game.

    Returns
    -------
    sum : Game
        The conjunctive sum of G and H.
    """
    left = {conjunctive(G_L, H_L) for G_L in G.left for H_L in H.left}
    right = {conjunctive(G_R, H_R) for G_R in G.right for H_R in H.right}
    return Game(left, right)


@lru_cache(maxsize=None)
@canonize
def selective(G, H):
    """
    Compute the selective sum of G and H.

    Move in any number of components, but at least one.

    Parameters
    ----------
    G : Game
        The first Game.
    H : Game
        The second Game.

    Returns
    -------
    sum : Game
        The selective sum of G and H.
    """
    left_1 = {selective(G_L, H) for G_L in G.left}
    left_2 = {selective(G, H_L) for H_L in H.left}
    left_3 = {selective(G_L, H_L) for G_L in G.left for H_L in H.left}
    right_1 = {selective(G_R, H) for G_R in G.right}
    right_2 = {selective(G, H_R) for H_R in H.right}
    right_3 = {selective(G_R, H_R) for G_R in G.right for H_R in H.right}
    return Game(left_1 | left_2 | left_3, right_1 | right_2 | right_3)


@lru_cache(maxsize=None)
@canonize
def diminished_disjunctive(G, H):
    """
    Compute the diminished disjunctive sum of G and H.

    Move in exactly one component. Play ends immediately when any one of them
    terminates.

    Parameters
    ----------
    G : Game
        The first Game.
    H : Game
        The second Game.

    Returns
    -------
    sum : Game
        The diminished disjunctive sum of G and H.
    """
    if G == 0 or H == 0:
        return Game(0)
    else:
        left_1 = {diminished_disjunctive(G_L, H) for G_L in G.left}
        left_2 = {diminished_disjunctive(G, H_L) for H_L in H.left}
        right_1 = {diminished_disjunctive(G_R, H) for G_R in G.right}
        right_2 = {diminished_disjunctive(G, H_R) for H_R in H.right}
        return Game(left_1 | left_2, right_1 | right_2)


@lru_cache(maxsize=None)
@canonize
def continued_conjunctive(G, H):
    """
    Compute the continued conjunctive sum of G and H.

    Move in all nonterminal components. Play ends only after all components
    terminate.

    Parameters
    ----------
    G : Game
        The first Game.
    H : Game
        The second Game.

    Returns
    -------
    sum : Game
        The continued conjunctive sum of G and H.
    """
    if G == 0 or H == 0:
        return disjunctive(G, H)
    else:
        left = {continued_conjunctive(G_L, H_L) for G_L in G.left for H_L in H.left}
        right = {continued_conjunctive(G_R, H_R) for G_R in G.right for H_R in H.right}
        return Game(left, right)


@lru_cache(maxsize=None)
@canonize
def shortened_selective(G, H):
    """
    Compute the shortened selective sum of G and H.

    Move in any number of components. Play ends immediately when any one of them
    terminates.

    Parameters
    ----------
    G : Game
        The first Game.
    H : Game
        The second Game.

    Returns
    -------
    sum : Game
        The shortened selective sum of G and H.
    """
    if G == 0 or H == 0:
        return Game(0)
    else:
        left_1 = {shortened_selective(G_L, H) for G_L in G.left}
        left_2 = {shortened_selective(G, H_L) for H_L in H.left}
        left_3 = {shortened_selective(G_L, H_L) for G_L in G.left for H_L in H.left}
        right_1 = {shortened_selective(G_R, H) for G_R in G.right}
        right_2 = {shortened_selective(G, H_R) for H_R in H.right}
        right_3 = {shortened_selective(G_R, H_R) for G_R in G.right for H_R in H.right}
        return Game(left_1 | left_2 | left_3, right_1 | right_2 | right_3)


@lru_cache(maxsize=None)
@canonize
def ordinal(G, H):
    """
    Compute the ordinal sum of G and H.

    Move in G or H; any move on G annihilates H.

    Parameters
    ----------
    G : Game
        The first Game.
    H : Game
        The second Game.

    Returns
    -------
    sum : Game
        The ordinal sum of G and H.
    """
    left = {ordinal(G, H_L) for H_L in H.left}
    right = {ordinal(G, H_R) for H_R in H.right}
    return Game(G.left | left, G.right | right)


@lru_cache(maxsize=None)
@canonize
def side(G, H):
    """
    Compute the side sum of G and H.

    Move in G or H; Left's moves on H annihilate G, and Right's moves on G
    annihilate H.

    Parameters
    ----------
    G : Game
        The first Game.
    H : Game
        The second Game.

    Returns
    -------
    sum : Game
        The side sum of G and H.
    """
    left = {side(G_L, H) for G_L in G.left}
    right = {side(G, H_R) for H_R in H.right}
    return Game(left | H.left, G.right | right)


@lru_cache(maxsize=None)
@canonize
def sequential(G, H):
    """
    Compute the sequential sum of G and H.

    Move in G unless G has terminated; in that case move in H.

    Parameters
    ----------
    G : Game
        The first Game.
    H : Game
        The second Game.

    Returns
    -------
    sum : Game
        The sequential sum of G and H.
    """
    if G == 0:
        return H
    else:
        left = {sequential(G_L, H) for G_L in G.left}
        right = {sequential(G_R, H) for G_R in G.right}
        return Game(left, right)
