from django.views import generic
from cafe.models import DishType
from django.urls import reverse_lazy
from cafe.views.views import UniversalListView
from django.contrib.auth.mixins import LoginRequiredMixin


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    template_name = "cafe/dish_type_form.html"
    fields = "__all__"


class DishTypeListView(LoginRequiredMixin, UniversalListView):
    template_name = "cafe/dish_type_list.html"
    context_object_name = "dish_type_list"
    queryset = DishType.objects.prefetch_related("dishes")
    key_to_search = "name"
    paginate_by = 5


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    template_name = "cafe/dish_type_form.html"
    fields = "__all__"


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "cafe/dish_type_confirm_delete.html"
    success_url = reverse_lazy("cafe:dish-type-list")
