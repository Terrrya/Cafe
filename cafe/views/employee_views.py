from django.views import generic
from cafe.forms import EmployeeForm, EmployeeUpdateForm
from cafe.models import Employee
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.utils import timezone
from cafe.views.views import UniversalListView
from django.forms import ModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class EmployeeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy("cafe:employee-list")

    def get_form(self, *args, **kwargs) -> ModelForm:
        form = super(EmployeeCreateView, self).get_form(*args, **kwargs)
        form.fields["hiring_date"].initial = timezone.localdate(timezone.now())
        return form


class EmployeeListView(LoginRequiredMixin, UniversalListView):
    queryset = Employee.objects.select_related("position")
    key_to_search = "last_name"
    paginate_by = 5


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee


class EmployeeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    success_url = reverse_lazy("cafe:employee-list")


@login_required
def dismissal_employee(request: HttpRequest, pk: int) -> HttpResponse:
    employee = Employee.objects.get(id=pk)
    if employee.date_of_dismissal is None:
        employee.date_of_dismissal = timezone.localdate(timezone.now())
    else:
        employee.date_of_dismissal = None
    employee.save()
    print(type(request))
    return HttpResponseRedirect(
            f"{request.META.get('HTTP_REFERER')}"
        )


class EmployeeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Employee
    success_url = reverse_lazy("cafe:employee-list")
