# mjh_math/__init__.py
"""
Math utilities package
"""

from .geometry import (
    get_obb_polygon,
    centerpos_from_frontcenter,
    calculate_obb_distance
)

from .basic_math import(
    normalize_angle,
    normalize_angle_half,
    get_decimal_places,
    round_to_decimal_places
)

__all__ = [
    'get_obb_polygon',
    'centerpos_from_frontcenter',
    'calculate_obb_distance',
    'normalize_angle',
    'normalize_angle_half',
    'get_decimal_places',
    'round_to_decimal_places',
]
