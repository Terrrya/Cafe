from django import forms
from django.contrib.auth.forms import UserCreationForm

from cafe.models import Employee, Dish, Recipe


class EmployeeForm(UserCreationForm):

    class Meta:
        model = Employee
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position"
        )


class EmployeeUpdateForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = (
            "username",
            "first_name",
            "last_name",
            "position"
        )

# class DishForm(forms.ModelForm):
#     amount = forms.FloatField()
#
#     class Meta:
#         model = Dish
#         exclude = "ingredients"
#
#     def save(self, commit=True):
#         dish = super(DishForm, self).save()
#
#         Recipe.objects.create(dish_id=self.cleaned_data["dish_id"], ingredients_id=[ingredient.id for ingredient in self.cleaned_data["ingredients"]], amount=self.cleaned_data["amount"])
#         return super(DishForm, self).save(commit=commit)
