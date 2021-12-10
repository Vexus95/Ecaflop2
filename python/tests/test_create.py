import pytest

from hr.models import Employee


def test_form(client):
    response = client.get("/employee/create")

    assert response.status_code == 200


@pytest.mark.django_db
def test_create_with_missing_fields(client):
    response = client.post(
        "/employee/create",
        data={
            "name": "",
            "email": "homer@aol.com",
            "city": "Springfield",
            "zip_code": "12345",
            "address_line1": "1623 Main Street",
        },
    )

    assert response.status_code == 200
    context = response.context

    errors = context["errors"]
    assert errors

    # Make sure existing form data is kept
    email = context["form"]["email"]
    assert email == "homer@aol.com"


@pytest.mark.django_db
def test_create_without_line2_address(
    client,
):
    response = client.post(
        "/employee/create",
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
    assert homer.address_line2 == ""


@pytest.mark.django_db
def test_create_with_line2_address(
    client,
):
    response = client.post(
        "/employee/create",
        data={
            "name": "Homer Simpson",
            "email": "homer@aol.com",
            "city": "Springfield",
            "zip_code": "12345",
            "address_line1": "1623 Main Street",
            "address_line2": "Apartment B",
        },
    )

    assert response.status_code == 302

    actual_list = Employee.objects.all()
    assert len(actual_list) == 1
    homer = actual_list[0]
    assert homer.name == "Homer Simpson"
    assert homer.address_line1 == "1623 Main Street"
    assert homer.address_line2 == "Apartment B"
