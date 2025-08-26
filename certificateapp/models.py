from django.db import models
from resume.models import Resume  # Assuming you have a Resume model

class Certificate(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="certificates")
    name = models.CharField(max_length=255)
    additional_info = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


# Create your models here.
