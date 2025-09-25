from rest_framework import serializers
from .models import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'resume', 'name', 'additional_info', 'link']
        read_only_fields = ['id', 'resume']
