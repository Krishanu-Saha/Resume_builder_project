from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id', 'resume', 'title', 'institution',
            'start_date', 'end_date', 'location',
            'description', 'link'
        ]
