from rest_framework import serializers
from .models import Organisation

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = [
            'id',
            'resume',  # show which resume this belongs to
            'name',
            'position',
            'start_date',
            'end_date',
            'location',
            'description'
        ]
        read_only_fields = ['resume']  # set from URL
