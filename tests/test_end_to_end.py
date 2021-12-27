import pytest

from faker import Faker
from conftest import new_fake_employee


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
    page.goto("/")
    assert page.is_visible("text=List employees")
    assert page.is_visible("text=Reset database")


def test_reset_database(page):
    page.goto("/")
    page.click("text=Reset database")
    page.click("text=Proceed")
    assert page.text_content("text=Deleted")


@pytest.fixture
def clean_db(page):
    page.goto("/reset-db")
    page.click("text=Proceed")


def save_employee(page, fake_employee):
    page.goto("/")
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
    page.wait_for_selector("h3")

    tables_rows = page.locator("tr")
    for i in range(0, tables_rows.count()):
        row = tables_rows.nth(i)
        if employee_name in row.inner_html():
            return row

    pytest.fail(f"{employee_name} not found in the list")


def test_add_employee(clean_db, saved_employee, page):
    row = find_employee_row(page, saved_employee.name)
    actual_content = page.content()
    assert saved_employee.name in actual_content
    assert saved_employee.email in actual_content


@pytest.mark.parametrize(
    "key",
    [
        "name",
        "email",
    ],
)
def test_edit_employee_basic_info(clean_db, saved_employee, page, key):
    row = find_employee_row(page, saved_employee.name)
    edit_button = row.locator("text=Edit")
    edit_url = edit_button.get_attribute("href")
    edit_button.click()

    link = page.locator("text='Update basic info'")
    link.click()

    page.wait_for_selector("text=Basic Info")
    faker = Faker()
    new_value = faker.pystr()
    page.fill(f'input[name="{key}"]', new_value)
    page.click('button[type="submit"]')

    # Making sure we make a round-trip through the db
    page.goto(edit_url)

    assert new_value in page.content()


@pytest.mark.parametrize(
    "key",
    [
        "address_line1",
        "address_line2",
        "city",
        "zip_code",
    ],
)
def test_edit_employee_address(clean_db, saved_employee, page, key):
    row = find_employee_row(page, saved_employee.name)
    edit_button = row.locator("text=Edit")
    edit_button.get_attribute("href")
    edit_button.click()

    link = page.locator("text='Update address'")
    edit_address_url = link.get_attribute("href")
    link.click()

    page.wait_for_selector("text=Address")
    faker = Faker()
    new_value = faker.pystr()
    page.fill(f'input[name="{key}"]', new_value)
    page.click('button[type="submit"]')

    # Making sure we make a round-trip through the db
    page.goto("/")

    page.goto(edit_address_url)
    input_element = page.locator(f'input[name="{key}"]')
    assert input_element.input_value() == new_value


def test_delete_single_employee(clean_db, page):
    alice = new_fake_employee()
    bob = new_fake_employee()
    save_employee(page, alice)
    save_employee(page, bob)

    row = find_employee_row(page, alice.name)
    delete_button = row.locator("text=Delete")
    delete_button.click()

    page.click("text=Proceed")

    page.goto("/employees")

    assert not page.is_visible(f"text={alice.name}")
    assert page.is_visible(f"text={bob.name}")
