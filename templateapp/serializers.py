from rest_framework import serializers
from .models import ResumeTemplate


class ResumeTemplateSerializer(serializers.ModelSerializer):
    preview_image = serializers.ImageField(use_url=True)  # ✅ absolute URL
    file = serializers.FileField(use_url=True)            # ✅ absolute URL

    class Meta:
        model = ResumeTemplate
        fields = ['id', 'name', 'description', 'preview_image', 'file']

