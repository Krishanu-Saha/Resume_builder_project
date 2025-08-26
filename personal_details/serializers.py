from rest_framework import serializers
from .models import PersonalDetails

class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        fields = '__all__'
        extra_kwargs = {
            "photo": {"required": False, "allow_null": True},  # ✅ optional
            "linkedin": {"required": False, "allow_null": True},
            "website": {"required": False, "allow_null": True},
            "nationality": {"required": False, "allow_null": True},
            "gender": {"required": False, "allow_null": True},
            "date_of_birth": {"required": False, "allow_null": True},
        }
