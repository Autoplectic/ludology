"""
Tests for ludology.sums.
"""

import pytest

from ludology import Game, canonicalize
from ludology.sums import (disjunctive, conjunctive, selective, diminished_disjunctive,
                           continued_conjunctive, shortened_selective, ordinal, side, sequential)


zero = Game(0)
one = Game(1)
star = Game({0}, {0})
pm = Game({1}, {-1})
G = Game({0}, {pm})
up = Game({0}, {star})


@pytest.mark.parametrize(['G', 'H', 'J'], [
    (G, up, Game({1}, {Game({1}, {1})})),
    (G, zero, G),
    (zero, G, G),
])
def test_disjunctive(G, H, J):
    """
    Test that the disjunctive sum matches known result.
    """
    assert canonicalize(disjunctive(G, H)) == J


@pytest.mark.parametrize(['G', 'H', 'J'], [
    (G, up, up),
    (G, zero, zero),
    (zero, G, zero),
])
def test_conjunctive(G, H, J):
    """
    Test that the conjunctive sum matches known result.
    """
    assert canonicalize(conjunctive(G, H)) == J


@pytest.mark.parametrize(['G', 'H', 'J'], [
    (G, up, Game({1}, {Game({1, one + star}, {-1, -one + star}), Game({1}, {1, pm})})),
    (G, zero, G),
    (zero, G, G),
])
def test_selective(G, H, J):
    """
    Test that the selective sum matches known result.
    """
    assert canonicalize(selective(G, H)) == J


@pytest.mark.parametrize(['G', 'H', 'J'], [
    (G, up, up),
    (G, zero, zero),
    (zero, G, zero),
])
def test_diminished_disjunctive(G, H, J):
    """
    Test that the diminished disjunctive sum matches known result.
    """
    assert canonicalize(diminished_disjunctive(G, H)) == J


@pytest.mark.parametrize(['G', 'H', 'J'], [
    (G, up, one),
    (G, zero, G),
    (zero, G, G),
])
def test_continued_conjunctive(G, H, J):
    """
    Test that the continued conjunctive sum matches known result.
    """
    assert canonicalize(continued_conjunctive(G, H)) == J


@pytest.mark.parametrize(['G', 'H', 'J'], [
    (G, up, Game({0}, {star, Game({0, star}, {0, star})})),
    (G, zero, zero),
    (zero, G, zero),
])
def test_shortened_selective(G, H, J):
    """
    Test that the shortened selective sum matches known result.
    """
    assert canonicalize(shortened_selective(G, H)) == J


@pytest.mark.parametrize(['G', 'H', 'J'], [
    (G, up, Game({1}, {Game({1}, {1, pm}), pm})),
    (G, zero, G),
    (zero, G, G),
])
def test_ordinal(G, H, J):
    """
    Test that the ordinal sum matches known result.
    """
    assert canonicalize(ordinal(G, H)) == J


@pytest.mark.parametrize(['G', 'H', 'J'], [
    (G, up, Game({0}, {Game({0}, {1})})),
    (G, zero, G),
    (zero, G, G),
])
def test_side(G, H, J):
    """
    Test that the side sum matches known result.
    """
    assert canonicalize(side(G, H)) == J


@pytest.mark.parametrize(['G', 'H', 'J'], [
    (G, up, one),
    (G, zero, G),
    (zero, G, G),
])
def test_sequential(G, H, J):
    """
    Test that the sequential sum matches known result.
    """
    assert canonicalize(sequential(G, H)) == J
