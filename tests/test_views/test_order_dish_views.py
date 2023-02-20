from django.test import TestCase
from django.urls import reverse
from cafe.models import OrderDish, Ingredient, Order, Dish, DishType, Recipe
from django.contrib.auth import get_user_model
from django.contrib import messages


class PublicOrderDishTest(TestCase):
    def setUp(self) -> None:
        test_employee = get_user_model().objects.create(
            username="test_user",
            password="test12345"
        )
        test_dish_type = DishType.objects.create(name="test dish type")
        test_dish = Dish.objects.create(
            name="test dish",
            price=10,
            description="test",
            dish_type=test_dish_type
        )
        self.test_order = Order.objects.create(
            employee=test_employee
        )
        self.order_dish = OrderDish.objects.create(
            order=self.test_order,
            dish=test_dish,
            amount=1
        )

    def test_order_dish_create_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:order-dish-create",
            kwargs={"pk": self.test_order.id}
        ))
        self.assertNotEqual(res.status_code, 200)


class PrivateIngredientTest(TestCase):
    def setUp(self) -> None:
        test_employee = get_user_model().objects.create(
            username="test_user",
            password="test12345"
        )
        test_dish_type = DishType.objects.create(name="test dish type")
        self.test_dish = Dish.objects.create(
            name="test dish",
            price=10,
            description="test",
            dish_type=test_dish_type
        )
        self.test_order = Order.objects.create(
            employee=test_employee
        )
        self.order_dish = OrderDish.objects.create(
            order=self.test_order,
            dish=self.test_dish,
            amount=1
        )
        self.client.force_login(test_employee)

    def test_order_dish_create_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:order-dish-create",
            kwargs={"pk": self.test_order.id}
        ))
        self.assertEqual(res.status_code, 200)

    def client_post_with_arg(self, amount):
        self.test_ingredient = Ingredient.objects.create(
            name="test ingredient",
            amount_of=1
        )
        Recipe.objects.create(
            dish=self.test_dish,
            ingredient=self.test_ingredient,
            amount=1
        )
        self.test_dish.ingredients.set([self.test_ingredient])
        self.data = {
            "dish": self.test_dish.name,
            "order": self.test_order.id,
            "amount": amount,
            "create": "create"
        }
        self.res = self.client.post(
            reverse(
                "cafe:order-dish-create",
                kwargs={"pk": self.test_order.id},
            ),
            data=self.data
        )
        if messages.get_messages(self.res.wsgi_request):
            return list(messages.get_messages(self.res.wsgi_request))

    def test_order_dish_create_view_add_0_dishes(self):
        test_messages = self.client_post_with_arg(0)
        self.assertEqual(len(test_messages), 1)
        self.assertEqual(
            str(test_messages[0]),
            "You should check at least 1 pc of dishes"
        )

    def test_order_dish_create_view_add_negative_dishes(self):
        test_messages = self.client_post_with_arg(-3)
        self.assertEqual(len(test_messages), 1)
        self.assertEqual(
            str(test_messages[0]),
            "You should check at least 1 pc of dishes"
        )

    def test_order_dish_create_view_add_dishes_with_enough_ingredients(self):
        test_messages = self.client_post_with_arg(1)
        self.assertIsNone(test_messages)

    def test_order_dish_create_view_not_enough_ingredients_for_dishes(self):
        test_messages = self.client_post_with_arg(5)
        self.assertEqual(len(test_messages), 1)
        self.assertEqual(
            str(test_messages[0]),
            "Not enough ingredient: "
            f"{self.test_ingredient.name} in warehouse"
        )

    def test_order_dish_create_success_url(self):
        self.client_post_with_arg(1)
        self.assertRedirects(self.res, reverse(
            "cafe:order-create", kwargs={
                "pk": self.test_order.id,
                "create": self.data["create"]
            }
        ))
