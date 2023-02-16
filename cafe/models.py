from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal


class Position(models.Model):
    name = models.CharField(max_length=255)
    salary = models.IntegerField()

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Employee(AbstractUser):
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="avatar/",
        default="avatar.png"
    )
    position = models.ForeignKey(
        to=Position,
        on_delete=models.CASCADE,
        related_name="employees",
        blank=True,
        null=True
    )
    hiring_date = models.DateField(default=timezone.now)
    date_of_dismissal = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("cafe:dish-type-list")


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    amount_of = models.FloatField(validators=[
        MinValueValidator(0)
    ])

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("cafe:ingredient-list")


class Dish(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="dish/")
    name = models.CharField(max_length=255, unique=True)
    dish_type = models.ForeignKey(
        to=DishType,
        on_delete=models.CASCADE,
        related_name="dishes"
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        related_name="dishes",
        through="Recipe",
        through_fields=["dish", "ingredient"]
    )
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[
        MinValueValidator(0)
    ])
    description = models.TextField()

    class Meta:
        ordering = ["dish_type", "name"]
        verbose_name_plural = "dishes"

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    dish = models.ForeignKey(
        to=Dish,
        on_delete=models.CASCADE,
        related_name="recipe"
    )
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.PROTECT,
        related_name="recipes"
    )
    amount = models.FloatField(validators=[
        MinValueValidator(0)
    ])

    class Meta:
        unique_together = ["dish", "ingredient"]


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    dishes = models.ManyToManyField(
        to=Dish,
        related_name="orders",
        through="OrderDish",
        through_fields=["order", "dish"]
    )
    delivery = models.BooleanField(default=False)
    employee = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    @property
    def total_price(self) -> Decimal:
        return sum(order_dish.dish.price * order_dish.amount
                   for order_dish in self.order_dish.select_related("dish"))

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return (f"Order at {self.created_at} "
                f"({self.employee.first_name} {self.employee.last_name})")


class OrderDish(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name="order_dish",
    )
    dish = models.ForeignKey(
        to=Dish,
        on_delete=models.CASCADE,
        related_name="order_dish",
        null=True
    )
    amount = models.IntegerField()
