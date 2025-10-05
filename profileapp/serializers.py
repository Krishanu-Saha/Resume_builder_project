from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    user = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = Profile
        fields = "__all__"
