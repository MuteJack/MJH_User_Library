# print_format/format_floats.py
"""Formatting utilities for printing and display"""

import math
from typing import Optional, Union


def format_list(lst: list, fmt: str = ".2f", sep: str = ", ") -> str:
    """Format list of numbers.

    Args:
        lst (list): List of numbers to format
        fmt (str): Format specifier (default: ".2f")
        sep (str): Separator between values (default: ", ")

    Returns:
        formatted_string (str): Formatted string

    Example:
        >>> format_list([1.234, 5.678])
        '1.23, 5.68'
    """
    return sep.join(f"{x:{fmt}}" for x in lst)


def format_dict(d: dict, fmt: str = ".2f", sep: str = ", ", kv_sep: str = ": ") -> str:
    """Format dict of numbers.

    Args:
        d (dict): Dictionary with numeric values
        fmt (str): Format specifier (default: ".2f")
        sep (str): Separator between key-value pairs (default: ", ")
        kv_sep (str): Separator between key and value (default: ": ")

    Returns:
        formatted_string (str): Formatted string

    Example:
        >>> format_dict({'x': 1.234, 'y': 5.678})
        'x: 1.23, y: 5.68'
    """
    return sep.join(f"{k}{kv_sep}{v:{fmt}}" for k, v in d.items())


def format_float_to_sci(x: Optional[float], sig_figs: int = 4, eng_nots: bool = True) -> Union[None, str]:
    """Format float with significant figures in scientific notation.

    Args:
        x (Optional[float]): Number to format (None returns None)
        sig_figs (int): Number of significant figures (default: 4)
        eng_nots (bool): Use engineering notation with exponent multiple of 3 (default: True)

    Returns:
        formatted_string (Union[None, str]): Formatted string or None if input is None

    Example:
        >>> format_float_to_sci(0.001234)
        '1.234e-03'
        >>> format_float_to_sci(5678.9, eng_nots=False)
        '5.679e+03'
    """
    if x is None: return None
    if x == 0.0:  return f"0.{'0' * (sig_figs - 1)}e+00"

    exp = int(math.floor(math.log10(abs(x))))

    if eng_nots:
        exp3 = (exp // 3) * 3
        mantissa = round(x / (10 ** exp3), sig_figs - 1 - (exp - exp3))
        int_digits = exp - exp3 + 1
        dec_digits = sig_figs - int_digits
        return f"{mantissa:.{max(0, dec_digits)}f}e{exp3:+03d}"

    # Standard scientific notation: 1 digit before decimal
    mantissa = round(x / (10 ** exp), sig_figs - 1)
    return f"{mantissa:.{sig_figs - 1}f}e{exp:+03d}"


def format_list_to_sci(lst: list, sig_figs: int = 4, eng_nots: bool = True, sep: str = ", ") -> str:
    """Format list of numbers using scientific notation.

    Args:
        lst (list): List of numbers to format
        sig_figs (int): Number of significant figures (default: 4)
        eng_nots (bool): Use engineering notation with exponent multiple of 3 (default: True)
        sep (str): Separator between values (default: ", ")

    Returns:
        formatted_string (str): Formatted string

    Example:
        >>> format_list_to_sci([0.001234, 5678.9, 0.0])
        '1.234e-03, 5.679e+03, 0.000e+00'
    """
    return sep.join(format_float_to_sci(x, sig_figs, eng_nots) for x in lst)
