from django.views import generic
from cafe.forms import EmployeeForm, EmployeeUpdateForm
from cafe.models import Employee
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils import timezone

from cafe.views.views import UniversalListView


class EmployeeCreateView(generic.CreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy("cafe:employee-list")

    def get_form(self, *args, **kwargs):
        form = super(EmployeeCreateView, self).get_form(*args, **kwargs)
        form.fields["hiring_date"].initial = timezone.now()
        return form


class EmployeeListView(UniversalListView):
    queryset = Employee.objects.all()
    key_to_search = "last_name"


class EmployeeDetailView(generic.DetailView):
    model = Employee


class EmployeeUpdateView(generic.UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    success_url = reverse_lazy("cafe:employee-list")


def dismissal_employee(request, pk):
    employee = Employee.objects.get(id=pk)
    if employee.date_of_dismissal is None:
        employee.date_of_dismissal = timezone.now()
    else:
        employee.date_of_dismissal = None
    employee.save()
    return HttpResponseRedirect(
            f"{request.META.get('HTTP_REFERER')}"
        )


class EmployeeDeleteView(generic.DeleteView):
    model = Employee
    success_url = reverse_lazy("cafe:employee-list")
