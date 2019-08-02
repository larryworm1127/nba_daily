"""Django Custom Template Tags

=== Module Description ===
This module contains various utility django custom template tags.

Current tags available:
  - arg_method

@date: 07/12/2019
@author: Larry Shi
"""
from typing import Any

from django import template

register = template.Library()


class SetVarNode(template.Node):
    """Set Variable Node Class.
    """
    var_name: str
    var_value: Any

    def __init__(self, var_name: str, var_value: Any) -> None:
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context: Any) -> str:
        """Render variable value.
        """
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value

        return u""


@register.tag(name='set')
def set_var(parser, token) -> SetVarNode:
    """Set variable django template tag.

    Syntax:
        {% set [name] = [value] %}

    Example:
        {% set some_var = '123' %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")

    return SetVarNode(parts[1], parts[3])
