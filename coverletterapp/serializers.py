from rest_framework import serializers
from .models import CoverLetter


class CoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetter
        fields = [
            "id",
            "user",
            "title",
            "template",
            "recipient_name",
            "recipient_position",
            "company_name",
            "body",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
