from django.db import models
from resume.models import Resume

class Course(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="courses")
    title = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.institution}"


# Create your models here.
