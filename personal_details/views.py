from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import PersonalDetails
from .serializers import PersonalDetailsSerializer
from accountapp.authentication import JWTAuthentication
from accountapp.permissions import IsResumeOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from resume.models import Resume


@api_view(['GET', 'POST', 'PUT', 'PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])  # ✅ support file uploads
def personal_details_manage(request, resume_id):
    """
    Get, create, or update personal details for a resume.
    Only the owner or admin can access.
    """
    resume = get_object_or_404(Resume, id=resume_id)

    # Ownership/admin check
    if resume.user != request.user and request.user.role != 'admin':
        return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    # Try to fetch existing personal details
    personal_details = getattr(resume, 'personal_details', None)

    if request.method == 'GET':
        if not personal_details:
            return Response({'detail': 'No personal details found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PersonalDetailsSerializer(personal_details)
        return Response(serializer.data)

    if request.method in ['POST', 'PUT', 'PATCH']:
        if personal_details:
            serializer = PersonalDetailsSerializer(
                personal_details,
                data=request.data,
                partial=(request.method=='PATCH'),
                context={'request': request}
            )
        else:
            serializer = PersonalDetailsSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(resume=resume)  # enforce resume association
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
