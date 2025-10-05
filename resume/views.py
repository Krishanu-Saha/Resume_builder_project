from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Resume
from .serializers import ResumeSerializer
from accountapp.authentication import JWTAuthentication   # ✅ your custom JWT auth
from accountapp.permissions import IsResumeOwner, IsResumeOwnerOrAdmin, IsAdmin  # ✅ custom permissions


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def resume_list_create(request):
    if request.method == 'GET':
        # ✅ Only fetch resumes owned by this user
        resumes = Resume.objects.filter(user=request.user)
        serializer = ResumeSerializer(resumes, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        user = request.user

        # ✅ Enforce subscription rule:
        if not user.is_subscribed and user.resumes.count() >= 1:
            return Response(
                {"error": "You need a subscription to create more than one resume."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ResumeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=user)  # 👈 enforce ownership
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsResumeOwnerOrAdmin])   # ✅ only owner or admin
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk)

    if request.method == 'GET':
        serializer = ResumeSerializer(resume, context={'request': request})
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        serializer = ResumeSerializer(
            resume,
            data=request.data,
            partial=(request.method == 'PATCH'),
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)  # 👈 enforce ownership
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        resume.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsResumeOwnerOrAdmin])   # ✅ owner or admin can preview
def preview_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    template_file = resume.template.file.path
    html = render_to_string(template_file, {"resume": resume})
    return HttpResponse(html)
