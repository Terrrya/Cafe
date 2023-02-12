from django.views import generic
from django.shortcuts import redirect
from cafe.models import Order, OrderDish, Dish
from django.urls import reverse_lazy
from django.shortcuts import render


class OrderListView(generic.ListView):
    model = Order


class OrderDetailView(generic.DetailView):
    model = Order


class OrderUpdateView(generic.UpdateView):
    model = Order
    fields = "__all__"
    success_url = reverse_lazy("cafe:order-list")


class OrderDeleteView(generic.DeleteView):
    model = Order
    success_url = reverse_lazy("cafe:order-list")


def create_new_order(request, pk, create):
    if pk > 0:
        order = Order.objects.get(id=pk)
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
        "create": create
    }
    return render(
        request,
        "cafe/order_dishes_create.html",
        context
    )


def delivery(request, pk, create):
    order = Order.objects.get(id=pk)
    order.delivery = not order.delivery
    order.save()
    return redirect(reverse_lazy("cafe:order-create", kwargs={
        "pk": pk,
        "create": create
    }))


def select_dish(request, order_pk, dish_pk, create):
    url = reverse_lazy("cafe:order-create", kwargs={
        "pk": order_pk,
        "create": create
    })
    return redirect(f"{url}?dish={dish_pk}")


def cancel_order(request, pk, create):
    if create == "create":
        Order.objects.get(id=pk).delete()
    return redirect(reverse_lazy("cafe:dish-list"))


def delete_dish_from_order(request, order_pk, order_dish_pk, create):
    OrderDish.objects.get(id=order_dish_pk).delete()
    return redirect(
        reverse_lazy('cafe:order-create', kwargs={
            "pk": order_pk,
            "create": create
        })
    )
