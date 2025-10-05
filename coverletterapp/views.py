from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import CoverLetter
from .serializers import CoverLetterSerializer
from accountapp.authentication import JWTAuthentication   # ✅ your custom JWT auth
from accountapp.permissions import IsResumeOwner, IsResumeOwnerOrAdmin, IsAdmin  # ✅ custom permissions


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def cover_letter_list_create(request):
    if request.method == 'GET':
        # ✅ Only fetch cover letters owned by this user
        cover_letters = CoverLetter.objects.filter(user=request.user)
        serializer = CoverLetterSerializer(cover_letters, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        user = request.user

        # ✅ Enforce subscription rule (same as Resume)
        if not user.is_subscribed and user.cover_letters.count() >= 1:
            return Response(
                {"error": "You need a subscription to create more than one cover letter."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CoverLetterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=user)  # 👈 enforce ownership
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsResumeOwnerOrAdmin])   # ✅ only owner or admin
def cover_letter_detail(request, pk):
    cover_letter = get_object_or_404(CoverLetter, pk=pk)

    if request.method == 'GET':
        serializer = CoverLetterSerializer(cover_letter, context={'request': request})
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        serializer = CoverLetterSerializer(
            cover_letter,
            data=request.data,
            partial=(request.method == 'PATCH'),
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)  # 👈 enforce ownership
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        cover_letter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsResumeOwnerOrAdmin])   # ✅ owner or admin can preview
def preview_cover_letter(request, cover_letter_id):
    cover_letter = get_object_or_404(CoverLetter, id=cover_letter_id)

    template_file = cover_letter.template.file.path
    html = render_to_string(template_file, {"cover_letter": cover_letter})
    return HttpResponse(html)


# Create your views here.
