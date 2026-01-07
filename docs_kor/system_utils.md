# system_utils 모듈

시스템 유틸리티 - 로깅 설정 및 관리

## Import

```python
from user_library.system_utils import get_logger, setup_logger

# 또는 alias 사용
from user_library import system_utils as su
su.get_logger()
```

---

## 개요

듀얼 출력(콘솔 + 파일)을 지원하는 로거를 제공합니다.
콘솔 출력에는 로그 레벨별 색상이 자동 적용됩니다.

### 로그 레벨 라우팅

| 레벨 | 숫자 | 콘솔 | info.log | verbose.log | debug.log | 색상 |
|------|------|------|----------|-------------|-----------|------|
| DEBUG | 10 | ❌ | ❌ | ❌ | ✅ | 회색 |
| VERBOSE | 15 | ✅ | ❌ | ✅ | ❌ | 청록색 |
| FUTUREWARN | 19 | ❌ | ❌ | ❌ | ✅ | 노란색 |
| INFO | 20 | ✅ | ✅ | ❌ | ❌ | 녹색 |
| WARNING | 30 | ✅ | ✅ | ❌ | ❌ | 노란색 |
| ERROR | 40 | ✅ | ✅ | ❌ | ❌ | 빨간색 |
| CRITICAL | 50 | ✅ | ✅ | ❌ | ❌ | 굵은 빨간색 |

### 로그 레벨 상수

```python
logger = get_logger()

logger.DEBUG     # 10
logger.VERBOSE   # 15
logger.FUTUREWARN # 19
logger.INFO      # 20
logger.WARNING   # 30
logger.WARN      # 30 (별칭)
logger.ERROR     # 40
logger.CRITICAL  # 50
```

---

## get_logger(name, **kwargs)

로거 인스턴스를 가져옵니다.

**Args:**
- `name` (Optional[str]): 로거 이름 (None이면 전역 로거 반환)
- `**kwargs`: setup_logger에 전달할 추가 인자

**Returns:**
- `logger` (LoggerWrapper): to_cli 지원 로거 인스턴스

**Example:**
```python
>>> from user_library.system_utils import get_logger
>>> logger = get_logger()
>>> logger.info("Application started")
2024-01-01 12:00:00; [INFO]; [my_script.py           ]; Application started
```

---

## setup_logger(name, level, log_dir, console, file)

듀얼 출력(콘솔 + 파일)을 가진 로거를 설정합니다.

**Args:**
- `name` (str): 로거 이름 (default: "GAIL")
- `level` (int): 콘솔 로깅 레벨 (default: INFO)
- `log_dir` (str): 로그 파일 저장 디렉토리 (default: "logs")
- `console` (bool): 콘솔 출력 활성화 (default: True)
- `file` (bool): 파일 출력 활성화 (default: True)

**Returns:**
- `tuple`: (logger, log_files) - 로거 인스턴스와 로그 파일 경로 딕셔너리

**Example:**
```python
>>> from user_library.system_utils import setup_logger
>>> logger, log_files = setup_logger("MyApp", log_dir="my_logs")
```

---

## 로그 파일 구조

```
logs/
├── log_20240101_120000_info.log    # INFO 이상 로그
├── log_20240101_120000_verbose.log # VERBOSE 레벨만
└── log_20240101_120000_debug.log   # DEBUG 레벨만
```

### 로그 포맷

```
{timestamp}; [{level}]; [{filename}]; {message}
```

예시:
```
2024-01-01 12:00:00; [INFO]; [simulation.py          ]; Simulation started
2024-01-01 12:00:01; [WARN]; [vehicle.py             ]; Vehicle speed exceeds limit
```

---

## to_cli 파라미터

모든 로깅 메서드는 콘솔 출력을 제어하는 `to_cli` 파라미터를 지원합니다.

**Example:**
```python
logger = get_logger()

# 일반 로깅 (콘솔 + 파일)
logger.info("This goes to console and file")

# 파일만 저장 (콘솔 출력 생략)
logger.info("This goes to file only", to_cli=False)
logger.warning("File-only warning", to_cli=False)
logger.error("File-only error", to_cli=False)
```

