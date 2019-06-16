"""Django Custom Template Tags - Math

=== Module Description ===
This module contains various django custom template tags that are used to do
mathematical operations

Current math tags available:
  - divide

@date: 06/13/2019
@author: Larry Shi
"""
from django import template
from typing import Optional, Any

register = template.Library()


@register.filter
def divide(value: Any, arg: Any) -> Optional[float]:
    """Custom django template filter.

    Integer division filter for django template language

    === Attributes ===
    numerator:
        the numerator of the division.
    denominator:
        the denominator of the division.
    """
    try:
        return round(int(value) / int(arg), 2)
    except (ValueError, ZeroDivisionError):
        return None
