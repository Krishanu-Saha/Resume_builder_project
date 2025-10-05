from rest_framework import serializers
from .models import CoverLetterTemplate

class CoverLetterTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetterTemplate
        fields = [
            "id", "name", "preview_image", "file",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
