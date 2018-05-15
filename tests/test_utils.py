"""
"""

import pytest

from ludology.utils import mex, powerset


@pytest.mark.parametrize(['s', 'v'], [
    ({1, 2, 3}, 0),
    ({0, 1, 3}, 2),
    ({0, 1, 2}, 3),
])
def test_mex(s, v):
    """
    """
    assert mex(s) == v


@pytest.mark.parametrize('n', range(6))
def test_powerset(n):
    """
    """
    assert len(list(powerset(range(n)))) == 2**n