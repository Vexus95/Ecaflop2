from django.db import models


class BasicInfo(models.Model):
    name = models.CharField(null=False, max_length=100)
    email = models.EmailField(null=False)
    address_line1 = models.CharField(null=False, max_length=100)
    address_line2 = models.CharField(null=False, max_length=100)
    city = models.CharField(null=False, max_length=100)
    zip_code = models.CharField(null=False, max_length=100)

    def __str__(self):
        return f"{self.name} - {self.email}"


class Contract(models.Model):
    hiring_date = models.DateField(null=False)
    job_title = models.CharField(null=False, max_length=100)

    def __str__(self):
        return f"{self.job_title} - hired on {self.hiring_date}"


class Team(models.Model):
    name = models.CharField(null=False, max_length=100)

    def __str__(self):
        return f"{self.name} # {self.id}"


class Employee(models.Model):
    basic_info = models.OneToOneField(BasicInfo, null=False, on_delete=models.CASCADE)
    contract = models.OneToOneField(Contract, null=False, on_delete=models.CASCADE)
    manager = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    is_manager = models.BooleanField(default=False)
    # BUG on_delete = DO_NOTHING
    team = models.ForeignKey(Team, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        res = self.basic_info.name
        if self.is_manager:
            res += " (manager)"
        return res
