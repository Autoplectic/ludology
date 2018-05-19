"""
Tests for ludolory.hypothesis.
"""

import pytest

from ludology import Game
from ludology.hypothesis import gamify


def test_gamify():
    """
    Test a contrived example.
    """
    structure = ([([], [([], [])]), ([], [])], [([], [])])
    assert gamify(structure) == Game({0}, {0})
