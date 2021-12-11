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
        for key in self.__json_fields:
            value = data.get(key)
            if value:
                setattr(self, key, value)

    def to_json(self):
        res = {k: getattr(self, k) for k in self.__json_fields}
        res["id"] = self.pk
        return res
