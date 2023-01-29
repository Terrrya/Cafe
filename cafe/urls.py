from django.urls import path
from cafe.views import index, PositionListView, DishTypeListView, \
    IngredientListView, EmployeeListView, DishListView

app_name = "cafe"

urlpatterns = [
    path("", index, name="index"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
    path("employees/", EmployeeListView.as_view(), name="employee-list"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
]
