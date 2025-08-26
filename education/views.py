# education/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Education
from .serializers import EducationSerializer
from resume.models import Resume


@api_view(['GET', 'POST'])
def education_list_create(request, resume_id):
    # Ensure the resume exists
    resume = get_object_or_404(Resume, id=resume_id)

    if request.method == 'GET':
        educations = Education.objects.filter(resume=resume)
        serializer = EducationSerializer(educations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data["resume"] = resume.id   # link to given resume
        serializer = EducationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def education_detail(request, resume_id, pk):
    # Ensure education belongs to the given resume
    education = get_object_or_404(Education, pk=pk, resume_id=resume_id)

    if request.method == 'GET':
        serializer = EducationSerializer(education)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data.copy()
        data["resume"] = education.resume.id  # prevent resume change
        serializer = EducationSerializer(education, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
