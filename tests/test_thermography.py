# -*- coding: utf-8 -*-

"""
Tests for ludology.thermography.
"""

import pytest

from ludology import Game, Surreal
from ludology.closet import (g1, g2, g5, half, one, pm_one, quarter, star, up,
                             zero)
from ludology.thermography import (Particle, cool, heat, is_cold, is_hot,
                                   is_tepid, mean, overheat, temperature,
                                   thermal_dissociation)


@pytest.mark.parametrize(('g', 'm'), [
    (pm_one, 0.0),
    (one + pm_one, 1.0),
    (3 * one, 3.0),
    (g1, 0.5),
])
def test_mean(g, m):
    """
    Test that several mean values are correct.
    """
    assert mean(g) == m


@pytest.mark.parametrize(('g', 't'), [
    (pm_one, 1.0),
    (3 * one, -1.0),
    (g1, 2.5),
    (half, -1 / 2),
    (half + quarter, -1 / 4),
])
def test_temperature(g, t):
    """
    Test that several temperatures are correct.
    """
    assert temperature(g) == t


@pytest.mark.parametrize(('g', 't', 'v'), [
    (Game({2}, {-2}), 1.0, Game({1}, {-1})),
    (g1, 2.0, Game({1}, {Game({0}, {0})})),
])
def test_cooling(g, t, v):
    """
    Test that several cooled Games are correct.
    """
    assert cool(g, t) == v


@pytest.mark.parametrize(('g', 't', 'v'), [
    (pm_one, one, Game({2}, {-2})),
    (pm_one, 1, Game({2}, {-2})),
    (2 * one, 1.0, 2 * one),
])
def test_heating(g, t, v):
    """
    Test that several heated Games are correct.
    """
    assert heat(g, t) == v


@pytest.mark.parametrize(('g', 't', 'v'), [
    (pm_one, 1.0, Game({3}, {-3})),
    (star, 1.0, pm_one),
    (up, 1.0, Game({1}, {Game({0}, {-2})})),
])
def test_overheating(g, t, v):
    """
    Test that several overheated Games are correct.
    """
    assert overheat(g, t) == v


@pytest.mark.parametrize('g', [
    3 * one,
    Surreal.from_value(1 / 4),
    zero,
    -4 * one,
])
def test_is_cold(g):
    """
    Assert that Numbers are cold.
    """
    assert is_cold(g)


@pytest.mark.parametrize('g', [
    star,
    2 + star,
    5 * one + up,
])
def test_is_tepid(g):
    """
    Assert that Numbers are tepid.
    """
    assert is_tepid(g)


@pytest.mark.parametrize('g', [
    pm_one,
    g1,
])
def test_is_hot(g):
    """
    Assert that Numbers are hot.
    """
    assert is_hot(g)


@pytest.mark.parametrize(('g', 'dissociation'), [
    (pm_one, (0.0, Particle(star, 1))),
    (g2, (0.0, Particle(star, 3.0), Particle(g5, 2.0), Particle(star, 1.0))),
])
def test_thermal_dissociation(g, dissociation):
    """
    Test the thermal dissociation.
    """
    assert thermal_dissociation(g) == dissociation
