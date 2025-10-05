from django.db import models
from django.core.exceptions import ValidationError

def validate_html_file(value):
    if not value.name.endswith('.html'):
        raise ValidationError("Only .html files are allowed for cover letter templates.")

class CoverLetterTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)

    # Preview image for UI
    preview_image = models.ImageField(
        upload_to='cover_letter_previews/',
        blank=True,
        null=True
    )

    # Actual HTML template file
    file = models.FileField(
        upload_to='cover_letter_files/',
        validators=[validate_html_file],
        blank=True,
        null=True
        
    )

    created_at = models.DateTimeField(auto_now_add=True)  # when added
    updated_at = models.DateTimeField(auto_now=True)      # last modified

    def __str__(self):
        return self.name

