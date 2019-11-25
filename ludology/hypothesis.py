"""
A hypothesis strategy for sampling Games.

We use hypothesis.strategies.recursive to build pairs of options recursively, with some base
set of Games as leaves. By manual testing, using the second day games as leaves, and limiting left
and right options to having at most two games tends to sample things best. Having too many options
increases the likelihood of a number which would dominate any interesting infinitesimals. As such,
it would be pretty rare to sample tinies or the like.
"""

from hypothesis.strategies import composite, lists, recursive, sampled_from, tuples

from .game import Game
from .lattice import all_games
from .tools import canonicalize


__all__ = [
    'games',
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
        return canonicalize(Game(left, right))
    except TypeError:
        return options


@composite
def games(draw, base_day=2, max_options=2):  # pragma: no cover
    """
    A Hypothesis strategy for generating Games.

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
