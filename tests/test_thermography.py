"""
Tests for ludology.thermography.
"""

import pytest

from ludology import Game
from ludology.thermography import mean, temperature, cool, heat, overheat


G_L1 = Game(5/2)
G_L2 = Game({Game(4)}, {Game(2)})
G_R1 = Game({Game(-1)}, {Game(-2)})
G_R2 = Game({Game()}, {Game(-4)})
g1 = Game({G_L1, G_L2}, {G_R1, G_R2})


@pytest.mark.parametrize(['g', 'm'], [
    (Game({1}, {-1}), 0.0),
    (Game({2}, {0}), 1.0),
    (Game(3), 3.0),
    (g1, 0.5),
])
def test_mean(g, m):
    """
    Test that several mean values are correct.
    """
    assert mean(g) == m


@pytest.mark.parametrize(['g', 't'], [
    (Game({1}, {-1}), 1.0),
    (Game({3}), -1.0),
    (g1, 2.5),
    (Game(1/2), -1/2),
    (Game(3/4), -1/4),
])
def test_temperature(g, t):
    """
    Test that several temperatures are correct.
    """
    assert temperature(g) == t


@pytest.mark.parametrize(['g', 't', 'v'], [
    (Game({2}, {-2}), 1.0, Game({1}, {-1})),
    (g1, 2.0, Game({1}, {Game({0}, {0})})),
])
def test_cooling(g, t, v):
    """
    Test that several cooled Games are correct.
    """
    assert cool(g, t) == v


@pytest.mark.parametrize(['g', 't', 'v'], [
    (Game({1}, {-1}), Game(1), Game({2}, {-2})),
    (Game({1}, {-1}), 1, Game({2}, {-2})),
    (Game(2), 1.0, Game(2)),
])
def test_heating(g, t, v):
    """
    Test that several heated Games are correct.
    """
    assert heat(g, t) == v


@pytest.mark.parametrize(['g', 't', 'v'], [
    (Game({1}, {-1}), 1.0, Game({3}, {-3})),
    (Game({0}, {0}), 1.0, Game({1}, {-1})),
    (Game({0}, {Game({0}, {0})}), 1.0, Game({1}, {Game({0}, {-2})})),
])
def test_overheating(g, t, v):
    """
    Test that several overheated Games are correct.
    """
    assert overheat(g, t) == v
