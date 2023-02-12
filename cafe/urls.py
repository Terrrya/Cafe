from django.urls import path
from django.contrib.auth import views

from cafe.views.dish_type_views import (
    DishTypeCreateView,
    DishTypeListView,
    DishTypeUpdateView,
    DishTypeDeleteView
)
from cafe.views.dish_views import (
    DishCreateView,
    DishListView,
    DishDetailView,
    DishUpdateView,
    DishDeleteView
)
from cafe.views.employee_views import (
    EmployeeCreateView,
    EmployeeListView,
    EmployeeDetailView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    dismissal_employee
)
from cafe.views.ingredient_views import (
    IngredientCreateView,
    IngredientListView,
    IngredientUpdateView,
    IngredientDeleteView
)
from cafe.views.order_views import (
    OrderListView,
    OrderDetailView,
    OrderUpdateView,
    OrderDeleteView,
    create_new_order,
    select_dish,
    delivery,
    cancel_order,
    delete_dish_from_order
)
from cafe.views.position_views import (
    PositionCreateView,
    PositionListView,
    PositionUpdateView,
    PositionDeleteView
)
from cafe.views.recipe_views import (
    RecipeView,
    RecipeListView,
    RecipeUpdateView,
    RecipeDeleteView
)
from cafe.views.views import home
from cafe.views.order_dish_views import OrderDishCreateView

app_name = "cafe"

urlpatterns = [
    path("", views.LoginView.as_view(), name="index"),
    path("home/", home, name="home"),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path(
        "positions/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update"
    ),
    path(
        "positions/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete"
    ),
    path(
        "dish-types/create/",
        DishTypeCreateView.as_view(),
        name="dish-type-create"
    ),
    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path(
        "dish-types/<int:pk>/update/",
        DishTypeUpdateView.as_view(),
        name="dish-type-update"
    ),
    path(
        "dish-types/<int:pk>/delete/",
        DishTypeDeleteView.as_view(),
        name="dish-type-delete"
    ),
    path(
        "ingredients/create/",
        IngredientCreateView.as_view(),
        name="ingredient-create"
    ),
    path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
    path(
        "ingredients/<int:pk>/update/",
        IngredientUpdateView.as_view(),
        name="ingredient-update"
    ),
    path(
        "ingredients/<int:pk>/delete/",
        IngredientDeleteView.as_view(),
        name="ingredient-delete"
    ),
    path(
        "employees/create/",
        EmployeeCreateView.as_view(),
        name="employee-create"
    ),
    path(
        "employees/",
        EmployeeListView.as_view(),
        name="employee-list"
    ),
    path(
        "employees/<int:pk>/",
        EmployeeDetailView.as_view(),
        name="employee-detail"
    ),
    path(
        "employees/<int:pk>/update/",
        EmployeeUpdateView.as_view(),
        name="employee-update"
    ),
    path(
        "employees/<int:pk>/delete/",
        EmployeeDeleteView.as_view(),
        name="employee-delete"
    ),
    path(
        "employees/<int:pk>/dismiss",
        dismissal_employee,
        name="employee-dismissal"
    ),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path(
        "dishes/<int:pk>/update/",
        DishUpdateView.as_view(),
        name="dish-update"
    ),
    path(
        "dishes/<int:pk>/delete/",
        DishDeleteView.as_view(),
        name="dish-delete"
    ),
    path(
        "oders/<int:order_pk>/<str:create>/dish/<int:order_dish_pk>/",
        delete_dish_from_order,
        name="delete-dish-from-order"),
    path(
        "orders/<int:pk>/<str:create>/",
        create_new_order,
        name="order-create"
    ),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path(
        "order/<int:pk>/delete/",
        OrderDeleteView.as_view(),
        name="order-delete"
    ),
    path(
        "order/<int:pk>/<str:create>/cancel/",
        cancel_order,
        name="order-cancel"
    ),
    path("order/<int:pk>/<str:create>/delivery/", delivery, name="delivery"),
    path(
        "orders/<int:order_pk>/<str:create>/dish/<int:dish_pk>/",
        select_dish,
        name="select-dish"),
    path(
        "orders/<int:pk>/create/dish/",
        OrderDishCreateView.as_view(),
        name="order-dish-create"
    ),
    path("dish/<int:pk>/recipe/", RecipeView.as_view(), name="dish-recipe"),
    path("dish-recipes/", RecipeListView.as_view(), name="dish-recipe-list"),
    path(
        "dish/recipe-ingredient/<int:pk>/update/",
        RecipeUpdateView.as_view(),
        name="recipe-ingredient-update"
    ),
    path(
        "dish/recipe-ingredient/<int:pk>/delete/",
        RecipeDeleteView.as_view(),
        name="recipe-ingredient-delete"
    ),
]
