from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'resume', 'name', 'description', 'start_date', 'end_date']
        read_only_fields = ['id','resume']

    def validate_resume(self, value):
        request = self.context.get('request')
        if request and value.user != request.user:
            raise serializers.ValidationError("You can only add projects to your own resumes.")
        return value
