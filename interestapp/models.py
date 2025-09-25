from django.db import models
from resume.models import Resume


class Interest(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="interests"
    )
    name = models.CharField(max_length=255)  # e.g., "Photography", "Traveling"
    additional_info = models.TextField(blank=True, null=True)  # e.g., "Nature and wildlife"
    link = models.URLField(blank=True, null=True)  # Optional reference or portfolio link

    class Meta:
        ordering = ["name"]  # ✅ Always sort interests alphabetically

    def __str__(self):
        return f"{self.name} ({self.resume.title})"
