from django.shortcuts import render
from cafe.forms import SearchForm
from cafe.models import Dish, Order
from django.views import generic
from django.utils import timezone


def home(request):
    popular_dish = Dish.objects.first()
    unpopular_dish = popular_dish
    popular_count = popular_dish.orders.count()
    unpopular_count = popular_count
    for dish in Dish.objects.all():
        popularity = dish.orders.count()
        if popular_count < popularity:
            popular_dish = dish
            popular_count = popularity
        if unpopular_count > popularity:
            unpopular_count = popularity
            unpopular_dish = dish
    _, week, _ = timezone.now().isocalendar()
    week_orders = (Order.objects.filter(
        created_at__week=week
    ))
    week_income = sum(order.total_price for order in week_orders)
    today_orders = (Order.objects.filter(created_at__day=timezone.now().day))
    today_income = sum(order.total_price for order in today_orders)
    month_orders = (Order.objects.filter(
        created_at__month=timezone.now().month
    ))
    month_income = sum(order.total_price for order in month_orders)
    context = {
        "unpopular_dish": unpopular_dish,
        "last_month_income": month_income,
        "today_income": today_income,
        "last_week_income": week_income,
        "popular_dish": popular_dish,
        "num_sushi": Dish.objects.filter(dish_type__name="sushi").count(),
        "num_salad": Dish.objects.filter(dish_type__name="salad").count(),
        "num_pizza": Dish.objects.filter(dish_type__name="pizza").count(),
        "num_soup": Dish.objects.filter(dish_type__name="soup").count()
    }
    return render(request, "cafe/home.html", context=context)


class UniversalListView(generic.ListView):
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
