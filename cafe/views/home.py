import calendar
from decimal import Decimal
from django.shortcuts import render
from cafe.models import Dish, Order
from django.utils import timezone
from django.http import HttpRequest, HttpResponse


class Calendar(calendar.HTMLCalendar):

    def formatday(self, day: int, weekday: int) -> str:
        if day == 0:
            return f"<td class='{self.cssclass_noday}'>&nbsp;</td>"
        else:
            if day == timezone.localdate(timezone.now()).day:
                return f"<td class='{self.cssclasses[weekday]} " \
                       f"today'>{day}</td>"
            return f"<td class='{self.cssclasses[weekday]}'>{day}</td>"


def order_total_price_income(key: str, value: int) -> Decimal:
    orders = Order.objects.filter(**{f"created_at__{key}": value})
    return sum(order.total_price for order in orders)


def home(request: HttpRequest) -> HttpResponse:
    popular_dish = Dish.objects.first()
    unpopular_dish = popular_dish
    popular_count = 0
    unpopular_count = popular_dish.orders.count()
    for dish in Dish.objects.all():
        popularity = dish.orders.count()
        if popular_count < popularity:
            popular_dish = dish
            popular_count = popularity
        if unpopular_count > popularity:
            unpopular_count = popularity
            unpopular_dish = dish
    year, week, _ = timezone.localdate(timezone.now()).isocalendar()
    month = timezone.localdate(timezone.now()).month
    cal = Calendar().formatmonth(theyear=year, themonth=month)
    week_income = order_total_price_income("week", week)
    today_income = order_total_price_income(
        "day",
        timezone.localdate(timezone.now()).day
    )
    month_income = order_total_price_income("month", month)
    context = {
        "cal": cal,
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
