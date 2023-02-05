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