---

## exc_info 파라미터

로그 출력에 traceback 정보를 포함합니다.

**Example:**
```python
logger = get_logger()

try:
    result = 1 / 0
except ZeroDivisionError:
    # 전체 traceback과 함께 에러 로깅
    logger.error("Division failed", exc_info=True)

    # 또는 exception() 메서드 사용 (exc_info=True가 기본값)
    logger.exception("Division failed")
```

---

## verbose() 메서드

VERBOSE 레벨은 ", "로 연결되는 여러 인자를 지원합니다.

**Example:**
```python
logger = get_logger()

# 단일 인자
logger.verbose("Processing step 1")

# 여러 인자 (", "로 연결)
logger.verbose("Step", "Position: 10.5", "Speed: 25.3")
# 출력: Step, Position: 10.5, Speed: 25.3
```

---

## print_log_files()

로그 파일 위치를 출력합니다. 스크립트 종료 시 자동 호출되지만, 수동으로도 호출 가능합니다.

**Example:**
```python
logger = get_logger()

# ... 작업 수행 ...

# 로그 파일 위치 출력
logger.print_log_files()
# 출력:
# Log files:
#   - info: logs/log_20240101_120000_info.log
#   - verbose: logs/log_20240101_120000_verbose.log
#   - debug: logs/log_20240101_120000_debug.log
```

---

## FutureWarning 처리

Python의 FutureWarning을 자동으로 로거로 리다이렉트합니다:
- **콘솔/info.log**: 요약만 표시 (WARNING 레벨)
- **debug.log**: 상세 정보 표시 (FUTUREWARN 레벨)

```python
import warnings
warnings.warn("This feature will be deprecated", FutureWarning)
# 콘솔: FutureWarning in my_script.py:10
# debug.log: 전체 스택 트레이스
```

---

## 전역 예외 훅

처리되지 않은 예외가 `sys.excepthook`을 통해 자동으로 로깅됩니다.
KeyboardInterrupt는 조용히 무시됩니다 (traceback 없음).

```python
# get_logger() import 시 자동 설정됨
from user_library.system_utils import get_logger
logger = get_logger()

# 처리되지 않은 모든 예외는 traceback과 함께 ERROR로 로깅됨
raise ValueError("Something went wrong")
# 로깅됨: ERROR - Unhandled exception (전체 traceback 포함)
```

---

## 활용 예시

### 기본 사용

```python
from user_library.system_utils import get_logger

logger = get_logger()

logger.debug("Debug message")      # debug.log에만 저장
logger.verbose("Verbose message")  # 콘솔(청록색) + verbose.log
logger.info("Info message")        # 콘솔(녹색) + info.log
logger.warning("Warning message")  # 콘솔(노란색) + info.log
logger.error("Error message")      # 콘솔(빨간색) + info.log
```

### 로그 레벨 상수 활용

```python
logger = get_logger()

# 레벨 상수로 직접 로깅
logger.log(logger.VERBOSE, "Custom verbose message")

# 레벨 비교
if current_level >= logger.WARNING:
    print("높은 우선순위 로그")
```

### 커스텀 로거 생성

```python
from user_library.system_utils import setup_logger
import logging

# 콘솔 출력 없이 파일만 저장
file_logger, _ = setup_logger("FileOnly", console=False)

# DEBUG 레벨부터 콘솔 출력
debug_logger, _ = setup_logger("Debug", level=logging.DEBUG)
```

### 다른 모듈에서 공유

```python
# module_a.py
from user_library.system_utils import get_logger
logger = get_logger()
logger.info("Module A initialized")

# module_b.py
from user_library.system_utils import get_logger
logger = get_logger()  # 같은 전역 로거 사용
logger.info("Module B initialized")
```

### Traceback과 함께 에러 처리

```python
logger = get_logger()

try:
    risky_operation()
except Exception as e:
    # traceback과 함께 로깅
    logger.error(f"Operation failed: {e}", exc_info=True)
```
