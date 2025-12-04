# mjh_math 모듈

수학 유틸리티 패키지 - 기본 수학 함수와 기하학 함수 제공

## 설치

```python
from mjh_math import (
    # basic_math
    normalize_angle,
    normalize_angle_half,
    get_decimal_places,
    round_to_decimal_places,
    # geometry
    get_obb_polygon,
    centerpos_from_frontcenter,
    calculate_polygon_distance,
)
```

---

## basic_math - 기본 수학 함수

### normalize_angle(angle)

각도를 [0, 360) 범위로 정규화합니다.

**Args:**
- `angle` (float): 각도 (degrees)

**Returns:**
- `normalized_angle` (float): [0, 360) 범위의 각도

**Example:**
```python
>>> normalize_angle(450)
90
>>> normalize_angle(-90)
270
```

---

### normalize_angle_half(angle)

각도를 [-180, 180) 범위로 정규화합니다.

**Args:**
- `angle` (float): 각도 (degrees)

**Returns:**
- `normalized_angle` (float): [-180, 180) 범위의 각도

**Example:**
```python
>>> normalize_angle_half(270)
-90
>>> normalize_angle_half(-270)
90
```

---

### get_decimal_places(x)

부동소수점 숫자의 소수점 자릿수를 반환합니다.

**Args:**
- `x` (float): 입력 숫자

**Returns:**
- `decimal_places` (int): 소수점 자릿수

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

값을 참조값의 소수점 자릿수에 맞춰 반올림합니다.
부동소수점 연산 오류를 해결하는 데 유용합니다.

**Args:**
- `value` (float): 반올림할 값
- `reference` (float): 소수점 자릿수 참조값

**Returns:**
- `rounded_value` (float): 반올림된 값

**Example:**
```python
>>> round_to_decimal_places(-2 * 0.2, 0.2)  # -0.4000000000000001 → -0.4
-0.4
>>> round_to_decimal_places(3 * 0.05, 0.05)  # 0.15000000000000002 → 0.15
0.15
```

---

## geometry - 기하학 함수

SUMO 시뮬레이션에서 OBB(Oriented Bounding Box) 충돌 감지 및 거리 계산용

### get_obb_polygon(x, y, width, length, angle_deg)

OBB를 Shapely Polygon으로 생성합니다.

**Args:**
- `x` (float): 중심 X 좌표
- `y` (float): 중심 Y 좌표
- `width` (float): 차량 너비 (횡방향)
- `length` (float): 차량 길이 (종방향)
- `angle_deg` (float): 회전 각도 (degrees, 0 = 오른쪽, 반시계 양수)

**Returns:**
- `polygon` (Polygon): OBB를 나타내는 Shapely Polygon

**Example:**
```python
>>> poly = get_obb_polygon(10, 5, 2.0, 5.0, 0)
>>> print(poly.bounds)  # (xmin, ymin, xmax, ymax)
(7.5, 4.0, 12.5, 6.0)
```

---

### centerpos_from_frontcenter(front_x, front_y, length, angle_deg)

전방 범퍼 중심 좌표를 차량 중심 좌표로 변환합니다.
(SUMO는 전방 범퍼 중심을 사용하지만, OBB 계산은 차량 중심이 필요)

**Args:**
- `front_x` (float): 전방 범퍼 중심 X 좌표 (SUMO 형식)
- `front_y` (float): 전방 범퍼 중심 Y 좌표 (SUMO 형식)
- `length` (float): 차량 길이
- `angle_deg` (float): 회전 각도 (degrees)

**Returns:**
- `center_position` (tuple): (center_x, center_y) - 차량 중심 좌표

**Example:**
```python
>>> # 오른쪽 방향 (0°) 차량
>>> center_x, center_y = centerpos_from_frontcenter(100, 50, 5.0, 0)
>>> print(f"Center: ({center_x}, {center_y})")
Center: (97.5, 50)

>>> # 위쪽 방향 (90°) 차량
>>> center_x, center_y = centerpos_from_frontcenter(100, 50, 5.0, 90)
>>> print(f"Center: ({center_x:.1f}, {center_y:.1f})")
Center: (100.0, 47.5)
```

---

### calculate_polygon_distance(poly1, poly2)

폴리곤 간 최소 거리를 계산합니다.
단일 폴리곤, 리스트, numpy 배열 입력을 지원합니다.

**Args:**
- `poly1` (Union[Polygon, List[Polygon], np.ndarray]): 단일 폴리곤 또는 폴리곤 배열
- `poly2` (Union[Polygon, List[Polygon], np.ndarray]): 단일 폴리곤 또는 폴리곤 배열

**Returns:**
- `distance` (Union[float, np.ndarray]): 폴리곤 쌍 간 거리 (겹치면 0)

**Example:**
```python
>>> # 1:1 - 단일 폴리곤 쌍
>>> poly1 = get_obb_polygon(0, 0, 2.0, 5.0, 0)
>>> poly2 = get_obb_polygon(10, 0, 2.0, 5.0, 0)
>>> dist = calculate_polygon_distance(poly1, poly2)
>>> print(f"Distance: {dist:.2f} m")
Distance: 5.00 m

>>> # N:N - 쌍별 거리
>>> polys1 = [get_obb_polygon(i, 0, 2, 5, 0) for i in range(3)]
>>> polys2 = [get_obb_polygon(i, 10, 2, 5, 0) for i in range(3)]
>>> dists = calculate_polygon_distance(polys1, polys2)

>>> # 1:N - 하나 대 여러 개 (브로드캐스트)
>>> ego = get_obb_polygon(0, 0, 2, 5, 0)
>>> others = [get_obb_polygon(i*10, 0, 2, 5, 0) for i in range(1, 5)]
>>> dists = calculate_polygon_distance(ego, others)
```
