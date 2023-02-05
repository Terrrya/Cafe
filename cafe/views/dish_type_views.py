from django.views import generic
from cafe.models import DishType
from django.urls import reverse_lazy


class DishTypeCreateView(generic.CreateView):
    model = DishType
    template_name = "cafe/dish_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("cafe:dish-type-list")


class DishTypeListView(generic.ListView):
    model = DishType
    template_name = "cafe/dish_type_list.html"
    context_object_name = "dish_type_list"


class DishTypeUpdateView(generic.UpdateView):
    model = DishType
    template_name = "cafe/dish_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("cafe:dish-type-list")


class DishTypeDeleteView(generic.DeleteView):
    model = DishType
    template_name = "cafe/dish_type_confirm_delete.html"
    success_url = reverse_lazy("cafe:dish-type-list")
