"""
A variety of ways of summing games.
"""

from .game import Game


def disjunctive(G, H):
    """
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
    left_1 = {disjunctive(G_L, H) for G_L in G._left}
    left_2 = {disjunctive(G, H_L) for H_L in H._left}
    right_1 = {disjunctive(G_R, H) for G_R in G._right}
    right_2 = {disjunctive(G, H_R) for H_R in H._right}
    return Game(left_1 | left_2, right_1 | right_2)


def conjunctive(G, H):
    """
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
    left = {conjunctive(G_L, H_L) for G_L in G._left for H_L in H._left}
    right = {conjunctive(G_R, H_R) for G_R in G._right for H_R in H._right}
    return Game(left, right)


def selective(G, H):
    """
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
    left_1 = {selective(G_L, H) for G_L in G._left}
    left_2 = {selective(G, H_L) for H_L in H._left}
    left_3 = {selective(G_L, H_L) for G_L in G._left for H_L in H._left}
    right_1 = {selective(G_R, H) for G_R in G._right}
    right_2 = {selective(G, H_R) for H_R in H._right}
    right_3 = {selective(G_R, H_R) for G_R in G._right for H_R in H._right}
    return Game(left_1 | left_2 | left_3, right_1 | right_2 | right_3)


def diminished_disjunctive(G, H):
    """
    Move in exactly one component. Play ends immediately when any one of them terminates.

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
        left_1 = {diminished_disjunctive(G_L, H) for G_L in G._left}
        left_2 = {diminished_disjunctive(G, H_L) for H_L in H._left}
        right_1 = {diminished_disjunctive(G_R, H) for G_R in G._right}
        right_2 = {diminished_disjunctive(G, H_R) for H_R in H._right}
        return Game(left_1 | left_2, right_1 | right_2)


def continued_conjunctive(G, H):
    """
    Move in all nonterminal components. Play ends only after all components terminate.

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
        left = {continued_conjunctive(G_L, H_L) for G_L in G._left for H_L in H._left}
        right = {continued_conjunctive(G_R, H_R) for G_R in G._right for H_R in H._right}
        return Game(left, right)


def shortened_selective(G, H):
    """
    Move in any number of components. Play ends immediately when any one of them terminates.

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
        left_1 = {shortened_selective(G_L, H) for G_L in G._left}
        left_2 = {shortened_selective(G, H_L) for H_L in H._left}
        left_3 = {shortened_selective(G_L, H_L) for G_L in G._left for H_L in H._left}
        right_1 = {shortened_selective(G_R, H) for G_R in G._right}
        right_2 = {shortened_selective(G, H_R) for H_R in H._right}
        right_3 = {shortened_selective(G_R, H_R) for G_R in G._right for H_R in H._right}
        return Game(left_1 | left_2 | left_3, right_1 | right_2 | right_3)


def ordinal(G, H):
    """
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
    left_1 = {G_L for G_L in G._left}
    left_2 = {ordinal(G, H_L) for H_L in H._left}
    right_1 = {G_R for G_R in G._right}
    right_2 = {ordinal(G, H_R) for H_R in H._right}
    return Game(left_1 | left_2, right_1 | right_2)


def side(G, H):
    """
    Move in G or H; Left's moves on H annihilate G, and Right's moves on G annihilate H.

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
    left_1 = {side(G_L, H) for G_L in G._left}
    left_2 = {H_L for H_L in H._left}
    right_1 = {G_R for G_R in G._right}
    right_2 = {side(G, H_R) for H_R in H._right}
    return Game(left_1 | left_2, right_1 | right_2)


def sequential(G, H):
    """
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
        left = {sequential(G_L, H) for G_L in G._left}
        right = {sequential(G_R, H) for G_R in G._right}
        return Game(left, right)
