from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('household', 'Household'),
        ('organization', 'Organization'),
        ('metro', 'Metro'),
        ('driver', 'Driver'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)



class Household(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    house_no = models.CharField(max_length=20)
    municipal = models.CharField(max_length=100)
    ward_no = models.IntegerField()

    def __str__(self):
        return f"Household: {self.user.username}"


class Organization(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=100)
    ward_no = models.IntegerField()
    waste_type = models.CharField(max_length=50)

    def __str__(self):
        return f"Organization: {self.user.username}"


class Metro(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    metro_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Metro: {self.user.username}"


