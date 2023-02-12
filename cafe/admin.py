from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from cafe.models import (
    Position,
    Employee,
    DishType,
    Ingredient,
    Dish,
    Order,
    Recipe,
    OrderDish
)

admin.site.register(DishType)
# admin.site.register(Dish)
admin.site.unregister(Group)


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        ("Staff", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "email",
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["dish", "ingredient", "amount"]


class RecipeInline(admin.TabularInline):
    model = Recipe
    verbose_name = "recipe ingredient"
    extra = 1


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name", "salary"]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name", "amount_of"]


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ["name", "dish_type", "price", "description"]
    inlines = [RecipeInline]


class OrderDishInline(admin.TabularInline):
    model = OrderDish
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["created_at", "delivery", "total_price", "employee"]
    inlines = [OrderDishInline]
