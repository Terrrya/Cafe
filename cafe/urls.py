from django.urls import path
from cafe.views import index, PositionListView, DishTypeListView, \
    IngredientListView, EmployeeListView, DishListView, OrderListView, \
    PositionCreateView, PositionDeleteView, PositionUpdateView, \
    DishTypeCreateView, DishTypeUpdateView, DishTypeDeleteView, \
    IngredientCreateView, IngredientUpdateView, IngredientDeleteView, \
    EmployeeCreateView, EmployeeDetailView, EmployeeUpdateView, \
    EmployeeDeleteView, DishCreateView, DishDetailView, DishUpdateView, \
    DishDeleteView

app_name = "cafe"

urlpatterns = [
    path("home/", index, name="index"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),
    path("dish-types/create/", DishTypeCreateView.as_view(), name="dish-type-create"),
    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish-types/<int:pk>/update/", DishTypeUpdateView.as_view(), name="dish-type-update"),
    path("dish-types/<int:pk>/delete/", DishTypeDeleteView.as_view(), name="dish-type-delete"),
    path("ingredients/create/", IngredientCreateView.as_view(), name="ingredient-create"),
    path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
    path("ingredients/<int:pk>/update/", IngredientUpdateView.as_view(), name="ingredient-update"),
    path("ingredients/<int:pk>/delete/", IngredientDeleteView.as_view(), name="ingredient-delete"),
    path("employees/create/", EmployeeCreateView.as_view(), name="employee-create"),
    path("employees/", EmployeeListView.as_view(), name="employee-list"),
    path("employees/<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),
    path("employees/<int:pk>/update/", EmployeeUpdateView.as_view(), name="employee-update"),
    path("employees/<int:pk>/delete/", EmployeeDeleteView.as_view(), name="employee-delete"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dishes/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
    path("orders/", OrderListView.as_view(), name="order-list"),
]
