"""
Internal functions and helpers for Fourth.
Anything defined here IS NOT part of the public API, and can change at any time.
"""
from __future__ import annotations

__all__ = ("contains_timezone",)


def contains_timezone(format_string: str) -> bool:
    """
    Give an strftime style format string, check if it contains a %Z or %z timezone
    format directive.

    :param format_string: The format string to check.
    :return: True if it does contain a timezone directive. False otherwise.
    """
    is_format_char = False  # if the current character is after a "%"

    for character in format_string:
        if is_format_char:
            if character == "z" or character == "Z":
                return True
            else:
                is_format_char = False
        else:
            if character == "%":
                is_format_char = True

    return False  # reached end of string without finding one, return False
