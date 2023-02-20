from django.test import TestCase
from cafe.forms import EmployeeUpdateForm
from cafe.models import Position
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile


class EmployeeUpdateFormTests(TestCase):
    def setUp(self) -> None:
        test_position = Position.objects.create(
            name="test position",
            salary=1000
        )
        self.form_data = {
            "username": "testuser",
            "image": "avatar.png",
            "first_name": "test",
            "last_name": "last",
            "position": test_position,
            "hiring_date": timezone.localdate(timezone.now()),
            "date_of_dismissal": timezone.localdate(timezone.now())
        }
        upload_file = open("media/avatar.png", "rb")
        self.image_data = {
            "image": SimpleUploadedFile(
                upload_file.name,
                upload_file.read()
            )
        }
        self.form = EmployeeUpdateForm(
            data=self.form_data,
            files=self.image_data
        )
        self.form_data.update(self.image_data)

    def test_first_last_name_position_hiring_dismissal_date_is_valid(self):
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.cleaned_data, self.form_data)
