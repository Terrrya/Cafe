from django.shortcuts import render

from cafe.forms import SearchForm
from cafe.models import Dish, Order
from django.views import generic

# def index(request):
#     context = {
#         "num_sushi": Dish.objects.filter(dish_type__name="sushi").count(),
#         "num_salad": Dish.objects.filter(dish_type__name="salad").count(),
#         "num_pizza": Dish.objects.filter(dish_type__name="pizza").count(),
#         "num_soup": Dish.objects.filter(dish_type__name="soup").count()
#     }
#     return render(request, "cafe/index.html", context=context)


def home(request):
    context = {
        "orders": Order.objects.filter(employee=request.user),
        "num_sushi": Dish.objects.filter(dish_type__name="sushi").count(),
        "num_salad": Dish.objects.filter(dish_type__name="salad").count(),
        "num_pizza": Dish.objects.filter(dish_type__name="pizza").count(),
        "num_soup": Dish.objects.filter(dish_type__name="soup").count()
    }
    return render(request, "cafe/home.html", context=context)


class UniversalListView(generic.ListView):
    # paginate_by = 3
    key_to_search = ""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UniversalListView, self).get_context_data(**kwargs)
        context["search_form"] = SearchForm(initial={
            "field": self.request.GET.get("field", "")
        })
        return context

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(**{
                f"{self.key_to_search}__icontains": form.cleaned_data["field"]
            })
        return self.queryset
