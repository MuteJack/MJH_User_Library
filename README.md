# User Library

A collection of common utility functions (math, formatting, system utilities)

This library was developed for personal use in Python research projects.

## 1. Module Structure

```
User_Library/
├── src/
│   └── user_library/          # Main package
│       ├── mjh_math/          # Math utilities
│       │   ├── basic_math.py  # Basic math functions (angle normalization, decimal handling)
│       │   └── geometry.py    # Geometry functions (OBB, distance calculation)
│       ├── print_format/      # Formatting utilities
│       │   └── format_floats.py  # Number formatting (scientific notation, etc.)
│       └── system_utils/      # System utilities
│           └── logger.py      # Logging configuration
├── docs/                  # Documentation
└── examples/              # Example notebooks
```

## 2. Installation

Package name: `user-library`

This library is designed to be used via pip install for seamless imports.

### 2.1. Dependencies

- Python >= 3.13 Recommended
- numpy
- shapely

> Dependencies are automatically installed during pip install.

### 2.2. Virtual Environment (Optional)

```bash
python -m venv .venv  # .venv can be any folder name

# Windows
.\.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 2.3. Install - pip install

```bash
# Editable Install (for development, recommended) - Changes to source code are reflected without reinstallation
pip install -e .\User_Library\

# Standard Install (not recommended) - Source code is copied to site-packages
pip install .\User_Library\
```

### 2.4. Uninstall - pip uninstall

**Reinstall** - When pyproject.toml is modified (dependencies changed, package structure changed, etc.)

```bash
# Check installation
pip show user-library

# Uninstall library
pip uninstall user-library
```

## 3. Quick Start

### 3.1. mjh_math - Math Utilities

```python
from user_library.mjh_math import normalize_angle, get_obb_polygon, calculate_obb_distance

# or using alias
from user_library import mjh_math as mm
mm.normalize_angle(450)

# Angle normalization
angle = normalize_angle(450)  # 90

# Create OBB (Oriented Bounding Box)
obb = get_obb_polygon(x=0, y=0, width=2.0, length=5.0, angle_deg=0)

# Calculate distance between OBBs
dist = calculate_obb_distance(obb1, obb2)
```

### 3.2. print_format - Formatting Utilities

```python
from user_library.print_format import format_list, format_float_to_sci, format_list_to_sci

# or using alias
from user_library import print_format as pf
pf.format_list([1.234, 5.678])

# List formatting
format_list([1.234, 5.678])  # '1.23, 5.68'

# Scientific notation (engineering notation)
format_float_to_sci(0.001234)  # '1.234e-03'

# List to scientific notation
format_list_to_sci([0.001234, 5678.9])  # '1.234e-03, 5.679e+03'
```

### 3.3. system_utils - System Utilities

```python
from user_library.system_utils import get_logger

# or using alias
from user_library import system_utils as su
su.get_logger()

logger = get_logger()
logger.info("Hello World")
logger.warning("Warning message")
```

## 4. Documentation

For detailed documentation, see the [docs/](docs/) folder.

- [mjh_math module](docs/mjh_math.md)
- [print_format module](docs/print_format.md)
- [system_utils module](docs/system_utils.md)

## 5. Examples

For example notebooks, see the [examples/](examples/) folder.

> P.S. The examples were modified from test notebooks using Claude and have not been fully reviewed, so there may be errors.

- [mjh_math examples](examples/mjh_math_examples.ipynb)
- [print_format examples](examples/print_format_examples.ipynb)
- [system_utils examples](examples/system_utils_examples.ipynb)
