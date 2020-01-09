# -*- coding: utf-8 -*-

"""
A hypothesis strategy for sampling Games.

We use hypothesis.strategies.recursive to build pairs of options recursively, with some base
set of Games as leaves. By manual testing, using the second day games as leaves, and limiting left
and right options to having at most two games tends to sample things best. Having too many options
increases the likelihood of a number which would dominate any interesting infinitesimals. As such,
it would be pretty rare to sample tinies or the like.
"""

from hypothesis.strategies import composite, integers, lists, recursive, sampled_from, tuples

from .canonical_form import canonical_form
from .games import Game, Nimber, Surreal
from .lattice import all_games


__all__ = [
    'games',
    'nimbers',
    'surreals',
]


def gamify(options):
    """
    Transform a nested pair of options into a Game in canonical form.

    Parameters
    ----------
    options : tuple(list, list)
        Nested tuples containing two lists of tuples containing two lists... with Games as leaves.

    Returns
    -------
    g : Game
        The Game represented by `options`.
    """
    try:
        left, right = options
        left = [gamify(_) for _ in left]
        right = [gamify(_) for _ in right]
        return canonical_form(Game(left, right))
    except TypeError:
        return options


@composite
def games(draw, base_day=2, max_options=2):  # pragma: no cover
    """
    Build a Hypothesis strategy for generating Games.

    Parameters
    ----------
    draw : func
        Required by hypothesis.strategies.composite.
    base_day : int >= 0
        The maximum birthday of games to use a leaves. Defaults to 2.
    max_options : int >= 0
        The maximum number of left, right options to allow for each subposition. Defaults to 2.
        Note that setting this number larger likely leads to the set being dominated by a number,
        reducing the variability in sampled games.

    Returns
    -------
    sample : Game
        A random Game.
    """
    options = draw(recursive(base=sampled_from(list(all_games(base_day))),
                             extend=lambda child: tuples(lists(child, max_size=max_options),
                                                         lists(child, max_size=max_options))))

    return gamify(options)


@composite
def nimbers(draw, max_value=20):  # pragma: no cover
    """
    Build a Hypothesis strategy for generating Nimbers.

    Parameters
    ----------
    draw : func
        Required by hypothesis.strategies.composite.
    max_value : int >= 0
        The maximum Nimber to consider

    Returns
    -------
    sample : Nimber
        A random Nimber.
    """
    value = draw(integers(min_value=0, max_value=max_value))

    return Nimber.from_integer(value)


@composite
def surreals(draw, max_numerator=5, max_denominator_exponent=5):  # pragma: no cover
    """
    Build a Hypothesis strategy for generating Surreal Numbers.

    Parameters
    ----------
    draw : func
        Required by hypothesis.strategies.composite.
    max_numerator : int >= 0
        The maximum numerator to generate.
    max_denominator_exponent : int >= 0
        The maximum exponent for the denominator.

    Returns
    -------
    sample : Surreal
        A random Surreal Number.
    """
    numerator = draw(integers(min_value=-max_numerator, max_value=max_numerator))
    denominator_exponent = draw(integers(min_value=0, max_value=max_denominator_exponent))

    return Surreal.from_value(numerator / 2**denominator_exponent)
