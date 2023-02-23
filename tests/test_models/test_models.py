from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from cafe.models import Position, DishType, Ingredient, Dish, Order


class ModelsTests(TestCase):
    def test_position_str(self):
        test_position = Position.objects.create(
            name="test position",
            salary=1000
        )
        self.assertEqual(str(test_position), test_position.name)

    def test_employee_str(self):
        test_employee = get_user_model().objects.create_user(
            username="test_user",
            password="test12345"
        )
        self.assertEqual(
            str(test_employee),
            f"{test_employee.first_name} {test_employee.last_name}"
        )

    def test_employee_with_image_position_hiring_date_dismissal(self):
        test_position = Position.objects.create(
            name="test position",
            salary=1000
        )
        username = "test_user",
        password = "test12345"
        image = SimpleUploadedFile(
            name="test.jpg",
            content=b"",
            content_type="image/png"
        )
        position = test_position
        hiring_date = timezone.localdate(timezone.now())
        date_of_dismissal = timezone.localdate(timezone.now())
        test_employee = get_user_model().objects.create_user(
            username=username,
            password=password,
            image=image,
            position=position,
            hiring_date=hiring_date,
            date_of_dismissal=date_of_dismissal
        )
        # self.assert
        self.assertEqual(test_employee.username, username)
        self.assertTrue(test_employee.check_password(password))
        self.assertIsNotNone(test_employee.image)
        self.assertEqual(test_employee.position, position)
        self.assertEqual(test_employee.hiring_date, hiring_date)
        self.assertEqual(test_employee.date_of_dismissal, date_of_dismissal)

    def test_dish_type_str(self):
        test_dish_type = DishType.objects.create(
            name="test dish type",
        )
        self.assertEqual(str(test_dish_type), test_dish_type.name)

    def test_ingredient_str(self):
        test_ingredient = Ingredient.objects.create(name="test", amount_of=100)
        self.assertEqual(str(test_ingredient), test_ingredient.name)

    def test_dish_str(self):
        test_dish_type = DishType.objects.create(name="test dish type")
        test_dish = Dish.objects.create(
            image=SimpleUploadedFile(
                name="test.jpg",
                content=b"",
                content_type="image/png"
            ),
            name="test dish",
            dish_type=test_dish_type,
            price=Decimal(15),
            description="test"
        )
        self.assertEqual(str(test_dish), test_dish.name)

    def test_order_total_price(self):
        test_employee = get_user_model().objects.create(
            username="test_user",
            password="test12345"
        )
        test_order = Order.objects.create(
            created_at=timezone.localdate(timezone.now()),
            is_delivery=False,
            employee=test_employee
        )
        self.assertEqual(
            str(test_order),
            f"Order at {test_order.created_at} ({test_employee.first_name} "
            f"{test_employee.last_name})"
        )
