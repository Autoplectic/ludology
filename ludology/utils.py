# -*- coding: utf-8 -*-

"""
Various utilities helpful in computing Game properties.
"""

import sys
from contextlib import contextmanager
from itertools import chain, combinations, count


__all__ = [
    'mex',
    'powerset',
    'recursion_limit',
]


def mex(s):
    """
    Compute the minimum excluded element of the set `s`.

    The universe is assumed to be the nonnegative integers.

    Parameters
    ----------
    s : collection
        The set/collection to compute the mex of.

    Returns
    -------
    mex : int
        The smallest non-negative integer not included in `s`.
    """
    for i in count():  # pragma: no branch, noqa: R503
        if i not in s:
            return i


def powerset(iterable):
    """
    Compute the powerset of the elements represented in `iterable`.

    Parameters
    ----------
    iterable : iterable
        The set of elements to compute the powerset of.

    Returns
    -------
    ps : iterable
        An iterator over the powerset of `iterable`.
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


@contextmanager
def recursion_limit(limit):
    """
    Temporarily set the recursion limit to `limit`.

    Parameters
    ----------
    limit : int > 0
        The new limit.
    """
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(limit)
    yield
    sys.setrecursionlimit(old_limit)
