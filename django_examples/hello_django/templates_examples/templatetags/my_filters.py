from django import template

register = template.Library()

@register.filter(name="upper_if_ends_with_a")
def upper_if_ends_with_a(value):
    if value.endswith("a"):
        return value.upper()
    return value