from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from cafe.models import Order, OrderDish, Dish, Recipe
from cafe.views.views import UniversalListView


class OrderListView(LoginRequiredMixin, UniversalListView):
    queryset = Order.objects.select_related("employee")
    key_to_search = "created_at"
    paginate_by = 4

    def get_context_data(self, **kwargs) -> dict:
        context = super(OrderListView, self).get_context_data(**kwargs)
        context["order_dishes_list"] = OrderDish.objects.select_related("dish")
        return context


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Order
    success_url = reverse_lazy("cafe:order-list")


@login_required
def create_new_order(
        request: HttpRequest, pk: int, create: str
) -> HttpResponse:
    if pk > 0:
        order = get_object_or_404(Order, id=pk)
    else:
        for order in Order.objects.all():
            if not order.order_dish.all():
                order.delete()
        order = Order.objects.create(employee=request.user)
        order.save()
    order_dish_list = order.order_dish.all()
    dish_list = Dish.objects.exclude(
        name__in=order_dish_list.values_list("dish__name")
    )
    context = {
        "new_order": True,
        "order": order,
        "order_dish_list": order_dish_list,
        "dish_list": dish_list,
        "create": create,
    }
    return render(request, "cafe/order_dishes_create.html", context)


@login_required
def delivery(request: HttpRequest, pk: int, create: str) -> HttpResponse:
    order = get_object_or_404(Order, id=pk)
    order.delivery = not order.delivery
    order.save()
    return redirect(
        reverse_lazy("cafe:order-create", kwargs={"pk": pk, "create": create})
    )


@login_required
def select_dish(
    request: HttpRequest, order_pk: int, dish_pk: int, create: str
) -> HttpResponse:
    url = reverse_lazy("cafe:order-create", kwargs={
        "pk": order_pk, "create": create
    })
    return redirect(f"{url}?dish={dish_pk}")


@login_required
def cancel_order(request: HttpRequest, pk: int, create: str) -> HttpResponse:
    if create == "create":
        get_object_or_404(Order, id=pk).delete()
    return redirect(reverse_lazy("cafe:dish-list"))


@login_required
def delete_dish_from_order(
    request: HttpRequest, order_pk: int, order_dish_pk: int, create: str
) -> HttpResponse:
    recipe_ingredients = Recipe.objects.filter(
        dish_id=get_object_or_404(Order, id=order_dish_pk).dish.id
    )
    for recipe_ingredient in recipe_ingredients:
        recipe_ingredient.ingredient.amount_of += recipe_ingredient.amount
        recipe_ingredient.ingredient.save()
    get_object_or_404(Order, id=order_dish_pk).delete()
    return redirect(reverse_lazy("cafe:order-create", kwargs={
        "pk": order_pk, "create": create
    }))
