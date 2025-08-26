from django.db import models
from resume.models import Resume

class Skill(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Amateur', 'Amateur'),
        ('Competent', 'Competent'),
        ('Proficient', 'Proficient'),
        ('Expert', 'Expert'),
    ]

    resume = models.ForeignKey(Resume, related_name="skills", on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)
    info = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.skill} ({self.level})"


# Create your models here.
