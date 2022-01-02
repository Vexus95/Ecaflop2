import dataclasses

import pytest
from faker import Faker

from tests.conftest import new_fake_employee


@pytest.fixture(autouse=True)
def set_timeout(page):
    page.set_default_timeout(2000)


def test_index(page):
    page.goto("/")
    assert page.is_visible("text=List employees")
    assert page.is_visible("text=Reset database")


def save_employee(page, fake_employee):
    page.goto("/add_employee")

    as_dict = dataclasses.asdict(fake_employee)
    for (key, value) in as_dict.items():
        page.fill(f'input[name="{key}"]', value)

    page.click('button[type="submit"]')
    return fake_employee


@pytest.fixture
def saved_employee(page, fake_employee):
    return save_employee(page, fake_employee)


def find_employee_row(page, employee_name):
    tables_rows = page.locator("tr")
    for i in range(0, tables_rows.count()):
        row = tables_rows.nth(i)
        if employee_name in row.inner_html():
            return row

    pytest.fail(f"employee {employee_name} not found in the list")


def find_team_row(page, team_name):
    tables_rows = page.locator("tr")
    for i in range(0, tables_rows.count()):
        row = tables_rows.nth(i)
        if team_name in row.inner_html():
            return row

    pytest.fail(f"team {team_name} not found in the list")


def test_add_employee(saved_employee, page):
    find_employee_row(page, saved_employee.name)
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
def test_edit_employee_basic_info(saved_employee, page, key):
    row = find_employee_row(page, saved_employee.name)
    edit_button = row.locator("text=Edit")
    edit_url = edit_button.get_attribute("href")
    edit_button.click()

    link = page.locator("text='Update basic info'")
    link.click()

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
def test_edit_employee_address(saved_employee, page, key):
    row = find_employee_row(page, saved_employee.name)
    edit_button = row.locator("text=Edit")
    edit_button.get_attribute("href")
    edit_button.click()

    link = page.locator("text='Update address'")
    edit_address_url = link.get_attribute("href")
    link.click()

    faker = Faker()
    new_value = faker.pystr()
    page.fill(f'input[name="{key}"]', new_value)
    page.click('button[type="submit"]')

    page.goto(edit_address_url)

    input_element = page.locator(f'input[name="{key}"]')
    assert input_element.input_value() == new_value


def test_edit_employee_job_title(saved_employee, page):
    row = find_employee_row(page, saved_employee.name)
    edit_button = row.locator("text=Edit")
    edit_button.get_attribute("href")
    edit_button.click()

    link = page.locator("text='Update legal info'")
    edit_legal_url = link.get_attribute("href")
    link.click()

    faker = Faker()
    new_value = faker.pystr()
    page.fill('input[name="job_title"]', new_value)
    page.click('button[type="submit"]')

    page.goto(edit_legal_url)

    input_element = page.locator('input[name="job_title"]')
    assert input_element.input_value() == new_value


def create_team(page):
    page.goto("/add_team")
    name = page.locator('input[name="name"]')
    fake = Faker()
    team_name = fake.pystr()
    name.fill(team_name)
    page.click("text='Add'")

    return team_name


def test_create_team(page):
    team_name = create_team(page)
    assert page.is_visible(f"td:has-text('{team_name}')")


def test_add_member_to_team(page):
    team_name = create_team(page)

    employee = new_fake_employee()
    employee = save_employee(page, employee)
    row = find_employee_row(page, employee.name)
    edit_button = row.locator("text=Edit")
    edit_button.click()

    page.click("text='Add to team'")

    select = page.locator("select[name='team_id']")
    select.select_option(label=team_name)
    page.click("text='Add'")

    row = find_team_row(page, team_name)
    link = row.locator("text='View members'")
    url = link.get_attribute("href")
    page.goto(url)
    assert page.is_visible(f"ul:has-text('{employee.name}')")


def test_promote_manager(page):
    employee = new_fake_employee()
    employee = save_employee(page, employee)
    row = find_employee_row(page, employee.name)
    edit_button = row.locator("text=Edit")
    edit_button.click()

    page.click("text='Promote as manager'")
    page.click("text='Proceed'")

    row = find_employee_row(page, employee.name)
    cell = row.locator("td > strong")
    assert cell.is_visible()
    assert cell.inner_text() == "yes"


def test_delete_single_employee(page):
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


def test_delete_team(page):
    team_one = create_team(page)
    team_two = create_team(page)

    row = find_team_row(page, team_two)
    link = row.locator("text='Delete'")
    url = link.get_attribute("href")
    page.goto(url)

    page.click("text='Proceed'")

    assert page.is_visible(f"td:has-text('{team_one}')")
    assert not page.is_visible(f"td:has-text('{team_two}')")
