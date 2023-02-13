from django import template
from cafe.models import Dish


register = template.Library()


@register.filter()
def get_dish(value):
    return Dish.objects.get(name=value["dish__name"])
