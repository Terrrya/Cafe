from django.views import generic
from cafe.models import Order, OrderDish, Dish
from django.urls import reverse_lazy


class OrderDishCreateView(generic.CreateView):
    model = OrderDish
    template_name = "includes/form.html"
    fields = ["amount"]

    def form_valid(self, form):
        form_fields = form.save(commit=False)
        form_fields.order = Order.objects.get(id=self.kwargs["pk"])
        form_fields.dish = Dish.objects.get(name=self.request.POST["dish"])
        form_fields.save()
        return super().form_valid(form_fields)

    def get_success_url(self):
        return reverse_lazy(
            "cafe:order-create", kwargs={
                "pk": self.kwargs["pk"],
                "create": self.request.POST["create"]
            }
        )
