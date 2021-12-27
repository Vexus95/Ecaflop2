import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# TODO: figure out how to set the token when the view is *not*
# served by django
from django.views.decorators.csrf import csrf_exempt

from .models import Employee


@csrf_exempt
def employees(request):
    if request.method == "GET":
        rows = Employee.objects.all()
        as_json = [x.to_json() for x in rows]
        return JsonResponse(as_json, safe=False)
    elif request.method == "DELETE":
        n, _ = Employee.objects.all().delete()
        return JsonResponse({"deleted": n}, status=200)


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
        return JsonResponse({"employee": employee.to_json()}, status=200)
    elif request.method == "DELETE":
        employee.delete()
        return JsonResponse({"deleted": 1}, status=200)
    else:
        return JsonResponse({"error": "method not allowed"}, status=405)


@csrf_exempt
def new_employee(request):
    body = request.body.decode()
    payload = json.loads(body)
    employee = Employee()
    employee.update(payload)
    employee.save()
    return JsonResponse({"employee": employee.to_json()}, status=201)


@csrf_exempt
def clean_db(request):
    Employee.objects.all().delete()
    return JsonResponse({"message": "database reset"}, status=200)
