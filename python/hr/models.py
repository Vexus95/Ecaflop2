from django.db import models


class Employee(models.Model):
    name = models.CharField(null=False, max_length=100)
    address_line1 = models.CharField(null=False, max_length=100)
    address_line2 = models.CharField(null=True, max_length=100, default="")
    city = models.CharField(null=False, max_length=100)
    zip_code = models.CharField(null=False, max_length=100)
    email = models.EmailField(null=True)

    __json_fields = [
        "name",
        "address_line1",
        "address_line2",
        "city",
        "zip_code",
        "email",
    ]

    def update(self, data):
        name = data.get("name")
        if name:
            self.name = name
        address_line1 = data.get("address_line1")
        if address_line1:
            self.address_line1 = address_line1
        address_line2 = data.get("address_line2")
        if address_line2:
            self.address_line2 = address_line2
        city = data.get("city")
        if city:
            self.city = city
        zip_code = data.get("zip_code")
        if zip_code:
            self.zip_code = zip_code
        email = data.get("email")
        if email:
            self.email = email

    def to_json(self):
        res = {
            "name": self.name,
            "address_line1": self.address_line1,
            "address_line2": self.address_line2,
            "city": self.city,
            "zip_code": self.zip_code,
            "email": self.email,
        }
        res["id"] = self.pk
        return res
