from django.urls import path

from . import views

app_name = "hr"


urlpatterns = [
    path("", views.index, name="index"),
    path("api/v1/employees", views.list_employees, name="employees"),
    path("api/v1/employee/<int:pk>", views.update_employee, name="employee"),
    path("api/v1/employee", views.new_employee, name="new_employee"),
]
