# certificateapp/views.py
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Certificate
from .serializers import CertificateSerializer
from accountapp.authentication import JWTAuthentication
from accountapp.permissions import IsResumeOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated


@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def certificate_list_create(request, resume_id):
    """
    List all certificates for a resume (owned by user) or create a new one.
    """
    from resume.models import Resume
    resume = get_object_or_404(Resume, id=resume_id)

    # Ownership check
    if resume.user != request.user:
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        certificates = resume.certificates.all()
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = CertificateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(resume=resume)  # enforce link to resume
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsResumeOwnerOrAdmin])
def certificate_detail(request, resume_id, pk):
    """
    Retrieve, update, or delete a certificate that belongs to the authenticated user.
    """
    certificate = get_object_or_404(Certificate, pk=pk, resume_id=resume_id)

    # Ownership check
    if certificate.resume.user != request.user:
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        serializer = CertificateSerializer(certificate)
        return Response(serializer.data)

    if request.method in ["PUT", "PATCH"]:
        serializer = CertificateSerializer(
            certificate,
            data=request.data,
            partial=(request.method == "PATCH"),
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(resume=certificate.resume)  # prevent reassignment
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        certificate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
