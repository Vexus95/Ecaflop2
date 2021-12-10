from django.urls import path

from . import views

app_name = "hr"


urlpatterns = [
    path("", views.index, name="index"),
    path(
        "employees",
        views.EmployeeListView.as_view(),
        name="employee_list",
    ),
    path(
        "employee/create",
        views.employee_create,
        name="employee_create",
    ),
    path(
        "employee/<int:pk>/update",
        views.employee_update,
        name="employee_update",
    ),
    path(
        "employee/<int:pk>/delete",
        views.EmployeeDeleteView.as_view(),
        name="employee_delete",
    ),
    path(
        "clean_db",
        views.clean_db,
        name="clean_db",
    ),
]
