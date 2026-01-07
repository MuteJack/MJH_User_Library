# system_utils Module

System utilities - Logging configuration and management

## Import

```python
from user_library.system_utils import get_logger, setup_logger

# or using alias
from user_library import system_utils as su
su.get_logger()
```

---

## Overview

Provides a logger with dual output (console + file).
Console output automatically applies colors based on log level.

### Log Level Routing

| Level | Number | Console | info.log | verbose.log | debug.log | Color |
|-------|--------|---------|----------|-------------|-----------|-------|
| DEBUG | 10 | No | No | No | Yes | Gray |
| VERBOSE | 15 | Yes | No | Yes | No | Cyan |
| FUTUREWARN | 19 | No | No | No | Yes | Yellow |
| INFO | 20 | Yes | Yes | No | No | Green |
| WARNING | 30 | Yes | Yes | No | No | Yellow |
| ERROR | 40 | Yes | Yes | No | No | Red |
| CRITICAL | 50 | Yes | Yes | No | No | Bold Red |

### Log Level Constants

```python
logger = get_logger()

logger.DEBUG     # 10
logger.VERBOSE   # 15
logger.FUTUREWARN # 19
logger.INFO      # 20
logger.WARNING   # 30
logger.WARN      # 30 (alias)
logger.ERROR     # 40
logger.CRITICAL  # 50
```

---

## get_logger(name, **kwargs)

Get a logger instance.

**Args:**
- `name` (Optional[str]): Logger name (if None, returns global logger)
- `**kwargs`: Additional arguments passed to setup_logger

**Returns:**
- `logger` (LoggerWrapper): Logger instance with to_cli support

**Example:**
```python
>>> from user_library.system_utils import get_logger
>>> logger = get_logger()
>>> logger.info("Application started")
2024-01-01 12:00:00; [INFO]; [my_script.py           ]; Application started
```

---

## setup_logger(name, level, log_dir, console, file)

Setup a logger with dual output (console + file).

**Args:**
- `name` (str): Logger name (default: "GAIL")
- `level` (int): Console logging level (default: INFO)
- `log_dir` (str): Directory to save log files (default: "logs")
- `console` (bool): Enable console output (default: True)
- `file` (bool): Enable file output (default: True)

**Returns:**
- `tuple`: (logger, log_files) - Logger instance and dict of log file paths

**Example:**
```python
>>> from user_library.system_utils import setup_logger
>>> logger, log_files = setup_logger("MyApp", log_dir="my_logs")
```

---

## Log File Structure

```
logs/
├── log_20240101_120000_info.log    # INFO level and above
├── log_20240101_120000_verbose.log # VERBOSE level only
└── log_20240101_120000_debug.log   # DEBUG level only
```

### Log Format

```
{timestamp}; [{level}]; [{filename}]; {message}
```

Example:
```
2024-01-01 12:00:00; [INFO]; [simulation.py          ]; Simulation started
2024-01-01 12:00:01; [WARN]; [vehicle.py             ]; Vehicle speed exceeds limit
```

---

## to_cli Parameter

All logging methods support the `to_cli` parameter to control console output.

**Example:**
```python
logger = get_logger()

# Normal logging (console + file)
logger.info("This goes to console and file")

# File only (skip console output)
logger.info("This goes to file only", to_cli=False)
logger.warning("File-only warning", to_cli=False)
logger.error("File-only error", to_cli=False)
```

---

## exc_info Parameter

Include traceback information in log output.

**Example:**
```python
logger = get_logger()

try:
    result = 1 / 0
except ZeroDivisionError:
    # Log error with full traceback
    logger.error("Division failed", exc_info=True)

    # Or use exception() method (exc_info=True by default)
    logger.exception("Division failed")
```

---

## verbose() Method

VERBOSE level supports multiple arguments joined with ", ".

**Example:**
```python
logger = get_logger()

# Single argument
logger.verbose("Processing step 1")

# Multiple arguments (joined with ", ")
logger.verbose("Step", "Position: 10.5", "Speed: 25.3")
# Output: Step, Position: 10.5, Speed: 25.3
```

---

## print_log_files()

Print log file locations. Called automatically at script exit, but can be called manually.

**Example:**
```python
logger = get_logger()

# ... do some work ...

# Print log file locations
logger.print_log_files()
# Output:
# Log files:
#   - info: logs/log_20240101_120000_info.log
#   - verbose: logs/log_20240101_120000_verbose.log
#   - debug: logs/log_20240101_120000_debug.log
```

---

## FutureWarning Handling

Python FutureWarnings are automatically redirected to the logger:
- **Console/info.log**: Summary only (WARNING level)
- **debug.log**: Detailed information (FUTUREWARN level)

```python
import warnings
warnings.warn("This feature will be deprecated", FutureWarning)
# Console: FutureWarning in my_script.py:10
# debug.log: Full stack trace
```

---

## Global Exception Hook

Unhandled exceptions are automatically logged via `sys.excepthook`.
KeyboardInterrupt is silently ignored (no traceback).

```python
# Automatically set up when importing get_logger()
from user_library.system_utils import get_logger
logger = get_logger()

# Any unhandled exception will be logged as ERROR with traceback
raise ValueError("Something went wrong")
# Logged: ERROR - Unhandled exception (with full traceback)
```

---

## Usage Examples

### Basic Usage

```python
from user_library.system_utils import get_logger

logger = get_logger()

logger.debug("Debug message")      # debug.log only
logger.verbose("Verbose message")  # console (cyan) + verbose.log
logger.info("Info message")        # console (green) + info.log
logger.warning("Warning message")  # console (yellow) + info.log
logger.error("Error message")      # console (red) + info.log
```

### Using Log Level Constants

```python
logger = get_logger()

# Log at specific level using constant
logger.log(logger.VERBOSE, "Custom verbose message")

# Level comparison
if current_level >= logger.WARNING:
    print("High priority log")
```

### Custom Logger Creation

```python
from user_library.system_utils import setup_logger
import logging

# File output only, no console
file_logger, _ = setup_logger("FileOnly", console=False)

# Console output from DEBUG level
debug_logger, _ = setup_logger("Debug", level=logging.DEBUG)
```

### Sharing Across Modules

```python
# module_a.py
from user_library.system_utils import get_logger
logger = get_logger()
logger.info("Module A initialized")

# module_b.py
from user_library.system_utils import get_logger
logger = get_logger()  # Same global logger
logger.info("Module B initialized")
```

### Error Handling with Traceback

```python
logger = get_logger()

try:
    risky_operation()
except Exception as e:
    # Log with traceback
    logger.error(f"Operation failed: {e}", exc_info=True)
```
