# mjh_math Module

Math utilities package - Basic math functions and geometry functions

## Import

```python
from user_library.mjh_math import (
    # basic_math
    normalize_angle,
    normalize_angle_half,
    get_decimal_places,
    round_to_decimal_places,
    # geometry
    get_obb_polygon,
    centerpos_from_frontcenter,
    frontcenter_from_centerpos,
    calculate_obb_distance,
    filter_points_in_radius,
    calculate_polygon_distance,
    calculate_polygon_distances,
    get_obb_bounding_margin,
)

# or using alias
from user_library import mjh_math as mm
mm.normalize_angle(450)
```

---

## basic_math - Basic Math Functions

### normalize_angle(angle)

Normalize angle to [0, 360) range.

**Args:**
- `angle` (float): Angle in degrees

**Returns:**
- `normalized_angle` (float): Angle in [0, 360) range

**Example:**
```python
>>> normalize_angle(450)
90
>>> normalize_angle(-90)
270
```

---

### normalize_angle_half(angle)

Normalize angle to [-180, 180) range.

**Args:**
- `angle` (float): Angle in degrees

**Returns:**
- `normalized_angle` (float): Angle in [-180, 180) range

**Example:**
```python
>>> normalize_angle_half(270)
-90
>>> normalize_angle_half(-270)
90
```

---

### get_decimal_places(x)

Get number of decimal places in a floating-point number.

**Args:**
- `x` (float): Input number

**Returns:**
- `decimal_places` (int): Number of decimal places

**Example:**
```python
>>> get_decimal_places(0.2)
1
>>> get_decimal_places(0.05)
2
>>> get_decimal_places(1.0)
0
```

---

### round_to_decimal_places(value, reference)

Round value to match reference value's decimal places.
Useful for resolving floating-point arithmetic errors.

**Args:**
- `value` (float): Value to round
- `reference` (float): Reference value for decimal places

**Returns:**
- `rounded_value` (float): Rounded value

**Example:**
```python
>>> round_to_decimal_places(-2 * 0.2, 0.2)  # -0.4000000000000001 → -0.4
-0.4
>>> round_to_decimal_places(3 * 0.05, 0.05)  # 0.15000000000000002 → 0.15
0.15
```

---

## geometry - Geometry Functions

For OBB (Oriented Bounding Box) collision detection and distance calculation in SUMO simulations

### get_obb_polygon(x, y, width, length, angle_deg)

Create OBB as Shapely Polygon.

**Args:**
- `x` (float): Center X coordinate
- `y` (float): Center Y coordinate
- `width` (float): Vehicle width (lateral dimension)
- `length` (float): Vehicle length (longitudinal dimension)
- `angle_deg` (float): Rotation angle (degrees, 0 = right, counterclockwise positive)

**Returns:**
- `polygon` (Polygon): Shapely Polygon representing the OBB

**Example:**
```python
>>> poly = get_obb_polygon(10, 5, 2.0, 5.0, 0)
>>> print(poly.bounds)  # (xmin, ymin, xmax, ymax)
(7.5, 4.0, 12.5, 6.0)
```

---

### centerpos_from_frontcenter(front_x, front_y, length, angle_deg)

Convert front bumper center coordinates to vehicle center coordinates.
(SUMO uses front bumper center, but OBB calculation requires vehicle center)

**Args:**
- `front_x` (float): Front bumper center X coordinate (SUMO format)
- `front_y` (float): Front bumper center Y coordinate (SUMO format)
- `length` (float): Vehicle length
- `angle_deg` (float): Rotation angle (degrees)

**Returns:**
- `center_position` (tuple): (center_x, center_y) - Vehicle center coordinates

**Example:**
```python
>>> # Vehicle pointing right (0°)
>>> center_x, center_y = centerpos_from_frontcenter(100, 50, 5.0, 0)
>>> print(f"Center: ({center_x}, {center_y})")
Center: (97.5, 50)

>>> # Vehicle pointing up (90°)
>>> center_x, center_y = centerpos_from_frontcenter(100, 50, 5.0, 90)
>>> print(f"Center: ({center_x:.1f}, {center_y:.1f})")
Center: (100.0, 47.5)
```

---

### frontcenter_from_centerpos(center_x, center_y, length, angle_deg)

Convert vehicle center coordinates to front bumper center coordinates.
Inverse of centerpos_from_frontcenter().

**Args:**
- `center_x` (float): Vehicle center X coordinate
- `center_y` (float): Vehicle center Y coordinate
- `length` (float): Vehicle length
- `angle_deg` (float): Rotation angle (degrees)

**Returns:**
- `front_position` (tuple): (front_x, front_y) - Front bumper center coordinates

