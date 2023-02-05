from django import template


register = template.Library()


@register.filter
def queryset_filter_dish(value, arg):
    return value.filter(dish=arg)
