"""
Tests for ludology.tools.
"""

import pytest

from ludology import Game
from ludology.closet import zero, pm_one, star
from ludology.tools import left_stop, right_stop, left_incentives, right_incentives


@pytest.mark.parametrize(['g', 'v'], [
    (zero, (0, '+')),
    (pm_one, (1, '-')),
    (star, (0, '-')),
])
def test_left_stop_1(g, v):
    """
    Test left stops with adornment.
    """
    assert left_stop(g) == v


@pytest.mark.parametrize(['g', 'v'], [
    (zero, 0),
    (pm_one, 1),
    (star, 0),
])
def test_left_stop_2(g, v):
    """
    Test left stops without adornment.
    """
    assert left_stop(g, adorn=False) == v


@pytest.mark.parametrize(['g', 'v'], [
    (zero, (0, '-')),
    (pm_one, (-1, '+')),
    (star, (0, '+')),
])
def test_right_stop_1(g, v):
    """
    Test right stops with adornment.
    """
    assert right_stop(g) == v


@pytest.mark.parametrize(['g', 'v'], [
    (zero, 0),
    (pm_one, -1),
    (star, 0),
])
def test_right_stop_2(g, v):
    """
    Test right stops without adornment.
    """
    assert right_stop(g, adorn=False) == v


def test_left_incentives():
    """
    Test for the incentives of a known example.
    """
    g = Game({0}, {Game({0}, {-2})})
    li = {Game({Game({2}, {0})}, {0})}
    assert left_incentives(g) == li


def test_right_incentives():
    """
    Test for the incentives of a known example.
    """
    g = Game({0}, {Game({0}, {-2})})
    ri = {Game({Game({2}, {0}), 2}, {0})}
    assert right_incentives(g) == ri
