from rest_framework import serializers
from .models import Skill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'resume', 'skill', 'info', 'level']
        read_only_fields = ['id','resume']

    # Optionally, validate that the resume belongs to the logged-in user
    def validate_resume(self, value):
        request = self.context.get('request')
        if request and value.user != request.user:
            raise serializers.ValidationError("You can only add skills to your own resumes.")
        return value
