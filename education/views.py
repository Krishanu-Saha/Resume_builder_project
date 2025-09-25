# education/views.py
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Education
from .serializers import EducationSerializer
from accountapp.authentication import JWTAuthentication
from accountapp.permissions import IsResumeOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def education_list_create(request, resume_id):
    """
    List all education entries for a resume (owned by the user) or create a new education.
    """
    from resume.models import Resume
    resume = get_object_or_404(Resume, id=resume_id)

    # enforce ownership
    if resume.user != request.user:
        return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        educations = resume.educations.all()
        serializer = EducationSerializer(educations, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = EducationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(resume=resume)  # enforce resume assignment
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsResumeOwnerOrAdmin])
def education_detail(request, resume_id, pk):
    education = get_object_or_404(Education, pk=pk, resume_id=resume_id)

    # Ownership check
    if education.resume.user != request.user:
        return Response({"detail": "Not authorized"}, status=403)

    if request.method == 'GET':
        serializer = EducationSerializer(education)
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        serializer = EducationSerializer(
            education,
            data=request.data,
            partial=(request.method == 'PATCH'),
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(resume=education.resume)  # prevent changing resume
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
