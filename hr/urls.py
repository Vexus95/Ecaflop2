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
        "employee/new",
        views.EmployeeCreateView.as_view(),
        name="employee_create",
    ),
    path(
        "employee/<int:pk>/update",
        views.EmployeeUpdateView.as_view(),
        name="employee_update",
    ),
    path(
        "employee/<int:pk>/delete",
        views.EmployeeDeleteView.as_view(),
        name="employee_delete",
    ),
]
