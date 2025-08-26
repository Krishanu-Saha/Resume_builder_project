# Create your models here.
from django.db import models
from templateapp.models import ResumeTemplate

class Resume(models.Model):
    title = models.CharField(max_length=255)
    template = models.ForeignKey(ResumeTemplate, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

