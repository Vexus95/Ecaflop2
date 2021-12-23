import pytest

from conftest import new_fake_employee

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


def save_employee(page, fake_employee):
    page.goto(BASE_URL)
    page.click("text=List employees")
    page.click("text=Add new employee")

    for (key, value) in fake_employee.to_json(with_id=False).items():
        page.fill(f'input[name="{key}"]', value)

    page.click('button[type="submit"]')
    return fake_employee


@pytest.fixture
def saved_employee(page, fake_employee):
    return save_employee(page, fake_employee)


def find_employee_row(page, employee_name):
    page.wait_for_selector("text=ID")

    tables_rows = page.locator("tr")
    for i in range(0, tables_rows.count()):
        row = tables_rows.nth(i)
        if employee_name in row.inner_html():
            return row

    pytest.fail(f"{employee_name} not found in the list")


def test_add_employee(clean_db, saved_employee, page):
    row = find_employee_row(page, saved_employee.name)
    link = row.locator("a")
    link.click()

    for (key, value) in saved_employee.to_json(with_id=False).items():
        input_element = page.locator(f'input[name="{key}"]')
        assert input_element.input_value() == value


@pytest.mark.parametrize(
    "key",
    [
        "name",
        "email",
        "address_line1",
        "address_line2",
        "city",
        "zip_code",
    ],
)
def test_edit_employee(clean_db, saved_employee, page, key):
    row = find_employee_row(page, saved_employee.name)
    link = row.locator("a")
    url = link.get_attribute("href")
    page.goto(BASE_URL + url)

    page.wait_for_selector("text=Edit Employee")
    page.fill(f'input[name="{key}"]', "new value")
    page.click('button[type="submit"]')

    # Making sure we make a round-trip through the db
    page.goto(BASE_URL + "/employees")

    page.goto(BASE_URL + url)
    page.wait_for_selector("text=Edit Employee")
    input_element = page.locator(f'input[name="{key}"]')
    assert input_element.input_value() == "new value"


def test_delete_single_employee(clean_db, page):
    alice = new_fake_employee()
    bob = new_fake_employee()
    save_employee(page, alice)
    save_employee(page, bob)

    row = find_employee_row(page, alice.name)
    delete_button = row.locator('text="Delete"')
    delete_button.click()

    # Making sure we make a round-trip through the db
    page.goto(BASE_URL + "/employees")

    assert not page.is_visible(f"text={alice.name}")
    assert page.is_visible(f"text={bob.name}")
