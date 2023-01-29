from django.urls import path
from cafe.views import index, PositionListView, DishTypeListView, \
    IngredientListView, EmployeeListView, DishListView, OrderListView, \
    PositionCreateView, PositionDeleteView, PositionUpdateView

app_name = "cafe"

urlpatterns = [
    path("home/", index, name="index"),
    path("positions/create", PositionCreateView.as_view(), name="position-create"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),
    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
    path("employees/", EmployeeListView.as_view(), name="employee-list"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("orders/", OrderListView.as_view(), name="order-list"),
]
