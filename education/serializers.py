# education/serializers.py
from rest_framework import serializers
from .models import Education

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "id",
            "resume",       # FK reference
            "degree",
            "school",
            "start_date",
            "end_date",
            "location",
            "description",
        ]
        read_only_fields = ["resume"]  # ✅ set automatically from URL
