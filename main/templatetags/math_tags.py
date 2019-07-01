"""Django Custom Template Tags - Math

=== Module Description ===
This module contains various django custom template tags that are used to do
mathematical operations

Current math tags available:
  - divide

@date: 06/13/2019
@author: Larry Shi
"""
from typing import Optional, Any, Union

from django import template

register = template.Library()


@register.filter
def divide(value: Any, arg: Any) -> Optional[float]:
    """Number division filter for django template language

    === Attributes ===
    value:
        the numerator of the division.
    arg:
        the denominator of the division.
    """
    try:
        return round(int(value) / int(arg), 2)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def multiply(value: Any, arg: Any) -> Optional[Union[int, float]]:
    """Number multiplication filter for django template language.

    === Attributes ===
    value:
        the first number to be multiplied.
    arg:
        the second number to be multiplied.
    """
    try:
        return round(value * arg, 1)
    except ValueError:
        return None
