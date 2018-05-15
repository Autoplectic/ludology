"""
"""

import pytest

from ludology import Game
from ludology.tools import left_stop, right_stop, left_incentives, right_incentives


@pytest.mark.parametrize(['g', 'v'], [
    (Game(0), (0, '+')),
    (Game({1}, {-1}), (1, '-')),
    (Game({0}, {0}), (0, '-')),
])
def test_left_stop(g, v):
    """
    """
    assert left_stop(g) == v


@pytest.mark.parametrize(['g', 'v'], [
    (Game(0), (0, '-')),
    (Game({1}, {-1}), (-1, '+')),
    (Game({0}, {0}), (0, '+')),
])
def test_right_stop(g, v):
    """
    """
    assert right_stop(g) == v