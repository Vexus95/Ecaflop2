from django.db import models


class Employee(models.Model):
    name = models.CharField(null=False, max_length=100)
    address_line1 = models.CharField(null=False, max_length=100)
    address_line2 = models.CharField(null=False, max_length=100)
    city = models.CharField(null=False, max_length=100)
    zip_code = models.CharField(null=False, max_length=100)
    email = models.EmailField(null=False)
    job_title = models.CharField(null=False, max_length=100)
    hiring_date = models.DateField(null=False)

    def __str__(self):
        return f"{self.name} - {self.email}"
