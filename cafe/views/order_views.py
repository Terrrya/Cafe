from django.views import generic
from cafe.models import Order
from django.urls import reverse_lazy


class OrderCreateView(generic.CreateView):
    model = Order
    fields = "__all__"
    success_url = reverse_lazy("cafe:order-list")


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
