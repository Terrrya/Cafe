from django import template
from cafe.models import Dish


register = template.Library()


@register.filter()
def get_dish(value):
    return Dish.objects.filter(
        name__in=value
    ).select_related("dish_type").prefetch_related(
        "orders"
    ).prefetch_related("ingredients__recipes")
