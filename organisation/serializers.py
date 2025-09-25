from rest_framework import serializers
from .models import Organisation

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = [
            'id',
            'name',
            'position',
            'start_date',
            'end_date',
            'location',
            'description',
            'resume',  # still returned in GETs
        ]
        read_only_fields = ['resume']  # will be set in views
