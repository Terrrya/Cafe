from django import template


register = template.Library()


@register.filter
def queryset_filter_order(value, arg):

    return value.filter(order=arg)
