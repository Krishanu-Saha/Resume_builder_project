from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Certificate
from .serializers import CertificateSerializer
from resume.models import Resume


@api_view(['GET', 'POST'])
def certificate_list_create(request, resume_id):
    # Ensure the resume exists
    resume = get_object_or_404(Resume, id=resume_id)

    if request.method == 'GET':
        certificates = Certificate.objects.filter(resume=resume)
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data["resume"] = resume.id   # link to given resume
        serializer = CertificateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def certificate_detail(request, resume_id, pk):
    # Ensure certificate belongs to the given resume
    certificate = get_object_or_404(Certificate, pk=pk, resume_id=resume_id)

    if request.method == 'GET':
        serializer = CertificateSerializer(certificate)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data.copy()
        data["resume"] = certificate.resume.id  # prevent resume change
        serializer = CertificateSerializer(certificate, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        certificate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
