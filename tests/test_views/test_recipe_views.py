from django.test import TestCase
from cafe.models import Recipe, Dish, DishType, Ingredient
from django.contrib.auth import get_user_model
from django.urls import reverse


class PublicRecipeTest(TestCase):
    def setUp(self) -> None:
        test_dish_type = DishType.objects.create(name="test dish type")
        self.test_dish = Dish.objects.create(
            name="test dish",
            price=10,
            description="test",
            dish_type=test_dish_type
        )
        self.test_ingredient = Ingredient.objects.create(
            name="test ingredient",
            amount_of=1
        )
        self.test_recipe = Recipe.objects.create(
            dish=self.test_dish,
            ingredient=self.test_ingredient,
            amount=2
        )
        self.test_dish.ingredients.set([self.test_ingredient])

    def test_recipe_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:dish-recipe",
            kwargs={"pk": self.test_dish.id}
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_recipe_list_view_login_required(self):
        res = self.client.get(reverse("cafe:dish-recipe-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_recipe_update_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:recipe-ingredient-update",
            kwargs={"pk": self.test_ingredient.id}
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_recipe_delete_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:recipe-ingredient-delete",
            kwargs={"pk": self.test_ingredient.id}
        ))
        self.assertNotEqual(res.status_code, 200)


class PrivateRecipeTest(TestCase):
    def setUp(self) -> None:
        test_dish_type = DishType.objects.create(name="test dish type")
        self.test_dish = Dish.objects.create(
            name="test dish",
            price=10,
            description="test",
            dish_type=test_dish_type
        )
        self.test_ingredient = Ingredient.objects.create(
            name="test ingredient",
            amount_of=100
        )
        self.test_ingredient_2 = Ingredient.objects.create(
            name="test ingredient 2",
            amount_of=100
        )
        self.test_ingredient_3 = Ingredient.objects.create(
            name="test ingredient 3",
            amount_of=100
        )
        self.test_recipe = Recipe.objects.create(
            dish=self.test_dish,
            ingredient=self.test_ingredient,
            amount=2
        )
        self.test_dish.ingredients.set([self.test_ingredient])
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345"
        )
        self.data = {"ingredient": self.test_ingredient_2.id, "amount": 2}
        self.client.force_login(self.user)

    def test_recipe_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:dish-recipe",
            kwargs={"pk": self.test_dish.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_recipe_view_changed_ingredient_queryset(self):
        res = self.client.get(reverse(
            "cafe:dish-recipe",
            kwargs={"pk": self.test_dish.id}
        ))
        self.assertQuerysetEqual(
            res.context["form"].fields["ingredient"].queryset,
            Ingredient.objects.exclude(
                name__in=self.test_dish.ingredients.values_list("name")
            )
        )

    def test_recipe_view_added_context_data(self):
        res = self.client.get(reverse(
            "cafe:dish-recipe",
            kwargs={"pk": self.test_dish.id}
        ))
        self.assertEqual(res.context["dish"], self.test_dish)
        self.assertQuerysetEqual(
            res.context["dish_recipe_ingredients"],
            Recipe.objects.filter(dish=self.test_dish)
        )

    def test_recipe_view_success_utl(self):
        res = self.client.post(
            reverse(
                "cafe:dish-recipe",
                kwargs={"pk": self.test_dish.id}
            ),
            data=self.data
        )
        self.assertRedirects(res, reverse(
            "cafe:dish-recipe",
            kwargs={"pk": self.test_dish.id}
        ))

    def test_recipe_list_view_login_required(self):
        res = self.client.get(reverse("cafe:dish-recipe-list"))
        self.assertEqual(res.status_code, 200)

    def test_recipe_update_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:recipe-ingredient-update",
            kwargs={"pk": self.test_ingredient.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_recipe_update_view_changed_ingredient_queryset(self):
        res = self.client.get(reverse(
            "cafe:recipe-ingredient-update",
            kwargs={"pk": self.test_ingredient.id}
        ))
        self.assertQuerysetEqual(
            res.context["form"].fields["ingredient"].queryset,
            Ingredient.objects.exclude(
                name__in=self.test_dish.ingredients.values_list("name")
            ) | Ingredient.objects.filter(
                name=self.test_ingredient.name
            )
        )

    def test_recipe_update_view_added_context_data(self):
        res = self.client.get(reverse(
            "cafe:recipe-ingredient-update",
            kwargs={"pk": self.test_ingredient.id}
        ))
        self.assertEqual(res.context["dish"], self.test_dish)
        self.assertQuerysetEqual(
            res.context["dish_recipe_ingredients"],
            Recipe.objects.filter(dish=self.test_dish)
        )

    def test_recipe_update_view_success_url(self):
        res = self.client.post(
            reverse(
                "cafe:recipe-ingredient-update",
                kwargs={"pk": self.test_ingredient.id}
            ),
            data=self.data
        )
        self.assertRedirects(res, reverse("cafe:dish-recipe", kwargs={
            "pk": self.test_dish.id
        }))

    def test_recipe_delete_view_login_required(self):
        res = self.client.get(reverse(
            "cafe:recipe-ingredient-delete",
            kwargs={"pk": self.test_ingredient.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_recipe_delete_view_success_url(self):
        res = self.client.post(reverse(
            "cafe:recipe-ingredient-delete",
            kwargs={"pk": self.test_ingredient.id}
        ))
        self.assertRedirects(res, reverse("cafe:dish-recipe", kwargs={
            "pk": self.test_dish.id
        }))
