from django import template


register = template.Library()


@register.filter
def endswith(value: str, arg: str) -> bool:
    return value.endswith(arg)
