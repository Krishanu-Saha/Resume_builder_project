from django.db import models
from django.conf import settings  # ✅ use AUTH_USER_MODEL
from cltemplateapp.models import CoverLetterTemplate # import from your template app
from django.utils import timezone


class CoverLetter(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cover_letters"
    )
    title = models.CharField(max_length=255)  # e.g., "Google SWE Cover Letter"

    template = models.ForeignKey(
        CoverLetterTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Extra fields specific to cover letters
    recipient_name = models.CharField(max_length=255, blank=True, null=True)   # "Hiring Manager"
    recipient_position = models.CharField(max_length=255, blank=True, null=True)  # "HR Manager"
    company_name = models.CharField(max_length=255, blank=True, null=True)     # "Google"
    body = models.TextField()  # actual cover letter content

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.email}"
