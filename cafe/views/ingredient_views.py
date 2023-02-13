from django.views import generic
from cafe.models import Ingredient
from django.urls import reverse_lazy

from cafe.views.views import UniversalListView


class IngredientCreateView(generic.CreateView):
    model = Ingredient
    fields = "__all__"


class IngredientListView(UniversalListView):
    queryset = Ingredient.objects.all()
    key_to_search = "name"



class IngredientUpdateView(generic.UpdateView):
    model = Ingredient
    fields = "__all__"


class IngredientDeleteView(generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("cafe:ingredient-list")
