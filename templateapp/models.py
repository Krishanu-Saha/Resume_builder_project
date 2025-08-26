from django.db import models

class ResumeTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    preview_image = models.ImageField(upload_to='templates/previews/', blank=True, null=True)
    file = models.FileField(upload_to='templates/html/')  # stores .html template file
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Create your models here.
