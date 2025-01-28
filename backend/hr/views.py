from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AddressForm,
    AddToTeamForm,
    BasicInfoForm,
    NewContractForm,
    TeamForm,
    UpdateContractForm,
)
from .models import Address, BasicInfo, Contract, Employee, Team


def index(request):
    return render(request, "hr/index.html")


def reset_db(request):
    if request.method == "GET":
        return render(request, "hr/reset_db.html")
    else:
        BasicInfo.objects.all().delete()
        Contract.objects.all().delete()
        Address.objects.all().delete()
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
    status = 200
    if request.method == "GET":
        address_form = AddressForm()
        basic_info_form = BasicInfoForm()
        contract_form = NewContractForm()
    else:
        address_form = AddressForm(request.POST)
        basic_info_form = BasicInfoForm(request.POST)
        contract_form = NewContractForm(request.POST)
        if (
            address_form.is_valid()
            and basic_info_form.is_valid()
            and contract_form.is_valid()
        ):
            address = address_form.save()
            basic_info = basic_info_form.save()
            contract = contract_form.save()
            Employee.objects.create(
                address=address, basic_info=basic_info, contract=contract
            )
            return redirect("hr:employees")
        else:
            status = 400
    return render(
        request,
        "hr/add_employee.html",
        {
            "address_form": address_form,
            "basic_info_form": basic_info_form,
            "contract_form": contract_form,
        },
        status=status
    )


def address(request, id):
    status = 200
    employee = get_object_or_404(Employee, pk=id)
    address = employee.address
    old_line2 = address.address_line1
    if request.method == "GET":
        form = AddressForm(instance=address)
    else:
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            # BUG
            address.address_line2 = old_line2
            address.save()
            return redirect("hr:employee", id=id)
        else:
            status = 400
    return render(request, "hr/address.html", {"form": form, "employee": employee}, status=status)


def basic_info(request, id):
    status = 200
    employee = get_object_or_404(Employee, pk=id)
    basic_info = employee.basic_info
    if request.method == "GET":
        form = BasicInfoForm(instance=basic_info)
    else:
        form = BasicInfoForm(request.POST, instance=basic_info)
        if form.is_valid():
            form.save()
            return redirect("hr:employee", id=id)
        else:
            status = 400
    return render(request, "hr/basic_info.html", {"form": form, "employee": employee}, status=status)


def contract(request, id):
    status = 200
    employee = get_object_or_404(Employee, pk=id)
    contract = employee.contract
    if request.method == "GET":
        form = UpdateContractForm(instance=contract)
    else:
        form = UpdateContractForm(request.POST, instance=contract)
        if form.is_valid():
            form.save()
            return redirect("hr:employee", id=id)
        else:
            status = 400
    return render(request, "hr/contract.html", {"form": form, "employee": employee}, status=status)


def promote(request, id):
    employee = get_object_or_404(Employee, pk=id)
    context = {"employee": employee}
    if request.method == "POST":
        employee.is_manager = True
        employee.save()
        return redirect("hr:employees")
    else:
        return render(request, "hr/promote.html", context=context)


def teams(request):
    return render(
        request,
        "hr/teams.html",
        context={"teams": Team.objects.all()},
    )


def add_team(request):
    status = 200
    if request.method == "GET":
        form = TeamForm()
    else:
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("hr:teams")
        else:
            status = 400

    return render(request, "hr/add_team.html", {"form": form}, status=status)


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
    status = 200
    employee = get_object_or_404(Employee, pk=id)
    if request.method == "GET":
        form = AddToTeamForm()
    else:
        form = AddToTeamForm(request.POST)
        if form.is_valid():
            employee.team = form.cleaned_data["team"]
            employee.save()
            return redirect("hr:employee", id=id)
        else:
            status = 400
    return render(
        request,
        "hr/add_to_team.html",
        {
            "employee": employee,
            "form": form,
        },
        status=status
    )
