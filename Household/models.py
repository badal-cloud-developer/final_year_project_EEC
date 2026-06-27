from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class WasteReport(models.Model):
    WASTE_TYPE_CHOICES=[
        ('organic','Organic'),
        ('nonorganic','Non-Organic'),
        ('ewaste','E-Easte')
    ]
    STATUS_CHOICES=[
        ('pending','Pending'),
         ('accepted','Accepted'),
        ('completed','Completed'),
       
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    waste_type = models.CharField(max_length=20, choices=WASTE_TYPE_CHOICES)
    items = models.JSONField()  
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    report_time = models.DateTimeField(default=timezone.now)
    points = models.IntegerField(default=0) 
    collected_by = models.CharField(blank=True,null=True, default=None,max_length=50)  
    collected_at = models.DateTimeField(null=True, blank=True, default=None)


    def __str__(self):
        return f"{self.user.username} - {self.waste_type} ({self.status})"
    

class IllegalDumping(models.Model):
    STATUS_PENDING      = "pending"
    STATUS_PROCESSING   = "processing"
    STATUS_VALIDATED    = "validated"
    STATUS_INVALID      = "invalid"

    STATUS_CHOICES = [
        (STATUS_PENDING,    "Pending"),
        (STATUS_PROCESSING, "Under processing"),
        (STATUS_VALIDATED,  "Validated"),
        (STATUS_INVALID,    "Invalid"),
    ]

    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description  = models.CharField(max_length=500)
    Area         = models.CharField(max_length=100)
    picture      = models.ImageField(upload_to="media/")
    status       = models.CharField(max_length=20,
                                    choices=STATUS_CHOICES,
                                    default=STATUS_PENDING,
                                    blank=True)
    report_time  = models.DateTimeField(default=timezone.now)
    points       = models.IntegerField(default=0)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/')

    def __str__(self):
        return self.user.username
    
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report = models.ForeignKey('IllegalDumping', on_delete=models.CASCADE, related_name='likes')
    liked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending', blank=True) 


    class Meta:
        unique_together = ('user', 'report')  # one like per user per report

    def __str__(self):
        return f"{self.user.username} liked report {self.report.id}"
