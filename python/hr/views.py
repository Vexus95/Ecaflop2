import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# TODO: figure out how to set the token when the view is *not*
# served by django
from django.views.decorators.csrf import csrf_exempt

from .models import Employee


@csrf_exempt
def list_employees(request):
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
        return JsonResponse({"employee": employee.to_json()}, status_code=202)


@csrf_exempt
def new_employee(request):
    body = request.body.decode()
    payload = json.loads(body)
    employee = Employee()
    employee.update(payload)
    employee.save()
    return JsonResponse({"employee": employee.to_json()}, status_code=201)


@csrf_exempt
def clean_db(request):
    Employee.objects.all().delete()
    return JsonResponse({"message": "database reset"}, status_code=202)
