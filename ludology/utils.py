"""
Various utilities helpful in computing Game properties.
"""

from itertools import chain, combinations, count


__all__ = [
    'mex',
    'powerset',
]


def mex(s):
    """
    Compute the *m*inimum *ex*cluded element of the set `s`. The universe is assumed to be the
    nonnegative integers.

    Parameters
    ----------
    s : collection
        The set/collection to compute the mex of.

    Returns
    -------
    mex : int
        The smallest non-negative integer not included in `s`.
    """
    for i in count():  # pragma: no branch
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
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
