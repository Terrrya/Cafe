from django import template


register = template.Library()


@register.filter
def not_none(value):
    return value if value else "-------"
