# mjh_math/geometry.py
"""
Geometry utilities for vehicle simulations

This module provides geometric functions for:
- OBB (Oriented Bounding Box): collision detection and distance calculations
- Curvature: polyline/lane curvature calculations using Menger curvature
"""

import numpy as np
from shapely.geometry import Polygon


def get_obb_polygon(x, y, width, length, angle_deg):
    """Create OBB (Oriented Bounding Box) as Shapely Polygon.

    Args:
        x (float): Center position X
        y (float): Center position Y
        width (float): Vehicle width (lateral dimension)
        length (float): Vehicle length (longitudinal dimension)
        angle_deg (float): Rotation angle in degrees (0 = pointing right, counterclockwise positive)

    Returns:
        polygon (Polygon): Shapely polygon representing the OBB

    Example:
        >>> # Create OBB for vehicle at (10, 5), width=2m, length=5m, pointing right
        >>> poly = get_obb_polygon(10, 5, 2.0, 5.0, 0)
        >>> print(poly.bounds)  # (xmin, ymin, xmax, ymax)
    """
    # Corner coordinates relative to center
    corners = np.array([
        [length/2, width/2],    # Front-left
        [length/2, -width/2],   # Front-right
        [-length/2, -width/2],  # Rear-right
        [-length/2, width/2]    # Rear-left
    ])

    # Rotate
    angle_rad = np.radians(angle_deg)
    cos_a, sin_a = np.cos(angle_rad), np.sin(angle_rad)
    rotation = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
    rotated = corners @ rotation.T

    # Translate to position
    translated = rotated + np.array([x, y])

    return Polygon(translated)


def centerpos_from_frontcenter(front_x, front_y, length, angle_deg):
    """Convert front bumper center position to vehicle center position.

    SUMO uses front bumper center, but OBB calculation uses vehicle center.

    Args:
        front_x (float): Front bumper center X position (SUMO format)
        front_y (float): Front bumper center Y position (SUMO format)
        length (float): Vehicle length
        angle_deg (float): Rotation angle in degrees (0 = pointing right, counterclockwise positive)

    Returns:
        center_position (tuple): (center_x, center_y) - Vehicle center position

    Example:
        >>> # SUMO vehicle at front position (100, 50), length 5m, pointing right (0°)
        >>> center_x, center_y = centerpos_from_frontcenter(100, 50, 5.0, 0)
        >>> print(f"Center: ({center_x}, {center_y})")
        Center: (97.5, 50)

        >>> # Vehicle pointing up (90°)
        >>> center_x, center_y = centerpos_from_frontcenter(100, 50, 5.0, 90)
        >>> print(f"Center: ({center_x:.1f}, {center_y:.1f})")
        Center: (100.0, 47.5)
    """
    # Calculate offset from front to center (half of vehicle length, in reverse direction)
    angle_rad = np.radians(angle_deg)

    # Offset vector pointing from front to center (backwards along vehicle axis)
    offset_x = -(length / 2.0) * np.cos(angle_rad)
    offset_y = -(length / 2.0) * np.sin(angle_rad)

    # Center position = front position + offset
    center_x = front_x + offset_x
    center_y = front_y + offset_y

    return center_x, center_y


def frontcenter_from_centerpos(center_x, center_y, length, angle_deg):
    """Convert vehicle center position to front bumper center position.

    Inverse of centerpos_from_frontcenter().
    OBB calculation uses vehicle center, but SUMO uses front bumper center.

    Args:
        center_x (float): Vehicle center X position
        center_y (float): Vehicle center Y position
        length (float): Vehicle length
        angle_deg (float): Rotation angle in degrees (0 = pointing right, counterclockwise positive)

    Returns:
        front_position (tuple): (front_x, front_y) - Front bumper center position

    Example:
        >>> # Vehicle center at (97.5, 50), length 5m, pointing right (0°)
        >>> front_x, front_y = frontcenter_from_centerpos(97.5, 50, 5.0, 0)
        >>> print(f"Front: ({front_x}, {front_y})")
        Front: (100.0, 50)

        >>> # Vehicle pointing up (90°)
        >>> front_x, front_y = frontcenter_from_centerpos(100, 47.5, 5.0, 90)
        >>> print(f"Front: ({front_x:.1f}, {front_y:.1f})")
        Front: (100.0, 50.0)
    """
    # Calculate offset from center to front (half of vehicle length, in forward direction)
    angle_rad = np.radians(angle_deg)

    # Offset vector pointing from center to front (forward along vehicle axis)
    offset_x = (length / 2.0) * np.cos(angle_rad)
    offset_y = (length / 2.0) * np.sin(angle_rad)

    # Front position = center position + offset
    front_x = center_x + offset_x
    front_y = center_y + offset_y

    return front_x, front_y


