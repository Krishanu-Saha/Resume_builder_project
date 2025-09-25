# interestapp/serializers.py
from rest_framework import serializers
from .models import Interest


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = [
            "id",'resume',       # parent resume
            "name",
            "additional_info",
            "link",
        ]
        read_only_fields = ['id','resume']  # ✅ resume is set from URL, not user input
