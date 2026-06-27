from django.db import models

class Vehicle(models.Model):
    AVAILABILITY_CHOICES = (
        (1, 'Available'),
        (0, 'Not Available'),
    )

    bus_no = models.CharField(max_length=20)
    ward_no = models.IntegerField()
    location = models.CharField(max_length=100)
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=15)
    availability = models.IntegerField(choices=AVAILABILITY_CHOICES, default=1)

    def __str__(self):
        return self.bus_no