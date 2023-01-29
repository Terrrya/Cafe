from django.urls import path
from cafe.views import index, PositionListView, DishTypeListView

app_name = "cafe"

urlpatterns = [
    path("", index, name="index"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("dish-types/", DishTypeListView.as_view(), name="dish-type")
]
