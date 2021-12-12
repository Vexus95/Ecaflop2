import requests
import pytest


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


def test_delete_employees(client):
    response = client.call("delete", "/employees")
    deleted = response["deleted"]
    assert deleted >= 0


@pytest.fixture
def clean_db(client):
    client.call("delete", "/employees")


def test_create_employee(client, clean_db):
    response = client.call("put", "/employee", json={"name": "john"})
    actual = response["employee"]
    assert actual["name"] == "john"


def test_get_employee(client, clean_db):
    response = client.call("put", "/employee", json={"name": "john"})
    id = response["employee"]["id"]

    response = client.call("get", f"/employee/{id}")
    actual = response["employee"]
    assert actual["name"] == "john"


def test_update_employe_name(client, clean_db):
    response = client.call("put", "/employee", json={"name": "john"})
    id = response["employee"]["id"]

    client.call("put", f"/employee/{id}", json={"name": "jane"})

    response = client.call("get", f"/employee/{id}")
    actual = response["employee"]
    assert actual["name"] == "jane"
