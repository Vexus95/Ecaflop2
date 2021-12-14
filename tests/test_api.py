import dataclasses

import requests
import pytest
from faker import Faker

from conftest import new_fake_employee


class Client:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "http://127.0.0.1:5678/api/v1"

    def call(self, method, path, **kwargs):
        url = self.base_url + path
        res = self.session.request(method, url, **kwargs)
        assert res.ok
        return res.json()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def clean_db(client):
    client.call("delete", "/employees")


def test_delete_employees(client, saved_employee):
    response = client.call("delete", "/employees")
    deleted = response["deleted"]
    assert deleted >= 1


def put_employee(client, employee):
    response = client.call("put", "/employee", json=dataclasses.asdict(employee))
    return response["employee"]["id"]


@pytest.fixture
def saved_employee(client, fake_employee):
    id = put_employee(client, fake_employee)
    fake_employee.id = id
    return fake_employee


def test_create_employee(client, fake_employee):
    put_employee(client, fake_employee)


def test_get_employee(client, saved_employee):
    response = client.call("get", f"/employee/{saved_employee.id}")
    actual = response["employee"]
    assert actual["name"] == saved_employee.name
    assert actual["email"] == saved_employee.email


def test_list_employees(client, clean_db):
    alice = new_fake_employee()
    bob = new_fake_employee()
    put_employee(client, alice)
    put_employee(client, bob)

    returned_alice, returned_bob = client.call("get", f"/employees/")
    assert returned_alice["name"] == alice.name
    assert returned_bob["name"] == bob.name


def test_update_employee_name(client, saved_employee):
    body = dataclasses.asdict(saved_employee)
    faker = Faker()
    body["name"] = "New Name"
    client.call("put", f"/employee/{saved_employee.id}", json=body)

    response = client.call("get", f"/employee/{saved_employee.id}")
    actual = response["employee"]
    assert actual["name"] == "New Name"
