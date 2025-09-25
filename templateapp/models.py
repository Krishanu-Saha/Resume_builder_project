from django.db import models
from django.core.exceptions import ValidationError

def validate_html_file(value):
    if not value.name.endswith('.html'):
        raise ValidationError("Only .html files are allowed for resume templates.")

class ResumeTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    # Store preview images separately
    preview_image = models.ImageField(
        upload_to='template_previews/',  # ✅ avoids clash with URLs
        blank=True,
        null=True
    )

    # Store HTML files separately
    file = models.FileField(
        upload_to='template_files/',    # ✅ avoids clash with URLs
        validators=[validate_html_file]
    )

    is_active = models.BooleanField(default=True)  # soft disable option
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # track last update

    def __str__(self):
        return self.name
