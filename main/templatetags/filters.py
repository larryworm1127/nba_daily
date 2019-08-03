"""Django Custom Template Filters

=== Module Description ===
This module contains various django custom template filters

Current filters available:
  - divide
  - multiply

@date: 06/13/2019
@author: Larry Shi
"""
from datetime import timedelta
from typing import Optional, Any, Union

from dateutil import parser
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
        if isinstance(arg, str) or isinstance(value, str):
            return 0

        return round(value * arg, 1)
    except ValueError:
        return None


@register.filter
def get_date(value: Any, arg: Any) -> Optional[str]:
    """Get date filter for django template language.

    === Attributes ===
    value:
        the original date in string.
    arg:
        the number of days to increase or decrease by.
    """
    date = parser.parse(value)
    return (date + timedelta(arg)).strftime("%m-%d-%Y")
