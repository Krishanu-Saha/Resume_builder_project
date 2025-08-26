# personal_details/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import PersonalDetails
from .serializers import PersonalDetailsSerializer
from resume.models import Resume


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def personal_details_crud(request, resume_id):
    """
    A single CRUD endpoint for handling PersonalDetails
    linked to a Resume. 
    - GET: Retrieve details
    - POST: Create details (if not already created)
    - PUT: Update details
    - DELETE: Remove details
    """
    resume = get_object_or_404(Resume, id=resume_id)

    try:
        personal_details = PersonalDetails.objects.get(resume=resume)
    except PersonalDetails.DoesNotExist:
        personal_details = None

    if request.method == 'GET':
        if personal_details is None:
            return Response({"detail": "No personal details found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PersonalDetailsSerializer(personal_details)
        return Response(serializer.data)

    elif request.method == 'POST':
        if personal_details is not None:
            return Response({"detail": "Personal details already exist. Use PUT to update."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data["resume"] = resume.id
        serializer = PersonalDetailsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if personal_details is None:
            return Response({"detail": "No personal details found to update. Use POST first."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data["resume"] = resume.id
        serializer = PersonalDetailsSerializer(personal_details, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if personal_details is None:
            return Response({"detail": "No personal details found to delete."}, status=status.HTTP_404_NOT_FOUND)
        personal_details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
