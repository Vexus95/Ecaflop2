import pytest

from hr.models import Employee


@pytest.fixture
def homer():
    return Employee(
        name="Homer Simpson",
        email="homer@aol.com",
        city="Springfield",
        zip_code="12345",
        address_line1="1623 Main Street",
        address_line2="",
    )
