from django import template


register = template.Library()


@register.filter
def not_none(value: str | int | None) -> str | int:
    return value if value else "-------"
