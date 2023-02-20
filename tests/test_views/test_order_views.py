from django.test import TestCase
from django.urls import reverse, reverse_lazy
from cafe.models import OrderDish, Ingredient, Order, Dish, DishType, Recipe
from django.contrib.auth import get_user_model


class PublicOrderTest(TestCase):
    def setUp(self) -> None:
        test_dish_type = DishType.objects.create(name="test dish type")
        self.test_dish = Dish.objects.create(
            name="test dish",
            dish_type=test_dish_type,
            price=10,
            description="test"
        )
        test_employee = get_user_model().objects.create_user(
            username="test user",
            password="test12345"
        )
        self.test_order = Order.objects.create(
            employee=test_employee
        )
        test_order_dish = OrderDish(
            order=self.test_order,
            dish=self.test_dish,
            amount=1
        )

    def test_order_list_view_login_required(self):
        res = self.client.get(reverse("cafe:order-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_order_delete_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:order-delete",
            kwargs={"pk": self.test_order.id}
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_create_new_order_login_required(self):
        res = self.client.get(reverse(
            "cafe:order-create",
            kwargs={"pk": 0, "create": "create"}
        ))
        self.assertNotEqual(res.status_code, 200)


class PrivateOrderTest(TestCase):
    def setUp(self) -> None:
        self.test_dish_type = DishType.objects.create(name="test dish type")
        self.test_dish = Dish.objects.create(
            name="test dish",
            dish_type=self.test_dish_type,
            price=10,
            description="test"
        )
        self.test_employee = get_user_model().objects.create_user(
            username="test user",
            password="test12345"
        )
        self.test_order = Order.objects.create(
            employee=self.test_employee
        )
        test_order_dish = OrderDish.objects.create(
            order=self.test_order,
            dish=self.test_dish,
            amount=1
        )
        self.test_order.dishes.set([self.test_dish])
        self.client.force_login(self.test_employee)

    def test_order_list_view_login_required(self):
        res = self.client.get(reverse("cafe:order-list"))
        self.assertEqual(res.status_code, 200)

    def test_order_list_get_context_data(self):
        res = self.client.get(reverse("cafe:order-list"))
        self.assertQuerysetEqual(
            res.context["order_dishes_list"],
            OrderDish.objects.select_related("dish")
        )

    def test_order_delete_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:order-delete",
            kwargs={"pk": self.test_order.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_create_new_order_login_required(self):
        res = self.client.get(reverse(
            "cafe:order-create",
            kwargs={"pk": 0, "create": "create"}
        ))
        self.assertEqual(res.status_code, 200)

    def test_create_new_order_pk_is_0(self):
        res = self.client.get(
            reverse(
                "cafe:order-create",
                kwargs={"pk": 0, "create": "create"}
            )
        )
        self.assertEqual(len(Order.objects.all()), 2)

    def test_create_new_order_pk_is_not_0(self):
        res = self.client.get(
            reverse(
                "cafe:order-create",
                kwargs={"pk": 1, "create": "create"}
            )
        )
        self.assertNotEqual(len(Order.objects.all()), 2)

    def test_create_new_order_has_context(self):
        res = self.client.get(
            reverse(
                "cafe:order-create",
                kwargs={"pk": 1, "create": "create"}
            )
        )
        self.assertEqual(res.context["new_order"], True)
        self.assertEqual(res.context["order"], self.test_order)
        self.assertQuerysetEqual(
            res.context["order_dish_list"],
            self.test_order.order_dish.all()
        )
        self.assertQuerysetEqual(
            res.context["dish_list"],
            Dish.objects.exclude(
                name__in=self.test_order.order_dish.values_list("dish__name")
            )
        )
        self.assertEqual(res.context["create"], "create")

    def test_delivery_when_order_delivery_is_true(self):
        self.test_order.delivery = True
        self.test_order.save()
        res = self.client.get(reverse(
            "cafe:delivery",
            kwargs={"pk": self.test_order.id, "create": "create"}
        ))
        self.test_order.refresh_from_db()
        self.assertEqual(self.test_order.delivery, False)

    def test_delivery_when_order_delivery_is_false(self):
        self.test_order.delivery = False
        self.test_order.save()
        res = self.client.get(reverse(
            "cafe:delivery",
            kwargs={"pk": self.test_order.id, "create": "create"}
        ))
        self.test_order.refresh_from_db()
        self.assertEqual(self.test_order.delivery, True)

    def test_delivery_redirect(self):
        res = self.client.post(reverse(
            "cafe:delivery",
            kwargs={"pk": self.test_order.id, "create": "create"}
        ))
        self.assertRedirects(res, reverse_lazy("cafe:order-create", kwargs={
            "pk": self.test_order.id,
            "create": "create"
        }))

    def test_select_dish_redirect(self):
        res = self.client.get(reverse("cafe:select-dish", kwargs={
            "order_pk": self.test_order.id,
            "dish_pk": self.test_dish.id,
            "create": "create"
        }))
        url = reverse_lazy("cafe:order-create", kwargs={
            "pk": self.test_order.id,
            "create": "create"
        })
        self.assertRedirects(res, f"{url}?dish={self.test_dish.id}")

    def test_cancel_order_create_is_create(self):
        res = self.client.get(reverse(
            "cafe:order-cancel",
            kwargs={"pk": self.test_order.id, "create": "create"}
        ))
        self.assertEqual(len(Order.objects.all()), 0)
        self.assertRedirects(res, reverse_lazy("cafe:dish-list"))

    def test_cancel_order_create_is_not_create(self):
        res = self.client.get(reverse(
            "cafe:order-cancel",
            kwargs={"pk": self.test_order.id, "create": "update"}
        ))
        self.assertEqual(len(Order.objects.all()), 1)
        self.assertRedirects(res, reverse_lazy("cafe:dish-list"))

    def test_delete_dish_from_order_back_deleted_ingredients(self):
        test_ingredient = Ingredient.objects.create(
            name="test ingredient",
            amount_of=10
        )
        test_recipe = Recipe.objects.create(
            dish=self.test_dish,
            ingredient=test_ingredient,
            amount=3
        )
        self.test_dish.ingredients.set([test_ingredient])
        res = self.client.get(reverse("cafe:delete-dish-from-order", kwargs={
            "order_pk": self.test_order.id,
            "order_dish_pk": self.test_dish.id,
            "create": "create"
        }))
        test_ingredient.refresh_from_db()
        self.assertEqual(test_ingredient.amount_of, 13)

    def test_delete_dish_from_order_redirect(self):
        res = self.client.get(reverse("cafe:delete-dish-from-order", kwargs={
            "order_pk": self.test_order.id,
            "order_dish_pk": self.test_dish.id,
            "create": "create"
        }))
        self.assertRedirects(res, reverse_lazy(
            "cafe:order-create",
            kwargs={
                "pk": self.test_order.id,
                "create": "create"
            }
        ))
