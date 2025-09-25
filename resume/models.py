from django.db import models
from django.conf import settings  # Best practice: use settings.AUTH_USER_MODEL
from templateapp.models import ResumeTemplate
from django.utils import timezone

class Resume(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Links to your custom User model
        on_delete=models.CASCADE,
        related_name="resumes"     # Allows reverse lookup: user.resumes.all()
    )
    title = models.CharField(max_length=255)
    template = models.ForeignKey(
        ResumeTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
 

    def __str__(self):
        return f"{self.title} ({self.user.email})"

