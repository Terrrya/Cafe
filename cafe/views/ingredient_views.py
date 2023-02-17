from django.views import generic
from cafe.models import Ingredient
from django.urls import reverse_lazy
from cafe.views.views import UniversalListView
from django.contrib.auth.mixins import LoginRequiredMixin

class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    fields = "__all__"


class IngredientListView(LoginRequiredMixin, UniversalListView):
    queryset = Ingredient.objects.all()
    key_to_search = "name"
    paginate_by = 10


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    fields = "__all__"


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("cafe:ingredient-list")
