"""
"""

from functools import lru_cache
from itertools import chain, combinations, count


__all__ = [
    'mex',
    'powerset',
]


def mex(s):
    """
    """
    for i in count():  # pragma: no branch
        if i not in s:
            return i


def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
