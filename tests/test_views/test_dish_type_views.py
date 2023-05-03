from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cafe.models import DishType


class PublicDishTypeTest(TestCase):
    def setUp(self) -> None:

        self.dish_type = DishType.objects.create(
            name="test dish type"
        )

    def test_dish_type_create_view_login_required(self):
        res = self.client.get(reverse("cafe:dish-type-create"))
        self.assertNotEqual(res.status_code, 200)

    def test_dish_type_list_view_login_required(self):
        res = self.client.get(reverse("cafe:dish-type-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_dish_type_update_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:dish-type-update",
            kwargs={"pk": self.dish_type.id}
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_dish_type_delete_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:dish-type-delete",
            kwargs={"pk": self.dish_type.id}
        ))
        self.assertNotEqual(res.status_code, 200)


class PrivateDishTypeTest(TestCase):
    def setUp(self) -> None:
        self.dish_type = DishType.objects.create(
            name="test dish type"
        )
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_dish_type_create_view_login_required(self):
        res = self.client.get(reverse("cafe:dish-type-create"))
        self.assertEqual(res.status_code, 200)

    def test_dish_type_list_view_login_required(self):
        res = self.client.get(reverse("cafe:dish-type-list"))
        self.assertEqual(res.status_code, 200)

    def test_dish_type_update_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:dish-type-update",
            kwargs={"pk": self.dish_type.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_dish_type_delete_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:dish-type-delete",
            kwargs={"pk": self.dish_type.id}
        ))
        self.assertEqual(res.status_code, 200)
