from django.views import generic
from cafe.models import Order, OrderDish, Dish, Recipe, Ingredient
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib import messages


class OrderDishCreateView(generic.CreateView):
    model = OrderDish
    template_name = "includes/form.html"
    fields = ["amount"]

    def form_valid(self, form):
        form_fields = form.save(commit=False)
        if form_fields.amount <= 0:
            messages.warning(self.request, "You should check at least 1 pc of dishes")
            return HttpResponseRedirect(self.get_success_url())
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
