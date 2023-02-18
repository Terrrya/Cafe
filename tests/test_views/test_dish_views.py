from django.test import TestCase
from django.urls import reverse, reverse_lazy
from cafe.models import Dish, DishType
from django.contrib.auth import get_user_model


class PublicDishTest(TestCase):
    def setUp(self) -> None:
        self.dish_type = DishType.objects.create(name="test dish type")
        self.dish = Dish.objects.create(
            name="test dish",
            dish_type=self.dish_type,
            price=1000,
            description="test"
        )

    def test_dish_create_view_login_required(self):
        res = self.client.get(reverse("cafe:dish-create"))
        self.assertNotEqual(res.status_code, 200)

    def test_dish_list_view_login_required(self):
        res = self.client.get(reverse("cafe:dish-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_dish_update_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:dish-update",
            kwargs={"pk": self.dish.id}
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_dish_delete_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:dish-delete",
            kwargs={"pk": self.dish.id}
        ))
        self.assertNotEqual(res.status_code, 200)


class PrivateDishTest(TestCase):
    def setUp(self) -> None:
        self.dish_type = DishType.objects.create(name="test dish type")
        self.dish = Dish.objects.create(
            name="test dish",
            dish_type=self.dish_type,
            price=1000,
            description="test"
        )
        self.post = {
            "name": "test2 dish",
            "dish_type": self.dish_type.id,
            "price": 1000,
            "description": "test"
        }
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_dish_create_view_login_required(self):
        res = self.client.get(reverse("cafe:dish-create"))
        self.assertEqual(res.status_code, 200)

    def test_dish_create_view_success_url(self):
        res = self.client.post(reverse("cafe:dish-create"), self.post)
        self.assertRedirects(res, reverse_lazy(
            "cafe:dish-recipe",
            kwargs={"pk": Dish.objects.last().id}
        ))

    def test_dish_list_view_login_required(self):
        res = self.client.get(reverse("cafe:dish-list"))
        self.assertEqual(res.status_code, 200)

    def test_dish_update_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:dish-update",
            kwargs={"pk": self.dish.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_dish_update_view_success_url(self):
        res = self.client.post(
            reverse(
                "cafe:dish-update",
                kwargs={"pk": self.dish.id}
            ),
            self.post
        )
        self.assertRedirects(res, reverse_lazy(
            "cafe:dish-recipe",
            kwargs={"pk": Dish.objects.last().id}
        ))

    def test_dish_delete_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:dish-delete",
            kwargs={"pk": self.dish.id}
        ))
        self.assertEqual(res.status_code, 200)


