from django.db import models
from resume.models import Resume

class Organisation(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="organisations"
    )
    name = models.CharField(max_length=255)  # Organisation name
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255)  # City, Country
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.position}"

# Create your models here.
