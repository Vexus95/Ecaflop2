from django.urls import path

from . import views

app_name = "hr"


urlpatterns = [
    path("", views.index, name="index"),
    path("reset_db", views.reset_db, name="reset_db"),
    path("add_employee", views.add_employee, name="add_employee"),
    path("employees", views.employees, name="employees"),
    path("employee/<id>/address", views.address, name="address"),
    path("employee/<id>/basic", views.basic, name="basic"),
    path("employee/<id>", views.employee, name="employee"),
    path("employee/delete/<id>>", views.delete_employee, name="delete_employee"),
]
