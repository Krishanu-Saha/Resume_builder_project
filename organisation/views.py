# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Organisation
from .serializers import OrganisationSerializer
from resume.models import Resume


@api_view(['GET', 'POST'])
def organisation_list_create(request, resume_id):
    # Ensure the resume exists
    resume = get_object_or_404(Resume, pk=resume_id)

    if request.method == 'GET':
        organisations = Organisation.objects.filter(resume=resume)
        serializer = OrganisationSerializer(organisations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(resume=resume)  # ✅ attach resume here
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def organisation_detail(request, resume_id, pk):
    # Ensure organisation exists under that resume
    organisation = get_object_or_404(Organisation, pk=pk, resume_id=resume_id)

    if request.method == 'GET':
        serializer = OrganisationSerializer(organisation)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrganisationSerializer(
            organisation,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save(resume=organisation.resume)  # ✅ prevent resume change
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        organisation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
