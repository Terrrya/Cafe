from django.test import TestCase
from django.urls import reverse
from cafe.models import Position
from django.contrib.auth import get_user_model


class PublicPositionTest(TestCase):
    def setUp(self) -> None:
        self.test_position = Position.objects.create(
            name="test position",
            salary=1000
        )

    def test_position_create_view_login_required(self):
        res = self.client.get(reverse("cafe:position-create"))
        self.assertNotEqual(res.status_code, 200)

    def test_position_list_view_login_required(self):
        res = self.client.get(reverse("cafe:position-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_position_update_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:position-update",
            kwargs={"pk": self.test_position.id}
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_position_delete_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:position-delete",
            kwargs={"pk": self.test_position.id}
        ))
        self.assertNotEqual(res.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self) -> None:
        self.test_position = Position.objects.create(
            name="test position",
            salary=1000
        )
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_position_create_view_login_required(self):
        res = self.client.get(reverse("cafe:position-create"))
        self.assertEqual(res.status_code, 200)

    def test_position_list_view_login_required(self):
        res = self.client.get(reverse("cafe:position-list"))
        self.assertEqual(res.status_code, 200)

    def test_position_update_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:position-update",
            kwargs={"pk": self.test_position.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_position_delete_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:position-delete",
            kwargs={"pk": self.test_position.id}
        ))
        self.assertEqual(res.status_code, 200)
