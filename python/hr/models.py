from django.db import models


class Employee(models.Model):
    name = models.CharField(null=False, max_length=100)
    address_line1 = models.CharField(null=False, max_length=100)
    address_line2 = models.CharField(null=True, max_length=100, default="")
    city = models.CharField(null=False, max_length=100)
    zip_code = models.CharField(null=False, max_length=100)
    email = models.EmailField(null=True)

    def __str__(self):
        import json

        return json.dumps(self.to_json())

    def to_json(self):
        res = {
            "name": self.name,
            "email": self.email,
            "address_line1": self.address_line1,
            "address_line2": self.address_line2,
            "city": self.city,
            "zip_code": self.zip_code,
        }
        res["id"] = self.pk
        return res
