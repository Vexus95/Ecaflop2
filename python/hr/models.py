from django.db import models


class Employee(models.Model):
    name = models.CharField(null=False, max_length=100)
    address_line1 = models.CharField(null=False, max_length=100)
    address_line2 = models.CharField(null=True, max_length=100, default="")
    city = models.CharField(null=False, max_length=100)
    zip_code = models.CharField(null=False, max_length=100)
    email = models.EmailField(null=True)
