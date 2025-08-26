from django.db import models
from resume.models import Resume

class Project(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="projects"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


# Create your models here.
