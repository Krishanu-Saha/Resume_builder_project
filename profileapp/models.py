# profileapp/models.py
from django.db import models
from django.conf import settings

class Profile(models.Model):
    FRESHER = 'fresher'
    EXPERIENCED = 'experienced'

    WORK_STATUS_CHOICES = [
        (FRESHER, 'Fresher'),
        (EXPERIENCED, 'Experienced'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    work_status = models.CharField(max_length=20, choices=WORK_STATUS_CHOICES, blank=True, null=True)
    total_experience_years = models.PositiveIntegerField(blank=True, null=True)
    total_experience_months = models.PositiveIntegerField(blank=True, null=True)
    current_salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - Profile"
