# print_format 모듈

숫자 포맷팅 유틸리티 - 리스트, 딕셔너리, 과학 표기법 포맷팅

## Import

```python
from user_library.print_format import (
    format_list,
    format_dict,
    format_float_to_sci,
    format_list_to_sci,
)

# or using alias
from user_library import print_format as pf
pf.format_list([1.234, 5.678])
```

---

## format_list(lst, fmt, sep)

숫자 리스트를 문자열로 포맷팅합니다.

**Args:**
- `lst` (list): 포맷할 숫자 리스트
- `fmt` (str): 포맷 지정자 (default: ".2f")
- `sep` (str): 값 사이 구분자 (default: ", ")

**Returns:**
- `formatted_string` (str): 포맷된 문자열

**Example:**
```python
>>> format_list([1.234, 5.678])
'1.23, 5.68'

>>> format_list([1.234, 5.678], fmt=".3f")
'1.234, 5.678'

>>> format_list([1.234, 5.678], sep=" | ")
'1.23 | 5.68'
```

---

## format_dict(d, fmt, sep, kv_sep)

숫자 값을 가진 딕셔너리를 문자열로 포맷팅합니다.

**Args:**
- `d` (dict): 숫자 값을 가진 딕셔너리
- `fmt` (str): 포맷 지정자 (default: ".2f")
- `sep` (str): 키-값 쌍 사이 구분자 (default: ", ")
- `kv_sep` (str): 키와 값 사이 구분자 (default: ": ")

**Returns:**
- `formatted_string` (str): 포맷된 문자열

**Example:**
```python
>>> format_dict({'x': 1.234, 'y': 5.678})
'x: 1.23, y: 5.68'

>>> format_dict({'x': 1.234, 'y': 5.678}, kv_sep="=")
'x=1.23, y=5.68'
```

---

## format_float_to_sci(x, sig_figs, eng_nots)

부동소수점 숫자를 과학 표기법으로 포맷팅합니다.

**Args:**
- `x` (Optional[float]): 포맷할 숫자 (None이면 None 반환)
- `sig_figs` (int): 유효숫자 개수 (default: 4)
- `eng_nots` (bool): 공학 표기법 사용 (지수가 3의 배수) (default: True)

**Returns:**
- `formatted_string` (Union[None, str]): 포맷된 문자열 또는 None

**Example:**
```python
>>> format_float_to_sci(0.001234)
'1.234e-03'

>>> format_float_to_sci(5678.9)
'5.679e+03'

>>> format_float_to_sci(5678.9, eng_nots=False)
'5.679e+03'

>>> format_float_to_sci(0.0)
'0.000e+00'

>>> format_float_to_sci(None)
None
```

### 공학 표기법 (Engineering Notation)

`eng_nots=True` (기본값)일 때, 지수가 3의 배수가 됩니다:
- 1e-03, 1e+00, 1e+03, 1e+06 등

이는 밀리(m), 킬로(k), 메가(M) 등의 SI 접두사와 일치합니다.

---

## format_list_to_sci(lst, sig_figs, eng_nots, sep)

숫자 리스트를 과학 표기법으로 포맷팅합니다.

**Args:**
- `lst` (list): 포맷할 숫자 리스트
- `sig_figs` (int): 유효숫자 개수 (default: 4)
- `eng_nots` (bool): 공학 표기법 사용 (default: True)
- `sep` (str): 값 사이 구분자 (default: ", ")

**Returns:**
- `formatted_string` (str): 포맷된 문자열

**Example:**
```python
>>> format_list_to_sci([0.001234, 5678.9, 0.0])
'1.234e-03, 5.679e+03, 0.000e+00'

>>> format_list_to_sci([0.001234, 5678.9], sig_figs=2)
'1.2e-03, 5.7e+03'
```

---

## 활용 예시

### 로깅에 활용

```python
from user_library.print_format import format_list_to_sci

distances = [0.00123, 0.00456, 0.00789]
print(f"Distances: {format_list_to_sci(distances)}")
# Distances: 1.230e-03, 4.560e-03, 7.890e-03
```

### 시뮬레이션 결과 출력

```python
from user_library.print_format import format_dict

results = {'position': 123.456, 'velocity': 45.678, 'acceleration': 1.234}
print(format_dict(results, fmt=".1f"))
# position: 123.5, velocity: 45.7, acceleration: 1.2
```
