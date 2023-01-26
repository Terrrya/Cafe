from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from decimal import *


class Position(models.Model):
    name = models.CharField(max_length=255)
    salary = models.IntegerField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    position = models.ForeignKey(
        to=Position,
        on_delete=models.CASCADE,
        related_name="employees",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DishType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    amount_of = models.FloatField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255)
    dish_type = models.ForeignKey(
        to=DishType,
        on_delete=models.CASCADE,
        related_name="dishes"
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        related_name="dishes"
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    recipe = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    class Meta():
        verbose_name_plural = "dishes"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    dishes = models.ManyToManyField(
        to=Dish,
        related_name="orders"
    )
    delivery = models.BooleanField(default=False)
    employee = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    @property
    def total_price(self):
        res = 0
        for dish in self.dishes.all():
            res += dish.price
        return res

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order at {self.created_at} " \
               f"({self.employee.first_name} {self.employee.last_name})"
