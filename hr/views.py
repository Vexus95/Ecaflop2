from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Employee


class EmployeeListView(ListView):
    model = Employee
    template_name = "hr/employee_list.haml"


class EmployeeCreateView(CreateView):
    model = Employee
    template_name = "hr/employee_edit.haml"
    fields = [
        "name",
        "address_line1",
        "city",
        "zip_code",
        "email",
    ]
    success_url = reverse_lazy("hr:employee_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "create"
        context["title"] = "Adding new employee"
        return context


class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = "hr/employee_edit.haml"
    success_url = reverse_lazy("hr:employee_list")
    fields = [
        "name",
        "address_line1",
        "address_line2",
        "city",
        "zip_code",
        "email",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "update"
        context["title"] = "Updating employee"
        return context


class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = "hr/employee_confirm_delete.haml"
    success_url = reverse_lazy("hr:employee_list")


def index(request):
    return HttpResponse("Hello hr")
