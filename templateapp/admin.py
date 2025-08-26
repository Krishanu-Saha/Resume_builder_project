from django.contrib import admin
from .models import ResumeTemplate

@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "file", "preview_image", "created_at")
    search_fields = ("name", "description")


# Register your models here.
