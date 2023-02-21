from django import forms
from django.contrib.auth.forms import UserCreationForm

from cafe.models import Employee


class EmployeeForm(UserCreationForm):
    hiring_date = forms.DateField(
        widget=forms.DateInput(attrs=dict(type="date"))
    )

    class Meta:
        model = Employee
        fields = UserCreationForm.Meta.fields + (
            "image",
            "first_name",
            "last_name",
            "email",
            "position",
            "hiring_date",
        )


class EmployeeUpdateForm(forms.ModelForm):
    hiring_date = forms.DateField(
        widget=forms.DateInput(attrs=dict(type="date"))
    )
    date_of_dismissal = forms.DateField(
        widget=forms.DateInput(attrs=dict(type="date")), required=False
    )

    class Meta:
        model = Employee
        fields = (
            "image",
            "username",
            "first_name",
            "last_name",
            "position",
            "hiring_date",
            "date_of_dismissal",
        )


class SearchForm(forms.Form):
    field = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search here",
                "size": "40",
                "class": "search textbox shadow-none",
            }
        ),
    )
