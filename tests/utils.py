"""Utilities for testing"""

def almost_equal(float1: float, float2: float, precision: float = 0.001) -> bool:
    """
    Returns if the difference between two floats is within a certain precision.

    Main purpose is to make sure monetary values are close enough after multiplication.
    """
    return abs(float1 - float2) < precision
