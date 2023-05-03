from django import template
from django.db.models import QuerySet

from cafe.models import Order

register = template.Library()


@register.filter
def queryset_filter_order(value: QuerySet, arg: Order) -> QuerySet:

    return value.filter(order=arg)
