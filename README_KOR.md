# User Library

공통 유틸리티 함수 모음 (수학, 포맷팅, 시스템 유틸리티)

해당 라이브러리는 개인 연구를 위한 Python Project에 사용하기 위해 개발되었습니다.

## 1. 모듈 구조

```
User_Library/
├── src/
│   └── user_library/          # 메인 패키지
│       ├── mjh_math/          # 수학 유틸리티
│       │   ├── basic_math.py  # 기본 수학 함수 (각도 정규화, 소수점 처리)
│       │   └── geometry.py    # 기하학 함수 (OBB, 거리 계산)
│       ├── print_format/      # 포맷팅 유틸리티
│       │   └── format_floats.py  # 숫자 포맷팅 (과학 표기법 등)
│       └── system_utils/      # 시스템 유틸리티
│           └── logger.py      # 로깅 설정
├── docs/                  # 문서
└── examples/              # 예제 노트북
```

## 2. 사용법 (How to Install)
패키지 이름: `user-library`

해당 라이브러리는 원활한 import를 위해 pip install을 해서 사용하는 것을 전제로 작성되었습니다.

### 2.1. 의존성 (Dependencies)

- Python >= 3.13 Recommended
- numpy
- shapely

> 의존성은 pip install 시 자동으로 설치됩니다.

### 2.2. 가상환경 생성 (선택사항)

```bash
python -m venv .venv  # .venv는 폴더 이름으로 자유롭게 설정 가능

# Windows
.\.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 2.3. 설치 - pip install
```bash
# Editable Install (개발용, 권장) - 소스 코드 수정 시 재설치 없이 반영됨
pip install -e .\User_Library\

# 일반 Install (비권장)** - 소스 코드가 site-packages에 복사됨
pip install .\User_Library\
```


### 2.4. 삭제 - pip uninstall

**재설치** - pyproject.toml 수정 시 (dependencies 변경, 패키지 구조 변경 등)

```bash
# 설치 여부 확인
pip show user-library

# 라이브러리 삭제
pip uninstall user-library
```

## 3. 빠른 시작

### 3.1. mjh_math - 수학 유틸리티

```python
from user_library.mjh_math import normalize_angle, get_obb_polygon, calculate_obb_distance

# 또는 alias 사용
from user_library import mjh_math as mm
mm.normalize_angle(450)

# 각도 정규화
angle = normalize_angle(450)  # 90

# OBB (Oriented Bounding Box) 생성
obb = get_obb_polygon(x=0, y=0, width=2.0, length=5.0, angle_deg=0)

# OBB 간 거리 계산
dist = calculate_obb_distance(obb1, obb2)
```

### 3.2. print_format - 포맷팅 유틸리티

```python
from user_library.print_format import format_list, format_float_to_sci, format_list_to_sci

# 또는 alias 사용
from user_library import print_format as pf
pf.format_list([1.234, 5.678])

# 리스트 포맷팅
format_list([1.234, 5.678])  # '1.23, 5.68'

# 과학 표기법 (공학 표기법)
format_float_to_sci(0.001234)  # '1.234e-03'

# 리스트를 과학 표기법으로
format_list_to_sci([0.001234, 5678.9])  # '1.234e-03, 5.679e+03'
```

### 3.3. system_utils - 시스템 관련 유틸리티

```python
from user_library.system_utils import get_logger

# 또는 alias 사용
from user_library import system_utils as su
su.get_logger()

logger = get_logger()
logger.info("Hello World")
logger.warning("Warning message")
```

## 4. 문서

자세한 문서는 [docs/](docs/) 폴더를 참조하세요.

- [mjh_math 모듈](docs/mjh_math.md)
- [print_format 모듈](docs/print_format.md)
- [system_utils 모듈](docs/system_utils.md)

## 5. 예제

예제 노트북은 [examples/](examples/) 폴더를 참조하세요.

> P.S. 예제의 경우 테스트를 위해 작성한 notebook(.ipynb) 파일을 Claude를 통해 수정하였으며, 검수되지 않았으므로 오류가 있을 수 있습니다.

- [mjh_math 예제](examples/mjh_math_examples.ipynb)
- [print_format 예제](examples/print_format_examples.ipynb)
- [system_utils 예제](examples/system_utils_examples.ipynb)
