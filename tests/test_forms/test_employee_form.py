from django.test import TestCase
from cafe.forms import EmployeeForm
from cafe.models import Position
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile


class EmployeeFormTests(TestCase):
    def setUp(self) -> None:
        test_position = Position.objects.create(
            name="test position",
            salary=1000
        )
        self.form_data = {
            "username": "testuser",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "test",
            "last_name": "last",
            "email": "test@test.com",
            "position": test_position,
            "hiring_date": timezone.localdate(timezone.now())
        }
        upload_file = open("media/avatar.png", "rb")
        self.image_data = {
            "image": SimpleUploadedFile(
                upload_file.name,
                upload_file.read()
            )
        }
        self.form = EmployeeForm(data=self.form_data, files=self.image_data)
        self.form_data.update(self.image_data)

    def test_first_Last_name_position_hiring_date_is_valid(self):
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.cleaned_data, self.form_data)
