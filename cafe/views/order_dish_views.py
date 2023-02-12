from django.views import generic
from cafe.models import Order, OrderDish, Dish
from django.urls import reverse_lazy


class OrderDishCreateView(generic.CreateView):
    model = OrderDish
    template_name = "includes/form.html"
    fields = ["amount"]
    success_url = reverse_lazy("cafe:order-create")

    def form_valid(self, form):
        form_fields = form.save(commit=False)
        form_fields.order = Order.objects.get(id=self.kwargs["pk"])
        form_fields.dish = Dish.objects.get(name=self.request.POST["dish"])
        form_fields.save()
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return f"{reverse_lazy('cafe:order-create')}?pk={pk}"
