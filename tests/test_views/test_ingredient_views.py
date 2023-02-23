from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cafe.models import Ingredient


class PublicIngredientTest(TestCase):
    def setUp(self) -> None:
        self.ingredient = Ingredient.objects.create(
            name="test ingredient",
            amount_of=10
        )

    def test_ingredient_create_view_login_required(self):
        res = self.client.get(reverse("cafe:ingredient-create"))
        self.assertNotEqual(res.status_code, 200)

    def test_ingredient_list_view_login_required(self):
        res = self.client.get(reverse("cafe:ingredient-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_ingredient_update_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:ingredient-update",
            kwargs={"pk": self.ingredient.id}
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_ingredient_delete_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:ingredient-delete",
            kwargs={"pk": self.ingredient.id}
        ))
        self.assertNotEqual(res.status_code, 200)


class PrivateIngredientTest(TestCase):
    def setUp(self) -> None:
        self.ingredient = Ingredient.objects.create(
            name="test ingredient",
            amount_of=10
        )
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_ingredient_create_view_login_required(self):
        res = self.client.get(reverse("cafe:ingredient-create"))
        self.assertEqual(res.status_code, 200)

    def test_ingredient_list_view_login_required(self):
        res = self.client.get(reverse("cafe:ingredient-list"))
        self.assertEqual(res.status_code, 200)

    def test_ingredient_update_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:ingredient-update",
            kwargs={"pk": self.ingredient.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_ingredient_delete_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:ingredient-delete",
            kwargs={"pk": self.ingredient.id}
        ))
        self.assertEqual(res.status_code, 200)
