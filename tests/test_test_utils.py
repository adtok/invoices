"""Testing for testing utils"""

from .utils import almost_equal


def test_almost_equal():
    """Tests almost_equal"""
    assert almost_equal(10.0, 10.0005)
    assert not almost_equal(10.0, 10.1)
    assert almost_equal(10.0, 10.01, precision=0.1)
    # Test "a 10% discount on $10"
    assert almost_equal(10.0 - 10.0 * (10.0 / 100), 9.0)
