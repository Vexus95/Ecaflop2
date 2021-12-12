import pytest
from dataclasses import dataclass
from typing import Optional

from faker import Faker

BASE_URL = "http://127.0.0.1:8080"


@dataclass
class Employee:
    id: Optional[int]
    name: str
    email: str
    address_line1: str
    address_line2: str
    city: str
    zip_code: str


def on_console_message(message):
    if message.type == "error":
        print(message.text)


@pytest.fixture(autouse=True)
def fail_when_console_errors(page):
    page.on("console", on_console_message)


@pytest.fixture(autouse=True)
def set_timeout(page):
    page.set_default_timeout(2000)


def test_index(page):
    page.goto(BASE_URL)
    assert page.is_visible("text=List employees")
    assert page.is_visible("text=Reset database")


def test_reset_database(page):
    page.goto(BASE_URL)
    page.click("text=Reset database")
    page.click("text=Proceed")
    assert page.text_content("text=Deleted")


@pytest.fixture
def clean_db(page):
    page.goto(BASE_URL + "/reset-db")
    page.click("text=Proceed")


@pytest.fixture
def employee(page):
    page.goto(BASE_URL + "/reset-db")
    page.click("text=Proceed")
    page.goto(BASE_URL)
    page.click("text=List employees")
    page.click("text=Add new employee")

    fake = Faker()
    name = fake.name()
    email = fake.email()
    address_line1, address_line2 = fake.address().split("\n")
    city = fake.city()
    zip_code = fake.zipcode()

    page.fill('input[name="name"]', name)
    page.fill('input[name="email"]', email)
    page.fill('input[name="address_line1"]', address_line1)
    page.fill('input[name="address_line2"]', address_line2)
    page.fill('input[name="city"]', city)
    page.fill('input[name="zip_code"]', zip_code)

    page.click('button[type="submit"]')

    return Employee(
        id=None,
        name=name,
        email=email,
        address_line1=address_line1,
        address_line2=address_line2,
        city=city,
        zip_code=zip_code,
    )


def find_employee_row(page, employee_name):
    page.wait_for_selector("text=ID")

    tables_rows = page.locator("tr")
    matching_row = None
    for i in range(0, tables_rows.count()):
        row = tables_rows.nth(i)
        if employee_name in row.inner_html():
            return row

    pytest.fail(f"{employee.name} not found in the list")


def test_add_employee(clean_db, employee, page):
    find_employee_row(page, employee.name)
    assert page.text_content(f"text={employee.name}")
    assert page.text_content(f"text={employee.email}")


def test_edit_employee_name(clean_db, employee, page):
    row = find_employee_row(page, employee.name)

    link = row.locator("a")
    link.click()

    page.wait_for_selector("text=Edit Employee")
    fake = Faker()
    new_name = fake.name()
    page.fill('input[name="name"]', new_name)
    page.click('button[type="submit"]')

    page.goto(BASE_URL + "/employees")

    find_employee_row(page, new_name)
