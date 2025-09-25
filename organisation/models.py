from django.db import models
from resume.models import Resume
from django.utils import timezone

class Organisation(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="organisations"
    )
    name = models.CharField(max_length=255)  # Organisation name
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # null => ongoing
    location = models.CharField(max_length=255)  # City, Country
    description = models.TextField(blank=True)

      # track updates

    def __str__(self):
        return f"{self.name} - {self.position}"