def filter_points_in_radius(origin, points, radius, margin=0.0):
    """Filter points within a circular radius (fast pre-filter).

    Uses squared distance comparison for speed (no sqrt).

    Args:
        origin (tuple): Origin point (x, y) or (x, y, ...)
        points (dict): Dict of {key: (x, y, ...)} or {key: [x, y, ...]}
        radius (float): Search radius in meters
        margin (float): Additional margin to add to radius (default: 0)

    Returns:
        candidates (dict): Filtered dict {key: point} within radius + margin

    Example:
        >>> origin = (100, 50)
        >>> points = {'a': (101, 51), 'b': (200, 50), 'c': (105, 55)}
        >>> nearby = filter_points_in_radius(origin, points, radius=10.0)
        >>> # Returns {'a': (101, 51), 'c': (105, 55)}
    """
    ox, oy = origin[0], origin[1]
    search_radius_sq = (radius + margin) ** 2

    candidates = {}
    for key, point in points.items():
        dx = point[0] - ox
        dy = point[1] - oy
        if dx*dx + dy*dy <= search_radius_sq:
            candidates[key] = point

    return candidates


def calculate_polygon_distance(poly1, poly2):
    """Calculate minimum distance between two Shapely polygons.

    Args:
        poly1 (Polygon): First Shapely polygon
        poly2 (Polygon): Second Shapely polygon

    Returns:
        distance (float): Minimum distance (0 if overlapping)
    """
    return poly1.distance(poly2)


def calculate_polygon_distances(reference_polygon, target_polygons):
    """Calculate distances from reference polygon to multiple targets.

    Args:
        reference_polygon (Polygon): Reference Shapely polygon
        target_polygons (dict): Dict of {key: Polygon}

    Returns:
        distances (list): List of (key, distance) sorted by distance

    Example:
        >>> ref = get_obb_polygon(0, 0, 2, 5, 0)
        >>> targets = {'a': get_obb_polygon(10, 0, 2, 5, 0), 'b': get_obb_polygon(5, 0, 2, 5, 0)}
        >>> dists = calculate_polygon_distances(ref, targets)
        >>> # Returns [('b', 0.0), ('a', 5.0)]
    """
    results = []
    for key, poly in target_polygons.items():
        dist = reference_polygon.distance(poly)
        results.append((key, dist))

    results.sort(key=lambda x: x[1])
    return results


def get_obb_bounding_margin(length, width):
    """Calculate diagonal margin for OBB worst-case rotation.

    Args:
        length (float): OBB length
        width (float): OBB width

    Returns:
        margin (float): Diagonal half-length (worst-case bounding radius)
    """
    return np.sqrt(length**2 + width**2) / 2


def calculate_obb_distance(obb1, obb2):
    """Calculate minimum distance between OBB polygon(s).

    Supports single polygon, list, or numpy array inputs.
    Uses Shapely's vectorized operations for array inputs.

    Args:
        obb1 (Union[Polygon, List[Polygon], np.ndarray]): Single OBB polygon or array of OBB polygons
        obb2 (Union[Polygon, List[Polygon], np.ndarray]): Single OBB polygon or array of OBB polygons

    Returns:
        distance (Union[float, np.ndarray]): Distance(s) between OBB pairs (0 if overlapping)

    Example:
        >>> # 1:1 - Single OBB pair
        >>> obb1 = get_obb_polygon(0, 0, 2.0, 5.0, 0)
        >>> obb2 = get_obb_polygon(10, 0, 2.0, 5.0, 0)
        >>> dist = calculate_obb_distance(obb1, obb2)
        >>> print(f"Distance: {dist:.2f} m")
        Distance: 5.00 m

        >>> # N:N - Pairwise distances (same length arrays)
        >>> obbs1 = [get_obb_polygon(i, 0, 2, 5, 0) for i in range(3)]
        >>> obbs2 = [get_obb_polygon(i, 10, 2, 5, 0) for i in range(3)]
        >>> dists = calculate_obb_distance(obbs1, obbs2)

        >>> # 1:N - One OBB vs many (broadcast)
        >>> ego = get_obb_polygon(0, 0, 2, 5, 0)
        >>> others = [get_obb_polygon(i*10, 0, 2, 5, 0) for i in range(1, 5)]
        >>> dists = calculate_obb_distance(ego, others)
    """
    from shapely import distance

    # Single OBB pair - direct calculation
    if isinstance(obb1, Polygon) and isinstance(obb2, Polygon):
        return obb1.distance(obb2)

    # Array inputs - vectorized calculation
    arr1 = np.atleast_1d(obb1)
    arr2 = np.atleast_1d(obb2)

    return distance(arr1, arr2)


