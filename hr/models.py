from django.db import models
from django.urls import reverse


class Employee(models.Model):
    name = models.CharField(null=False, max_length=100)
    address_line1 = models.CharField(null=False, max_length=100)
    address_line2 = models.CharField(null=True, max_length=100)
    city = models.CharField(null=False, max_length=100)
    zip_code = models.CharField(null=False, max_length=100)
    email = models.EmailField(null=True)


"""
    def get_absolute_url(self):
        return reverse("hr:employee_detail", kwargs={"pk": self.pk})
        """