**Example:**
```python
>>> # Vehicle pointing right (0°)
>>> front_x, front_y = frontcenter_from_centerpos(97.5, 50, 5.0, 0)
>>> print(f"Front: ({front_x}, {front_y})")
Front: (100.0, 50)

>>> # Vehicle pointing up (90°)
>>> front_x, front_y = frontcenter_from_centerpos(100, 47.5, 5.0, 90)
>>> print(f"Front: ({front_x:.1f}, {front_y:.1f})")
Front: (100.0, 50.0)
```

---

### filter_points_in_radius(origin, points, radius, margin)

Filter points within a circular radius (fast pre-filter).
Uses squared distance comparison for speed (no sqrt).

**Args:**
- `origin` (tuple): Origin point (x, y) or (x, y, ...)
- `points` (dict): Dict of {key: (x, y, ...)} or {key: [x, y, ...]}
- `radius` (float): Search radius in meters
- `margin` (float): Additional margin to add to radius (default: 0)

**Returns:**
- `candidates` (dict): Filtered dict {key: point} within radius + margin

**Example:**
```python
>>> origin = (100, 50)
>>> points = {'a': (101, 51), 'b': (200, 50), 'c': (105, 55)}
>>> nearby = filter_points_in_radius(origin, points, radius=10.0)
>>> # Returns {'a': (101, 51), 'c': (105, 55)}
```

---

### calculate_polygon_distance(poly1, poly2)

Calculate minimum distance between two Shapely polygons.

**Args:**
- `poly1` (Polygon): First Shapely polygon
- `poly2` (Polygon): Second Shapely polygon

**Returns:**
- `distance` (float): Minimum distance (0 if overlapping)

**Example:**
```python
>>> poly1 = get_obb_polygon(0, 0, 2, 5, 0)
>>> poly2 = get_obb_polygon(10, 0, 2, 5, 0)
>>> dist = calculate_polygon_distance(poly1, poly2)
>>> print(f"Distance: {dist:.2f} m")
Distance: 5.00 m
```

---

### calculate_polygon_distances(reference_polygon, target_polygons)

Calculate distances from reference polygon to multiple targets.
Returns results sorted by distance.

**Args:**
- `reference_polygon` (Polygon): Reference Shapely polygon
- `target_polygons` (dict): Dict of {key: Polygon}

**Returns:**
- `distances` (list): List of (key, distance) sorted by distance

**Example:**
```python
>>> ref = get_obb_polygon(0, 0, 2, 5, 0)
>>> targets = {
...     'a': get_obb_polygon(10, 0, 2, 5, 0),
...     'b': get_obb_polygon(5, 0, 2, 5, 0)
... }
>>> dists = calculate_polygon_distances(ref, targets)
>>> # Returns [('b', 0.0), ('a', 5.0)]
```

---

### get_obb_bounding_margin(length, width)

Calculate diagonal margin for OBB worst-case rotation.

**Args:**
- `length` (float): OBB length
- `width` (float): OBB width

**Returns:**
- `margin` (float): Diagonal half-length (worst-case bounding radius)

**Example:**
```python
>>> margin = get_obb_bounding_margin(5.0, 2.0)
>>> print(f"Margin: {margin:.2f} m")
Margin: 2.69 m
```

---

### calculate_obb_distance(obb1, obb2)

Calculate minimum distance between OBBs.
Supports single OBB, list, or numpy array inputs.

**Args:**
- `obb1` (Union[Polygon, List[Polygon], np.ndarray]): Single OBB or OBB array
- `obb2` (Union[Polygon, List[Polygon], np.ndarray]): Single OBB or OBB array

**Returns:**
- `distance` (Union[float, np.ndarray]): Distance(s) between OBB pairs (0 if overlapping)

**Example:**
```python
>>> # 1:1 - Single OBB pair
>>> obb1 = get_obb_polygon(0, 0, 2.0, 5.0, 0)
>>> obb2 = get_obb_polygon(10, 0, 2.0, 5.0, 0)
>>> dist = calculate_obb_distance(obb1, obb2)
>>> print(f"Distance: {dist:.2f} m")
Distance: 5.00 m

>>> # N:N - Pairwise distances
>>> obbs1 = [get_obb_polygon(i, 0, 2, 5, 0) for i in range(3)]
>>> obbs2 = [get_obb_polygon(i, 10, 2, 5, 0) for i in range(3)]
>>> dists = calculate_obb_distance(obbs1, obbs2)

>>> # 1:N - One vs many (broadcast)
>>> ego = get_obb_polygon(0, 0, 2, 5, 0)
>>> others = [get_obb_polygon(i*10, 0, 2, 5, 0) for i in range(1, 5)]
>>> dists = calculate_obb_distance(ego, others)
```
