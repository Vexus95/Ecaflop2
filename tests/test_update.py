import pytest
from django.forms.models import model_to_dict


@pytest.mark.django_db
def test_update_mail(client, homer):
    homer.save()

    homer.email = "new@fastmail.com"
    response = client.post(f"/employee/{homer.pk}/update", data=model_to_dict(homer))

    if response.status_code != 302:
        form = response.context["form"]
        pytest.fail(f"Form contained errors {dict(form.errors)}")

    homer.refresh_from_db()
    assert homer.email == "new@fastmail.com"


@pytest.mark.django_db
def test_add_address_line2(client, homer):
    homer.save()

    homer.address_line2 = "Apartment C"
    response = client.post(f"/employee/{homer.pk}/update", data=model_to_dict(homer))

    assert response.status_code == 302
    homer.refresh_from_db()
    assert homer.address_line2 == "Apartment C"
