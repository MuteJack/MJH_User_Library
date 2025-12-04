# mjh_math/basic_math.py
""" Sets of Functions/Macros about Basic Math Functions"""

# Angle
def normalize_angle(angle):
    """Normalize angle to [0, 360) range.

    Args:
        angle (float): Angle in degrees

    Returns:
        normalized_angle (float): Angle in [0, 360) range
    """
    return (angle % 360)


def normalize_angle_half(angle):
    """Normalize angle to [-180, 180) range.

    Args:
        angle (float): Angle in degrees

    Returns:
        normalized_angle (float): Angle in [-180, 180) range
    """
    return ((angle + 180) % 360 - 180)


# Decimal places
def get_decimal_places(x: float) -> int:
    """Get number of decimal places in a float.

    Args:
        x (float): Input number

    Returns:
        decimal_places (int): Number of decimal places

    Example:
        >>> get_decimal_places(0.2)
        1
        >>> get_decimal_places(0.05)
        2
        >>> get_decimal_places(1.0)
        0
    """
    s = f"{x:.10f}".rstrip('0')
    if '.' in s:
        return len(s.split('.')[1])
    return 0


def round_to_decimal_places(value: float, reference: float) -> float:
    """Round value to match decimal places of reference.

    Args:
        value (float): Value to round
        reference (float): Reference value for decimal places

    Returns:
        rounded_value (float): Rounded value

    Example:
        >>> round_to_decimal_places(-2 * 0.2, 0.2)  # -0.4000000000000001 → -0.4
        -0.4
        >>> round_to_decimal_places(3 * 0.05, 0.05)  # 0.15000000000000002 → 0.15
        0.15
    """
    return round(value, get_decimal_places(reference))
