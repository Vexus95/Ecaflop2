from django.urls import path

from . import views

app_name = "hr"


urlpatterns = [
    path("api/v1/employees", views.employees, name="employees"),
    path("api/v1/employee/<int:pk>", views.employee, name="employee"),
    path("api/v1/employee", views.new_employee, name="new_employee"),
]
