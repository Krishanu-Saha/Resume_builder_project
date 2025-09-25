from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Project
from .serializers import ProjectSerializer
from accountapp.authentication import JWTAuthentication
from accountapp.permissions import IsResumeOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from resume.models import Resume


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def project_list_create(request, resume_id):
    """
    List all projects for a resume (owned by the user) or create a new project.
    """
    resume = get_object_or_404(Resume, id=resume_id)

    # enforce ownership
    if resume.user != request.user:
        return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        projects = resume.projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(resume=resume)  # enforce resume assignment
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsResumeOwnerOrAdmin])
def project_detail(request, resume_id, pk):
    """
    Retrieve, update, or delete a project.
    Ownership is enforced via resume.user.
    """
    project = get_object_or_404(Project, pk=pk, resume_id=resume_id)

    # enforce ownership
    if project.resume.user != request.user and request.user.role != 'admin':
        return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        serializer = ProjectSerializer(
            project,
            data=request.data,
            partial=(request.method == 'PATCH'),
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(resume=project.resume)  # prevent changing resume
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
