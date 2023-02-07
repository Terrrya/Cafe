from django.views import generic
from cafe.models import Ingredient
from django.urls import reverse_lazy


class IngredientCreateView(generic.CreateView):
    model = Ingredient
    fields = "__all__"


class IngredientListView(generic.ListView):
    model = Ingredient


class IngredientUpdateView(generic.UpdateView):
    model = Ingredient
    fields = "__all__"


class IngredientDeleteView(generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("cafe:ingredient-list")
