from django.urls import path
from cafe.views import index, PositionListView, DishTypeListView, \
    IngredientListView, EmployeeListView, DishListView, OrderListView, \
    PositionCreateView, PositionDeleteView, PositionUpdateView, \
    DishTypeCreateView, DishTypeUpdateView, DishTypeDeleteView, \
    IngredientCreateView, IngredientUpdateView, IngredientDeleteView

app_name = "cafe"

urlpatterns = [
    path("home/", index, name="index"),
    path("positions/create", PositionCreateView.as_view(), name="position-create"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),
    path("dish-types/create", DishTypeCreateView.as_view(), name="dish-type-create"),
    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish-types/<int:pk>/update/", DishTypeUpdateView.as_view(), name="dish-type-update"),
    path("dish-types/<int:pk>/delete/", DishTypeDeleteView.as_view(), name="dish-type-delete"),
    path("ingredients/create", IngredientCreateView.as_view(), name="ingredient-create"),
    path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
    path("ingredients/<int:pk>/update", IngredientUpdateView.as_view(), name="ingredient-update"),
    path("ingredients/<int:pk>/delete", IngredientDeleteView.as_view(), name="ingredient-delete"),
    path("employees/", EmployeeListView.as_view(), name="employee-list"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("orders/", OrderListView.as_view(), name="order-list"),
]
