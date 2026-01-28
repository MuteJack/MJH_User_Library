# mjh_math/__init__.py
"""
Math utilities package
"""

from .geometry import (
    get_obb_polygon,
    centerpos_from_frontcenter,
    frontcenter_from_centerpos,
    calculate_obb_distance,
    filter_points_in_radius,
    calculate_polygon_distance,
    calculate_polygon_distances,
    get_obb_bounding_margin,
    menger_curvature,
    curvature_at_position,
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
    'frontcenter_from_centerpos',
    'calculate_obb_distance',
    'filter_points_in_radius',
    'calculate_polygon_distance',
    'calculate_polygon_distances',
    'get_obb_bounding_margin',
    'menger_curvature',
    'curvature_at_position',
    'normalize_angle',
    'normalize_angle_half',
    'get_decimal_places',
    'round_to_decimal_places',
]
