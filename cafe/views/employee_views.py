from django.views import generic
from cafe.forms import EmployeeForm, EmployeeUpdateForm
from cafe.models import Employee
from django.urls import reverse_lazy


class EmployeeCreateView(generic.CreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy("cafe:employee-list")


class EmployeeListView(generic.ListView):
    model = Employee


class EmployeeDetailView(generic.DetailView):
    model = Employee


class EmployeeUpdateView(generic.UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    success_url = reverse_lazy("cafe:employee-list")


class EmployeeDeleteView(generic.DeleteView):
    model = Employee
    success_url = reverse_lazy("cafe:employee-list")
