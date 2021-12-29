from dataclasses import dataclass

import pytest
from faker import Faker


@dataclass
class Employee:
    name: str
    email: str
    address_line1: str
    address_line2: str
    city: str
    zip_code: str
    hiring_date: str
    job_title: str


def new_fake_employee():
    fake = Faker()
    name = fake.name()
    email = fake.email()
    address_line1, address_line2 = fake.address().split("\n")
    city = fake.city()
    zip_code = fake.zipcode()
    job_title = fake.job()
    hiring_date = fake.date_this_year().strftime("%Y-%m-%d")

    return Employee(
        name=name,
        email=email,
        address_line1=address_line1,
        address_line2=address_line2,
        city=city,
        zip_code=zip_code,
        job_title=job_title,
        hiring_date=hiring_date,
    )


@pytest.fixture
def fake_employee():
    return new_fake_employee()
