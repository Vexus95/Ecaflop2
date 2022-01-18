from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import BasicInfo, Contract, Employee, Team


def index(request):
    return render(request, "hr/index.html")


def reset_db(request):
    if request.method == "GET":
        return render(request, "hr/reset_db.html")
    else:
        BasicInfo.objects.all().delete()
        Contract.objects.all().delete()
        Employee.objects.all().delete()
        Team.objects.all().delete()
        return redirect("hr:index")


def employees(request):
    return render(
        request,
        "hr/employees.html",
        context={"employees": Employee.objects.all()},
    )


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
        payload = request.POST
        errors = False

        # Basic
        basic_keys = [
            "name",
            "email",
        ]
        basic_params = {}
        for key in basic_keys:
            value = payload.get(key)
            if value is not None:
                if value:
                    basic_params[key] = value
                else:
                    messages.add_message(
                        request, messages.ERROR, f"{key} cannot be blank"
                    )
                    errors = True

        # Address
        address_keys = [
            "address_line1",
            "address_line2",
            "city",
            "zip_code",
        ]
        address_params = {}
        for key in address_keys:
            value = payload.get(key)
            if value is not None:
                if value:
                    address_params[key] = value
                    if key == "zip_code":
                        try:
                            int(value)
                        except ValueError:
                            messages.add_message(
                                request, messages.ERROR, "zip_code must be an int"
                            )
                            errors = True
                else:
                    messages.add_message(
                        request, messages.ERROR, f"{key} cannot be blank"
                    )
                    errors = True

        # Legal
        contract_keys = [
            "hiring_date",
            "job_title",
        ]
        contract_params = {}
        for key in contract_keys:
            value = payload.get(key)
            if value is not None:
                if value:
                    contract_params[key] = value
                else:
                    messages.add_message(
                        request, messages.ERROR, f"{key} cannot be blank"
                    )
                    errors = True

        if errors:
            employee = {
                "name": basic_params.get("name", ""),
                "email": basic_params.get("email", ""),
                "basic_info": address_params,
                "contract": contract_params,
            }
            context = {"employee": employee}
            print(context)
            return render(request, "hr/add_employee.html", context)
        else:
            basic_info = BasicInfo.objects.create(**basic_params, **address_params)
            contract = Contract.objects.create(**contract_params)
            Employee.objects.create(basic_info=basic_info, contract=contract)
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


def legal(request, id):
    employee = get_object_or_404(Employee, pk=id)
    context = {"employee": employee}
    if request.method == "POST":
        return update_legal(request, employee)
    else:
        return render(request, "hr/legal.html", context=context)


def update_address(request, employee):
    payload = request.POST
    errors = False
    basic_info = employee.basic_info
    for key in [
        "address_line1",
        "address_line2",
        "city",
        "zip_code",
    ]:
        value = payload.get(key)
        if value is not None:
            if value:
                setattr(basic_info, key, value)
            else:
                messages.add_message(request, messages.ERROR, f"{key} cannot be blank")
                errors = True
    if errors:
        context = {"employee": employee}
        return render(request, "hr/basic.html", context=context)
    else:
        basic_info.save()
        return redirect("hr:employees")


def update_basic(request, employee):
    payload = request.POST
    errors = False
    keys = ["name", "email"]
    basic_info = employee.basic_info
    for key in keys:
        value = payload.get(key)
        if value is not None:
            if value:
                setattr(basic_info, key, value)
            else:
                messages.add_message(request, messages.ERROR, f"{key} cannot be blank")
                errors = True
    if errors:
        context = {"employee": employee}
        return render(request, "hr/basic.html", context=context)
    else:
        basic_info.save()
        return redirect("hr:employees")


def update_legal(request, employee):
    payload = request.POST
    errors = False
    contract = employee.contract
    for key in [
        "job_title",
        "hiring_date",
    ]:
        value = payload.get(key)
        if value is not None:
            if value:
                setattr(contract, key, value)
            else:
                messages.add_message(request, messages.ERROR, f"{key} cannot be blank")
                errors = True
    if errors:
        context = {"employee": employee}
        return render(request, "hr/legal.html", context=context)
    else:
        contract.save()
        return redirect("hr:employees")


def promote(request, id):
    employee = get_object_or_404(Employee, pk=id)
    context = {"employee": employee}
    if request.method == "POST":
        return promote_employee(request, employee)
    else:
        return render(request, "hr/promote.html", context=context)


def promote_employee(request, employee):
    employee.is_manager = True
    employee.save()
    return redirect("hr:employees")


def teams(request):
    return render(
        request,
        "hr/teams.html",
        context={"teams": Team.objects.all()},
    )


def add_team(request):
    if request.method == "POST":
        payload = request.POST
        errors = False
        creation_params = {}
        for key in [
            "name",
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
            context = {"team": creation_params}
            return render(request, "hr/add_team", context=context)
        else:
            team = Team.objects.create(**creation_params)
            team.save()
            return redirect("hr:teams")
    else:
        return render(
            request,
            "hr/add_team.html",
        )


def team(request, id):
    team = get_object_or_404(Team, pk=id)
    return render(
        request,
        "hr/team.html",
        context={"team": team},
    )


def members(request, id):
    team = get_object_or_404(Team, pk=id)
    members = Employee.objects.filter(team=team)
    return render(
        request,
        "hr/members.html",
        context={"team": team, "members": members},
    )


def delete_team(request, id):
    team = get_object_or_404(Team, pk=id)
    if request.method == "GET":
        return render(
            request,
            "hr/delete_team.html",
            context={"team": team},
        )
    else:
        team.delete()
        return redirect("hr:teams")


def add_to_team(request, id):
    employee = get_object_or_404(Employee, pk=id)
    teams = Team.objects.all()
    context = {
        "employee": employee,
        "teams": teams,
    }
    if request.method == "GET":
        return render(request, "hr/add_to_team.html", context=context)
    else:
        team_id = request.POST.get("team_id")
        if not team_id:
            messages.add_message(request, messages.ERROR, "Please select a team")
            return render(request, "hr/add_to_team.html", context=context)
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            messages.add_message(request, messages.ERROR, "No such team")
            return render(request, "hr/add_to_team.html", context=context)

        employee.team = team
        employee.save()
        return redirect("hr:teams")
