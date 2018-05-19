"""
Tests for ludolory.hypothesis.
"""

import pytest

from ludology import Game
from ludology.hypothesis import gamify


@pytest.mark.parametrize(['s', 'g'], [
    (([([], [([], [])]), ([], [])], [([], [])]), Game({0}, {0})),
    (Game({0}, {0}), Game({0}, {0})),
])
def test_gamify(s, g):
    """
    Test a contrived example.
    """
    assert gamify(s) == g
