"""
"""

import pytest

from ludology import Nimber


def test_add_nimbers():
    """
    """
    a = Nimber(5)
    b = Nimber(6)
    c = Nimber(3)
    assert a + b == c


def test_mul_nimbers():
    """
    """
    a = Nimber(5)
    b = Nimber(6)
    c = Nimber(8)
    assert a + b == c


def test_neg_nimbers():
    """
    """
    a = Nimber(5)
    assert a == -a