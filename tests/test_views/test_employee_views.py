from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone


class PublicEmployeeTest(TestCase):
    def setUp(self) -> None:
        self.employee = get_user_model().objects.create_user(
            username="test_user",
            password="test12345"
        )

    def test_create_view_login_required(self):
        res = self.client.get(reverse("cafe:employee-create"))
        self.assertNotEqual(res.status_code, 200)

    def test_list_view_login_required(self):
        res = self.client.get(reverse("cafe:employee-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_detail_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:employee-detail",
            kwargs={"pk": self.employee.id}
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_update_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:employee-update",
            kwargs={"pk": self.employee.id}
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_delete_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:employee-delete",
            kwargs={"pk": self.employee.id}
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_dismissal_employee_login_required(self):
        res = self.client.get(reverse(
            "cafe:employee-dismissal",
            kwargs={"pk": self.employee.id}
        ))


class PrivateEmployeeTest(TestCase):
    def setUp(self) -> None:
        self.employee = get_user_model().objects.create_user(
            username="test_user",
            password="test12345"
        )
        self.client.force_login(self.employee)

    def test_create_view_login_required(self):
        res = self.client.get(reverse("cafe:employee-create"))
        self.assertEqual(res.status_code, 200)

    def test_create_view_form_field_initial(self):
        res = self.client.get(reverse("cafe:employee-create"))
        self.assertIsNotNone(res.context["form"]["hiring_date"])

    def test_list_view_login_required(self):
        res = self.client.get(reverse("cafe:employee-list"))
        self.assertEqual(res.status_code, 200)

    def test_detail_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:employee-detail",
            kwargs={"pk": self.employee.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_update_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:employee-update",
            kwargs={"pk": self.employee.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_delete_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:employee-delete",
            kwargs={"pk": self.employee.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_dismissal_employee_login_required(self):
        res = self.client.get(reverse(
            "cafe:employee-dismissal",
            kwargs={"pk": self.employee.id}
        ))

    def test_dismissal_employee_add_date_of_dismissal(self):
        res = self.client.get(reverse(
            "cafe:employee-dismissal",
            kwargs={"pk": self.employee.id}
        ))
        self.employee.refresh_from_db()
        self.assertIsNotNone(self.employee.date_of_dismissal)

    def test_dismissal_employee_remove_date_of_dismissal(self):
        self.employee.date_of_dismissal = timezone.now()
        self.employee.save()
        res = self.client.get(reverse(
            "cafe:employee-dismissal",
            kwargs={"pk": self.employee.id}
        ))
        self.employee.refresh_from_db()
        self.assertIsNone(self.employee.date_of_dismissal)
