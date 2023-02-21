from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from cafe.models import Order, OrderDish, Dish, Recipe


class OrderDishCreateView(LoginRequiredMixin, generic.CreateView):
    model = OrderDish
    template_name = "includes/form.html"
    fields = ["amount"]

    def form_valid(self, form: ModelForm) -> ModelForm | HttpResponseRedirect:
        form_fields = form.save(commit=False)
        if form_fields.amount <= 0:
            messages.warning(
                self.request, "You should check at least 1 pc of dishes"
            )
            return HttpResponseRedirect(self.get_success_url())
        form_fields.order = Order.objects.get(id=self.kwargs["pk"])
        form_fields.dish = Dish.objects.get(name=self.request.POST["dish"])
        recipe_ingredients = Recipe.objects.filter(
            dish__name=form_fields.dish.name
        )
        for recipe_ingredient in recipe_ingredients:
            recipe_ingredient.ingredient.amount_of -= (
                recipe_ingredient.amount * form_fields.amount
            )
            if recipe_ingredient.ingredient.amount_of < 0:
                messages.warning(
                    self.request,
                    "Not enough ingredient: "
                    f"{recipe_ingredient.ingredient.name} in warehouse",
                )
                return HttpResponseRedirect(self.get_success_url())
            recipe_ingredient.ingredient.save()
        form_fields.save()
        return super().form_valid(form_fields)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "cafe:order-create",
            kwargs={"pk": self.kwargs["pk"], "create": self.request.POST[
                "create"
            ]}
        )
