from rest_framework import serializers
from .models import Interest

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'resume', 'name', 'additional_info', 'link']
