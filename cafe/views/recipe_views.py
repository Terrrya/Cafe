from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.views import generic

from cafe.models import Dish, Ingredient, Recipe
from cafe.views.views import UniversalListView


class RecipeView(LoginRequiredMixin, generic.CreateView):
    model = Recipe
    fields = ["ingredient", "amount"]

    def get_form(self, form_class: ModelForm = None) -> ModelForm:
        form = super(RecipeView, self).get_form()
        dish = Dish.objects.get(id=self.kwargs["pk"])
        form.fields["ingredient"].queryset = form.fields[
            "ingredient"
        ].queryset.exclude(name__in=dish.ingredients.values_list("name"))
        return form

    def get_context_data(self, **kwargs) -> dict:
        context = super(RecipeView, self).get_context_data(**kwargs)
        context["dish"] = Dish.objects.get(id=self.kwargs["pk"])
        context["dish_recipe_ingredients"] = Recipe.objects.filter(
            dish=context["dish"]
        )
        return context

    def form_valid(self, form: ModelForm) -> ModelForm:
        form_fields = form.save(commit=False)
        form_fields.dish = Dish.objects.get(id=self.kwargs["pk"])
        form_fields.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "cafe:dish-recipe", kwargs={"pk": self.kwargs["pk"]}
        )


class RecipeListView(LoginRequiredMixin, UniversalListView):
    queryset = (
        Recipe.objects.order_by("dish__name").values_list(
            "dish__name"
        ).distinct()
    )
    key_to_search = "dish__name"
    paginate_by = 4


class RecipeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Recipe
    fields = ["ingredient", "amount"]

    def get_form(self, *args, **kwargs) -> ModelForm:
        form = super(RecipeUpdateView, self).get_form(*args, **kwargs)
        recipe = Recipe.objects.get(id=self.kwargs["pk"])
        new_queryset = form.fields["ingredient"].queryset.exclude(
            name__in=recipe.dish.ingredients.values_list("name")
        )
        form.fields["ingredient"].queryset = Ingredient.objects.filter(
            name=recipe.ingredient.name
        )
        if new_queryset:
            form.fields["ingredient"].queryset = (
                new_queryset | form.fields["ingredient"].queryset
            )
        return form

    def get_context_data(self, **kwargs) -> dict:
        context = super(RecipeUpdateView, self).get_context_data(**kwargs)
        context["dish"] = Recipe.objects.get(id=self.kwargs["pk"]).dish
        context["dish_recipe_ingredients"] = Recipe.objects.filter(
            dish=context["dish"]
        )
        return context

    def get_success_url(self) -> str:
        return reverse_lazy(
            "cafe:dish-recipe",
            kwargs={"pk": Recipe.objects.get(id=self.kwargs["pk"]).dish.id},
        )


class RecipeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Recipe

    def get_success_url(self) -> str:
        return reverse_lazy(
            "cafe:dish-recipe",
            kwargs={"pk": Recipe.objects.get(id=self.kwargs["pk"]).dish.id},
        )
