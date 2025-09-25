from rest_framework import serializers 
from .models import Resume
from personal_details.serializers import PersonalDetailsSerializer
from organisation.serializers import OrganisationSerializer
from project.serializers import ProjectSerializer
from education.serializers import EducationSerializer
from templateapp.serializers import ResumeTemplateSerializer 
from skillapp.serializers import SkillSerializer
from templateapp.models import ResumeTemplate
from certificateapp.serializers import CertificateSerializer
from courseapp.serializers import CourseSerializer
from interestapp.serializers import InterestSerializer


class ResumeSerializer(serializers.ModelSerializer):
    personal_details = PersonalDetailsSerializer(read_only=True)
    organisations = OrganisationSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    certificates = CertificateSerializer(many=True, read_only=True)
    courses = CourseSerializer(many=True, read_only=True)
    interests = InterestSerializer(many=True, read_only=True)

    # Read-only nested template serializer
    template = ResumeTemplateSerializer(read_only=True)
    # Write-only field to accept template_id
    template_id = serializers.PrimaryKeyRelatedField(
        queryset=ResumeTemplate.objects.all(),
        source="template",
        write_only=True
    )

    # Show user email (read-only)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Resume
        fields = [
            'id', 'title',
            'user',                     # ✅ added user field
            'template', 'template_id',  # ✅ include both
            'personal_details', 'organisations', 'projects',
            'educations', 'skills', 'certificates',
            'courses', 'interests'
        ]

    def create(self, validated_data):
        """
        Ensure the logged-in user is automatically set as the resume owner.
        """
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user
        return super().create(validated_data)
