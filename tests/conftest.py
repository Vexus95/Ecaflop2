from dataclasses import dataclass
from typing import Optional
from faker import Faker
import pytest


@dataclass
class Employee:
    id: Optional[int]
    name: str
    email: str
    address_line1: str
    address_line2: str
    city: str
    zip_code: str


@pytest.fixture
def fake_employee():
    fake = Faker()
    name = fake.name()
    email = fake.email()
    address_line1, address_line2 = fake.address().split("\n")
    city = fake.city()
    zip_code = fake.zipcode()

    return Employee(
        id=None,
        name=name,
        email=email,
        address_line1=address_line1,
        address_line2=address_line2,
        city=city,
        zip_code=zip_code,
    )
