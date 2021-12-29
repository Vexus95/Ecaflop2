from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Employee


def index(request):
    return render(request, "hr/index.html")


def reset_db(request):
    if request.method == "GET":
        return render(request, "hr/reset_db.html")
    else:
        Employee.objects.all().delete()
        return redirect("hr:employees")


def employees(request):
    rows = Employee.objects.all()
    context = {"employees": rows}
    return render(request, "hr/employees.html", context=context)


def employee(request, id):
    employee = get_object_or_404(Employee, pk=id)
    context = {"employee": employee}
    return render(request, "hr/employee.html", context=context)


def delete_employee(request, id):
    employee = get_object_or_404(Employee, pk=id)
    if request.method == "GET":
        context = {"employee": employee}
        return render(request, "hr/delete_employee.html", context=context)
    else:
        employee.delete()
        return redirect("hr:employees")


def add_employee(request):
    if request.method == "GET":
        return render(request, "hr/add_employee.html")
    else:
        creation_params = {}
        payload = request.POST
        errors = False
        for key in [
            "name",
            "email",
            "address_line1",
            "address_line2",
            "city",
            "zip_code",
            "job_title",
            "hiring_date",
        ]:
            value = payload.get(key)
            if value is not None:
                if value:
                    creation_params[key] = value
                else:
                    messages.add_message(
                        request, messages.ERROR, f"{key} cannot be blank"
                    )
                    errors = True
        if errors:
            context = {"employee": creation_params}
            return render(request, "hr/add_employee.html", context)
        else:
            Employee.objects.create(**creation_params)
            return redirect("hr:employees")


def address(request, id):
    employee = get_object_or_404(Employee, pk=id)
    context = {"employee": employee}
    if request.method == "POST":
        return update_address(request, employee)
    else:
        return render(request, "hr/address.html", context=context)


def basic(request, id):
    employee = get_object_or_404(Employee, pk=id)
    context = {"employee": employee}
    if request.method == "POST":
        return update_basic(request, employee)
    else:
        return render(request, "hr/basic.html", context=context)


def update_address(request, employee):
    payload = request.POST
    errors = False
    for key in [
        "address_line1",
        "address_line2",
        "city",
        "zip_code",
    ]:
        value = payload.get(key)
        if value is not None:
            if value:
                setattr(employee, key, value)
            else:
                messages.add_message(request, messages.ERROR, f"{key} cannot be blank")
                errors = True
    if errors:
        context = {"employee": employee}
        return render(request, "hr/basic.html", context=context)
    else:
        employee.save()
        return redirect("hr:employees")


def update_basic(request, employee):
    payload = request.POST
    errors = False
    for key in [
        "name",
        "email",
    ]:
        value = payload.get(key)
        if value is not None:
            if value:
                setattr(employee, key, value)
            else:
                messages.add_message(request, messages.ERROR, f"{key} cannot be blank")
                errors = True
    if errors:
        context = {"employee": employee}
        return render(request, "hr/basic.html", context=context)
    else:
        employee.save()
        return redirect("hr:employees")
