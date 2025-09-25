from django.db import models
from resume.models import Resume
from django.utils import timezone

class PersonalDetails(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Prefer not to say', 'Prefer not to say'),
    ]

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
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # New profile image field
    profile_image = models.ImageField(
        upload_to='personal_images/',  # Folder inside MEDIA_ROOT
        blank=True,
        null=True,
        default=None
    )

    def __str__(self):
        title = self.resume.title if self.resume.title else "Unnamed Resume"
        return f"Personal Details for {title}"
