from rest_framework import serializers
from .models import PersonalDetails

class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        fields = '__all__'
        extra_kwargs = {
            "full_name": {"required": False, "allow_null": True},
            "professional_title": {"required": False, "allow_null": True},
            "email": {"required": False, "allow_null": True},
            "phone": {"required": False, "allow_null": True},
            "location": {"required": False, "allow_null": True},
            "linkedin": {"required": False, "allow_null": True},
            "website": {"required": False, "allow_null": True},
            "nationality": {"required": False, "allow_null": True},
            "gender": {"required": False, "allow_null": True},
            "date_of_birth": {"required": False, "allow_null": True},
            "profile_image": {"required": False, "allow_null": True},  # New field
        }
        read_only_fields = ['id', 'resume']

    def validate_resume(self, value):
        request = self.context.get('request')
        if request and value.user != request.user:
            raise serializers.ValidationError("You can only manage personal details for your own resume.")
        return value
