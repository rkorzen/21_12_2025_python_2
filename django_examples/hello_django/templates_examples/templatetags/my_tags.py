from django import template

register = template.Library()


@register.simple_tag
def upper_if_startswith(text, start):
    if text.startswith(start):
        return text.upper()
    return text