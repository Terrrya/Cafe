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
    success_url = reverse_lazy("cafe:dish-list")


def create_new_order(request):

    if request.GET.get("pk"):
        order = Order.objects.get(id=request.GET.get("pk"))
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
    }
    return render(
        request,
        "cafe/order_dishes_create.html",
        context
    )


def delivery(request, pk):
    order = Order.objects.get(id=pk)
    order.delivery = not order.delivery
    order.save()
    return redirect(f"{reverse_lazy('cafe:order-create')}?pk={pk}")


def select_dish(request, order_pk, dish_pk):
    return redirect(
        f"{reverse_lazy('cafe:order-create')}?pk={order_pk}&dish={dish_pk}"
    )


def cancel_order(request, pk):
    Order.objects.get(id=pk).delete()
    return redirect(reverse_lazy("cafe:dish-list"))


def delete_dish_from_order(request, order_pk, order_dish_pk):
    OrderDish.objects.get(id=order_dish_pk).delete()
    return redirect(
        f"{reverse_lazy('cafe:order-create')}?pk={order_pk}"
    )
