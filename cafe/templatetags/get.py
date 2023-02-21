from django import template
from django.db.models import QuerySet

from cafe.models import Dish

register = template.Library()


@register.filter()
def get_dish(value: str) -> QuerySet:
    return (
        Dish.objects.filter(name__in=value)
        .select_related("dish_type")
        .prefetch_related("orders")
        .prefetch_related("ingredients__recipes")
    )
