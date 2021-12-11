import json

from django.http import JsonResponse
from django.middleware.csrf import get_token as get_csrf_token
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy

# TODO: figure out how to set the token when the view is *not*
# served by django
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, ListView

from .models import Employee


@csrf_exempt
def employees(request):
    rows = Employee.objects.all()
    as_json = [x.to_json() for x in rows]
    return JsonResponse(
        {
            "info": {
                "employees": as_json,
                "count": len(rows),
            },
        }
    )


@csrf_exempt
def employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "GET":
        return JsonResponse({"employee": employee.to_json()})
    elif request.method == "PUT":
        body = request.body.decode()
        payload = json.loads(body)
        employee.update(payload)
        employee.save()
        return JsonResponse({"status": "updated"})

@csrf_exempt
def new_employee(request):
    body = request.body.decode()
    payload = json.loads(body)
    employee = Employee()
    employee.update(payload)
    employee.save()
    return JsonResponse({"status": "created"})


def index(request):
    return TemplateResponse(request, "hr/index.haml")


def clean_db(request):
    if request.method == "GET":
        return TemplateResponse(request, "hr/db_confirm_delete.haml")
    else:
        Employee.objects.all().delete()
        return redirect("hr:index")


# Using Class-Based-Views here because I don't inted to customize those
class EmployeeListView(ListView):
    model = Employee
    template_name = "hr/employee_list.haml"


class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = "hr/employee_confirm_delete.haml"
    success_url = reverse_lazy("hr:employee_list")


def employee_create(request):
    if request.method == "GET":
        return employee_create_form(request, context={})
    else:
        return employee_create_action(request)


def employee_create_form(request, *, context):
    context.update(
        {
            "action": "create",
            "title": "Adding new employee",
            "form_url": reverse_lazy("hr:employee_create"),
        }
    )
    return TemplateResponse(request, "hr/employee_create.haml", context)


def employee_create_action(request):
    data, errors = process_form(
        request,
        required_fields=[
            "name",
            "address_line1",
            "city",
            "zip_code",
            "email",
        ],
        optional_fields=["address_line2"],
    )
    if errors:
        context = {"errors": errors, "form": data}
        return employee_create_form(request, context=context)
    else:
        model = Employee(**data)
        model.save()
        return redirect("hr:employee_list")


def employee_update(request, pk):
    if request.method == "GET":
        return employee_update_form(request, pk=pk, context={})
    else:
        return employee_update_action(request, pk)


def employee_update_form(request, *, pk, context):
    employee = get_object_or_404(Employee, pk=pk)
    context.update(
        {
            "action": "Update",
            "title": "Update new employee",
            "form": employee,
            "form_url": reverse_lazy("hr:employee_update", kwargs={"pk": pk}),
            "delete": True,
        }
    )
    return TemplateResponse(request, "hr/employee_update.haml", context)


def employee_update_action(request, pk):
    data, errors = process_form(
        request,
        required_fields=[
            "name",
            "address_line1",
            "city",
            "zip_code",
            "email",
        ],
        optional_fields=["address_line2"],
    )
    if errors:
        context = {"errors": errors}
        return employee_update_form(request, pk=pk, context=context)
    else:
        model = Employee(pk=pk, **data)
        model.save()
        return redirect("hr:employee_list")


def process_form(request, *, required_fields=None, optional_fields=None):
    form = request.POST
    required_fields = required_fields or []
    optional_fields = optional_fields or []
    errors = []
    data = {}
    for key in required_fields:
        value = form.get(key, "")
        if value:
            data[key] = value
        else:
            errors.append(f"Field '{key}' is required")
    for key in optional_fields:
        if form.get(key):
            value = form.get(key, "")
            if value:
                data[key] = value
    return data, errors
