from django.db import models
from resume.models import Resume

class PersonalDetails(models.Model):
    resume = models.OneToOneField(
        Resume,
        on_delete=models.CASCADE,
        related_name="personal_details"
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    professional_title = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    linkedin = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Personal Details for {self.resume.title}"
