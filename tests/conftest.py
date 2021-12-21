from dataclasses import dataclass
from typing import Optional

import pytest
from faker import Faker


@dataclass
class Employee:
    id: Optional[int]
    name: str
    email: str
    address_line1: str
    address_line2: str
    city: str
    zip_code: str

    def to_json(self, with_id=True):
        res = {
            "name": self.name,
            "email": self.email,
            "address_line1": self.address_line1,
            "address_line2": self.address_line2,
            "city": self.city,
            "zip_code": self.zip_code,
        }
        if with_id:
            res["id"] = self.id
        return res


def new_fake_employee():
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


@pytest.fixture
def fake_employee():
    return new_fake_employee()
