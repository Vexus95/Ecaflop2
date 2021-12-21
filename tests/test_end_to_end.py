import pytest
from faker import Faker

BASE_URL = "http://127.0.0.1:8080"


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
def saved_employee(page, fake_employee):
    page.goto(BASE_URL + "/reset-db")
    page.click("text=Proceed")
    page.goto(BASE_URL)
    page.click("text=List employees")
    page.click("text=Add new employee")

    page.fill('input[name="name"]', fake_employee.name)
    page.fill('input[name="email"]', fake_employee.email)
    page.fill('input[name="address_line1"]', fake_employee.address_line1)
    page.fill('input[name="address_line2"]', fake_employee.address_line2)
    page.fill('input[name="city"]', fake_employee.city)
    page.fill('input[name="zip_code"]', fake_employee.zip_code)

    page.click('button[type="submit"]')
    return fake_employee


def find_employee_row(page, employee_name):
    page.wait_for_selector("text=ID")

    tables_rows = page.locator("tr")
    for i in range(0, tables_rows.count()):
        row = tables_rows.nth(i)
        if employee_name in row.inner_html():
            return row

    pytest.fail(f"{employee_name} not found in the list")


def test_add_employee(clean_db, saved_employee, page):
    find_employee_row(page, saved_employee.name)
    assert page.text_content(f"text={saved_employee.name}")
    assert page.text_content(f"text={saved_employee.email}")


def test_edit_employee_name(clean_db, saved_employee, page):
    row = find_employee_row(page, saved_employee.name)

    link = row.locator("a")
    link.click()

    page.wait_for_selector("text=Edit Employee")
    fake = Faker()
    new_name = fake.name()
    page.fill('input[name="name"]', new_name)
    page.click('button[type="submit"]')

    page.goto(BASE_URL + "/employees")

    find_employee_row(page, new_name)
