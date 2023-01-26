from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from cafe.models import Position, Employee, DishType, Ingredient, Dish, Order

admin.site.register(Position)
admin.site.register(DishType)
admin.site.register(Ingredient)
admin.site.register(Dish)
admin.site.register(Order)


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
