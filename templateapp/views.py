from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from accountapp.permissions import IsAdmin  # ✅ custom admin-only permission
from accountapp.authentication import JWTAuthentication

from .models import ResumeTemplate
from .serializers import ResumeTemplateSerializer


@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def template_list_create(request):
    if request.method == "GET":
        templates = ResumeTemplate.objects.filter(is_active=True)
        serializer = ResumeTemplateSerializer(templates, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        if not request.user.role == "admin":
            return Response({"detail": "Only admins can create templates."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ResumeTemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def template_detail(request, pk):
    template = get_object_or_404(ResumeTemplate, pk=pk)

    if request.method == "GET":
        serializer = ResumeTemplateSerializer(template)
        return Response(serializer.data)

    if request.method in ["PUT", "PATCH"]:
        if not request.user.role == "admin":
            return Response({"detail": "Only admins can update templates."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ResumeTemplateSerializer(template, data=request.data, partial=(request.method == "PATCH"))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        if not request.user.role == "admin":
            return Response({"detail": "Only admins can delete templates."}, status=status.HTTP_403_FORBIDDEN)
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
