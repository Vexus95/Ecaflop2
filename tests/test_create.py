import pytest
from django.forms.models import model_to_dict

from hr.models import Employee


@pytest.mark.django_db
def test_create_with_missing_fields(client):

    response = client.post("/employee/new", data={})

    assert response.status_code == 200
    context = response.context

    actual_form = context["form"]
    assert actual_form.errors


@pytest.mark.django_db
def test_create_without_line2_address(
    client,
):
    response = client.post(
        "/employee/new",
        data={
            "name": "Homer Simpson",
            "email": "homer@aol.com",
            "city": "Springfield",
            "zip_code": "12345",
            "address_line1": "1623 Main Street",
        },
    )

    assert response.status_code == 302

    actual_list = Employee.objects.all()
    assert len(actual_list) == 1
    homer = actual_list[0]
    assert homer.name == "Homer Simpson"
    assert homer.address_line1 == "1623 Main Street"
    assert homer.address_line2 is None
