from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Interest
from .serializers import InterestSerializer
from resume.models import Resume


@api_view(['GET', 'POST'])
def interest_list_create(request, resume_id):
    # Ensure the resume exists
    resume = get_object_or_404(Resume, id=resume_id)

    if request.method == 'GET':
        interests = Interest.objects.filter(resume=resume)
        serializer = InterestSerializer(interests, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data["resume"] = resume.id   # link to given resume
        serializer = InterestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def interest_detail(request, resume_id, pk):
    # Ensure interest belongs to the given resume
    interest = get_object_or_404(Interest, pk=pk, resume_id=resume_id)

    if request.method == 'GET':
        serializer = InterestSerializer(interest)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data.copy()
        data["resume"] = interest.resume.id  # prevent resume change
        serializer = InterestSerializer(interest, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        interest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