# =============================================================================
# Curvature Calculations
# =============================================================================

def menger_curvature(p1, p2, p3):
    """Calculate Menger curvature from three consecutive points.

    Menger curvature: κ = 4 * triangle_area / (a * b * c)
    where a, b, c are side lengths of the triangle formed by three points.

    For collinear points (straight line), curvature is exactly 0.

    Args:
        p1 (tuple): First point (x, y)
        p2 (tuple): Second point (x, y) - curvature is calculated at this point
        p3 (tuple): Third point (x, y)

    Returns:
        curvature (float): Signed curvature [1/m]
            - Positive: left turn (counter-clockwise)
            - Negative: right turn (clockwise)
            - Zero: straight line

    Example:
        >>> # Straight line -> curvature = 0
        >>> menger_curvature((0, 0), (1, 0), (2, 0))
        0.0

        >>> # Circle with radius R -> curvature = 1/R
        >>> import math
        >>> R = 10.0
        >>> p1 = (R, 0)
        >>> p2 = (R * math.cos(0.1), R * math.sin(0.1))
        >>> p3 = (R * math.cos(0.2), R * math.sin(0.2))
        >>> abs(menger_curvature(p1, p2, p3) - 1/R) < 0.01
        True
    """
    # Side lengths
    a = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    b = np.sqrt((p3[0] - p2[0])**2 + (p3[1] - p2[1])**2)
    c = np.sqrt((p3[0] - p1[0])**2 + (p3[1] - p1[1])**2)

    # Degenerate case (coincident points)
    if a * b * c < 1e-12:
        return 0.0

    # Triangle area via Heron's formula
    s = (a + b + c) / 2.0
    area_sq = s * (s - a) * (s - b) * (s - c)

    # Numerical stability (collinear or near-collinear)
    if area_sq <= 0:
        return 0.0

    area = np.sqrt(area_sq)

    # Menger curvature magnitude
    curvature = 4.0 * area / (a * b * c)

    # Sign via cross product (z-component)
    # cross > 0: counter-clockwise (left turn) -> positive
    # cross < 0: clockwise (right turn) -> negative
    cross = (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p2[1] - p1[1]) * (p3[0] - p2[0])
    if cross < 0:
        curvature = -curvature

    return curvature


def curvature_at_position(shape, position):
    """Calculate curvature at a specific position along a polyline.

    Finds three shape points around the given position and calculates
    Menger curvature.

    Args:
        shape (list): List of (x, y) tuples representing the polyline
        position (float): Position along the polyline [m] (from start)

    Returns:
        curvature (float): Signed curvature [1/m]
            - Positive: left turn (counter-clockwise)
            - Negative: right turn (clockwise)
            - Zero: straight line or insufficient points

    Example:
        >>> shape = [(0, 0), (10, 0), (20, 5), (30, 10)]
        >>> curvature_at_position(shape, 15.0)  # Near the curve
    """
    if len(shape) < 3:
        return 0.0

    # Find segment containing the position
    cumulative_dist = 0.0
    target_idx = 0

    for i in range(len(shape) - 1):
        p1 = shape[i]
        p2 = shape[i + 1]
        segment_length = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

        if cumulative_dist + segment_length >= position:
            target_idx = i
            break
        cumulative_dist += segment_length
    else:
        # Position beyond end - use last segment
        target_idx = len(shape) - 2

    # Select three points: [idx-1, idx, idx+1]
    idx = max(1, min(target_idx, len(shape) - 2))

    p1 = shape[idx - 1]
    p2 = shape[idx]
    p3 = shape[idx + 1]

    return menger_curvature(p1, p2, p3)
