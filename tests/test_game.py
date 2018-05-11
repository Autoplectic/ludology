"""
"""

import pytest

from ludology import Game


zero = Game(0)
half = Game(1/2)
one = Game(1)
star = Game({zero}, {zero})
up = Game({zero}, {star})


@pytest.mark.parametrize(['g1', 'g2'], [
    (one, zero),
    (one, half),
    (one, -one),
    (zero, -one),
    (zero, -half),
    (up, zero),
    (half, up),
    (up + up, star),
])
def test_ge(g1, g2):
    """
    """
    assert g1 >= g2


@pytest.mark.parametrize(['g1', 'g2'], [
    (star, zero),
    (star, up),
])
def test_fuzzy(g1, g2):
    """
    """
    assert g1 | g2